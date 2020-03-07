#!/usr/bin/env python
# coding=utf-8

import json
import re
import time

import requests
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient


def get_ip():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    #  r = requests.get('https://www.ip.cn/')
    # r = requests.get('http://ipinfo.io/ip', headers=headers)
    # r = requests.get('http://www.ip138.com/', headers=headers)
    r = requests.get("https://2020.ip138.com/", headers=headers)
    r.encoding = 'gb2312'
    get_ip_address = re.findall('<iframe.*</iframe>', r.text)
    ip_host = re.findall('src="(.*?)"', get_ip_address[0])
    ip_str = requests.get(ip_host[0], headers=headers)
    ip = re.findall('\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}', ip_str.text)
    return ip[0]


def getIP():
    response = requests.get("http://2020.ip138.com/ic.asp")
    ip = re.search(r"\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]", response.content.decode(errors='ignore')).group(0)
    return ip.replace("[", "").replace("]", "")


def update():
    print("start time:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    new_ip = getIP()
    with open("./config.json", 'r') as load_f:
        load_dict = json.load(load_f)
    accessKeyId = load_dict['AccessKeyId']
    accessKeySecret = load_dict['AccessKeySecret']
    domain = load_dict['domain']
    secondDomain = load_dict['second-level-domain']
    client = AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    response = client.do_action_with_exception(request)
    records = json.loads(response)['DomainRecords']['Record']

    old_record_id = ''
    old_ip = ''
    for record in records:
        if record['RR'] == secondDomain:
            old_ip = record['Value']
            old_record_id = record['RecordId']
            break

    print("old_ip->" + old_ip + ",new_ip->" + new_ip)
    if old_record_id != '' and old_ip != new_ip:
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(old_record_id)
        request.set_RR(secondDomain)
        request.set_Type('A')
        request.set_Value(new_ip)
        client.do_action_with_exception(request)
        print('更新ip:' + new_ip)
    elif old_record_id == '':
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_RR(secondDomain)
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
    while True:
        try:
            update()
        except BaseException as err:
            print(err)
        time.sleep(10)
