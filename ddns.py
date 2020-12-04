#!/usr/bin/env python
# coding=utf-8

import json
import re
import time
import argparse

import requests
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient


def getIP():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    r = requests.get("https://ip.tool.chinaz.com/", headers=headers)
    r.encoding = 'gb2312'
    ip_address_str = re.findall('<dd class="fz24">[.0-9]*</dd>', r.text)
    ip_host = re.findall('\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}', ip_address_str[0])
    return ip_host[0]


def update(access_key, access_secret, domain, second_domain):
    print("start time:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    new_ip = getIP()
    print("current ip:" + new_ip)
    client = AcsClient(access_key, access_secret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    response = client.do_action_with_exception(request)
    records = json.loads(response)['DomainRecords']['Record']

    old_record_id = ''
    old_ip = ''
    for record in records:
        if record['RR'] == second_domain:
            old_ip = record['Value']
            old_record_id = record['RecordId']
            break

    print("old_ip->" + old_ip + ",new_ip->" + new_ip)
    if old_record_id != '' and old_ip != new_ip:
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(old_record_id)
        request.set_RR(second_domain)
        request.set_Type('A')
        request.set_Value(new_ip)
        client.do_action_with_exception(request)
        print('更新ip:' + new_ip)
    elif old_record_id == '':
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_RR(second_domain)
        request.set_Type('A')
        request.set_Value(new_ip)

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        print(str(response, encoding='utf-8'))
        print('添加新ip:' + new_ip)
    else:
        print('不需要更新')
    print("end time:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test for argparse')
    parser.add_argument('--key', '-key', help='阿里云AccessKeyId必填', required=True)
    parser.add_argument('--secret', '-secret', help='阿里云AccessKeySecret必填', required=True)
    parser.add_argument('--domain', '-domain', help='domain一级域名必要参数', required=True)
    parser.add_argument('--record', '-record', help='映射二级域名', required=True, default='ddns')
    parser.add_argument('--interval', '-interval', help='间隔时间', default='30')
    args = parser.parse_args()
    print("key: " + args.key)
    print("secret: " + args.secret)
    print("domain: " + args.domain)
    print("record: " + args.record)
    print("interval: " + args.interval)
    while True:
        try:
            update(args.key, args.secret, args.domain, args.record)
        except BaseException as err:
            print(err)
        time.sleep(int(args.interval))
