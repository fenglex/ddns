#!/bin/bash
pip3 install aliyun-python-sdk-core requests aliyun-python-sdk-alidns
cp /opt/ddns/ddns.service /usr/lib/systemd/system/
