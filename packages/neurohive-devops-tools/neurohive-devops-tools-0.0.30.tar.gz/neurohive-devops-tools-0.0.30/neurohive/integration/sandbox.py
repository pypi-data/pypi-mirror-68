import json
import datetime
from pprint import pprint
import argparse
import logging
import sys
import os
import subprocess
import time
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.ERROR)

HEADER_NAME = 'X-LIB-VERSION'
STICKY_DURATION = 60 * 60  # 1 hour
SERVICE_NAME = 'ustate'
HOSTNAME = 'ustate-stage.mib.neurohive.net'
APP_PORT = 8000
VPC_ID = 'vpc-0877bd4263db7c45b'
LISTENER_ARN = 'arn:aws:elasticloadbalancing:eu-west-1:265052334192:listener/app/mib-testing/3c289b6855ce644f/73c26b32828676db'
TAG_ENV = 'production'
TAG_PROJECT = 'mib'
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURR_PATH)
SERVICE_DIR = os.path.join(CURR_PATH, 'service')
DEPLOY_TIME = int(time.time())
DATA_DIR=os.path.join(PROJECT_DIR, "data_dir")
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)


class AwsWrapperException(Exception):
    pass


# сделать декоратор
#    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
#        logging.error("Unable to update rule")
#        raise AwsWrapperException(response)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lib-version", required=True, type=str)
    parser.add_argument("--build-number", required=True, type=str)
    return parser.parse_args()


def init_terraform():
    cmd = ['terraform', 'init']
    complete = subprocess.run(cmd, capture_output=True, check=True, cwd=SERVICE_DIR)


def     create_service(vars_file):
    state_opt = "-state={}/{}-ustate.state".format(DATA_DIR, DEPLOY_TIME)
    cmd = ['terraform', 'apply', '-auto-approve', '-no-color', state_opt, '-var-file={}'.format(vars_file)]
    try:
        subprocess.check_call(cmd, cwd=SERVICE_DIR)
    except subprocess.CalledProcessError as e:
        logging.error(e)
        sys.exit(1)


def get_rules(listener_arn):
    response = client.describe_rules(
        ListenerArn=listener_arn
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Rules']


def filter_by_id(rules, version):
    host_rules = []
    for rule in rules:
        for cond in rule['Conditions']:
            if cond['Field'] == 'host-header' and HOSTNAME in cond['Values']:
                host_rules.append(rule)
    for hrule in host_rules:
        for cond in hrule['Conditions']:
            if cond['Field'] == 'http-header':
                if cond['HttpHeaderConfig']['HttpHeaderName'] == HEADER_NAME:
                    if version in cond['HttpHeaderConfig']['Values']:
                        return hrule


def update_rule(rule, target_group_arn):
    """ добавить новый forward to"""
    remove_keys = ['Priority', 'Conditions', 'IsDefault']
    [rule.pop(k) for k in remove_keys]
    forward_config = filter(lambda a: a['Type'] == 'forward', rule['Actions']).__next__()
    if 'TargetGroupArn' in forward_config:
        del forward_config['TargetGroupArn']
    # старый вес в 0
    for tg in forward_config['ForwardConfig']['TargetGroups']:
        tg['Weight'] = 0
    # новый вес в 1
    forward_config['ForwardConfig']['TargetGroups'].append(
        {
            'TargetGroupArn': target_group_arn,
            'Weight': 1
        }
    )
    response = client.modify_rule(**rule)
    return response['Rules'][0]['RuleArn']


def create_rule(rules, listener_arn, target_grp_arn, lib_version, hostname, ):
    try:
        new_priority = max([int(r['Priority']) for r in rules if r['Priority'].isdigit()]) + 1
    except ValueError:
        new_priority = 1
    response = client.create_rule(
        ListenerArn=listener_arn,
        Conditions=[
            {
                "Field": "http-header",
                "HttpHeaderConfig": {
                    "Values": [
                        lib_version
                    ],
                    "HttpHeaderName": HEADER_NAME
                }
            },
            {
                "Field": "host-header",
                "HostHeaderConfig": {
                    "Values": [
                        hostname
                    ]
                }
            }
        ],
        Priority=new_priority,
        Actions=[
            {
                'Type': 'forward',
                'ForwardConfig': {
                    'TargetGroups': [
                        {
                            'TargetGroupArn': target_grp_arn,
                            'Weight': 1
                        },
                    ],
                    'TargetGroupStickinessConfig': {
                        'Enabled': True,
                        'DurationSeconds': STICKY_DURATION
                    }
                }
            }
        ]
    )
    logging.info(response)
    return response['Rules'][0]['RuleArn']


def update_listener(listener_arn, target_group_arn, lib_version, hostname):
    rules = get_rules(listener_arn)
    rule = filter_by_id(rules, lib_version)
    if rule is None:
        logging.info("Create new rule")
        return create_rule(rules, listener_arn, target_group_arn, lib_version, hostname)
    else:
        logging.info("Update existent rule")
        return update_rule(rule, target_group_arn)


def create_target_group(lib_version, build_number):
    response_tg = client.create_target_group(
        Name='-'.join([SERVICE_NAME, lib_version, build_number]),
        Protocol='HTTP',
        Port=APP_PORT,
        VpcId=VPC_ID,
        HealthCheckPath='/health',
        TargetType='ip'
    )
    response = client.modify_target_group_attributes(
        TargetGroupArn=response_tg['TargetGroups'][0]['TargetGroupArn'],
        Attributes=[
            {
                'Key': 'stickiness.enabled',
                'Value': 'true'
            },
            {
                'Key': 'stickiness.lb_cookie.duration_seconds',
                'Value': '604800'
            }
        ]
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Cant create target group")
    return response_tg['TargetGroups'][0]['TargetGroupArn']


if __name__ == '__main__':
    args = parse_args()
    init_terraform()
    client = boto3.client('elbv2')
    target_group_arn = create_target_group(args.lib_version, args.build_number)
    rule_arn = update_listener(LISTENER_ARN, target_group_arn, args.lib_version, HOSTNAME)
    data = {
        'image_tag': args.build_number,
        'lib_version': args.lib_version,
        'build_version': args.build_number,
        'target_group_arn': target_group_arn,
        "rule_arn": rule_arn
    }
    vars_file = "{}/{}-ustate.auto.tfvars.json".format(DATA_DIR, DEPLOY_TIME)
    with open(vars_file, "w") as fp:
        fp.write(json.dumps(data))
    create_service(vars_file)
