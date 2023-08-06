from __future__ import print_function

import argparse
from collections import namedtuple
import json
import sys

import boto3
from botocore.exceptions import ClientError

WhoamiInfo = namedtuple('WhoamiInfo', [
    'Account',
    'AccountAliases',
    'Arn',
    'Type',
    'Name',
    'RoleSessionName',
    'UserId',
])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--profile')

    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()

    try:
        session = boto3.Session(profile_name=args.profile)

        whoami_info = whoami(session)

        if args.json:
            print(json.dumps(whoami_info._asdict()))
        else:
            print(_format_whoami(whoami_info))
    except ClientError as e:
        sys.stderr.write('{}\n'.format(e))
        sys.exit(1)

def _format_whoami(whoami_info):
    lines = []
    lines.append(('Account: ', whoami_info.Account))
    for alias in whoami_info.AccountAliases:
        lines.append(('', alias))
    lines.append(("{}: ".format(whoami_info.Type), whoami_info.Name))
    if whoami_info.RoleSessionName:
        lines.append(('RoleSessionName: ', whoami_info.RoleSessionName))
    lines.append(('Arn: ', whoami_info.Arn))
    lines.append(('UserId: ', whoami_info.UserId))
    max_len = max(len(l[0]) for l in lines)
    return '\n'.join("{}{}".format(l[0].ljust(max_len), l[1]) for l in lines)

def whoami(session=None):
    session = session or boto3.Session()

    data = {}

    response = session.client('sts').get_caller_identity()

    for field in ['Account', 'Arn', 'UserId']:
        data[field] = response[field]

    data['Type'], name = data['Arn'].rsplit(':', 1)[1].split('/',1)

    if data['Type'] == 'assumed-role':
        data['Name'], data['RoleSessionName'] = name.rsplit('/', 1)
    else:
        data['Name'] = name

    data['AccountAliases'] = []
    try:
        #pedantry
        paginator = session.client('iam').get_paginator('list_account_aliases')
        for response in paginator.paginate():
            data['AccountAliases'].extend(response['AccountAliases'])
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') != 'AccessDenied':
            raise

    return WhoamiInfo(**data)

if __name__ == '__main__':
    main()
