FROM python:3.6-alpine
MAINTAINER fenglex@126.com
ENV key ''
ENV secret ''
ENV domain ''
ENV record ''
ENV interval ''
WORKDIR /opt/ddns

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
&& apk update \
&& apk add build-base gcc libffi-dev openssl libressl-dev \
&& pip3 install -i https://mirrors.aliyun.com/pypi/simple/ requests aliyun-python-sdk-core aliyun-python-sdk-alidns
#RUN pip install -i aliyun-python-sdk-core requests aliyun-python-sdk-alidns
COPY ddns.py /opt/ddns/

ENTRYPOINT python ddns.py -key ${key} -secret ${secret} -domain ${domain} -record ${record} -interval ${interval}

# build command
# docker build -t fenglex/ddns .