
需要自行安装pyhton3的环境，网上教程很多，这里不在进行赘述
需要安装下面的依赖包
```
pip3 install aliyun-python-sdk-core requests aliyun-python-sdk-alidns  
```

需要在config.json中配置自己的阿里云的accessKey等信息  
domain配置自己的域名  
second-level-domain 配置对应的二级域名，
如果不想使用二级域名可以配置成@，就是一级的域名
然后执行  
python3 DDNS.py

拷贝ddns.service到/usr/lib/systemd/system

设置开机启动
systemctl enable ddns