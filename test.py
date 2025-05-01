# 引入模块
import os
from obs import ObsClient
from collections import namedtuple

# 推荐通过环境变量获取AKSK，这里也可以使用其他外部引入方式传入，如果使用硬编码可能会存在泄露风险。
# 您可以登录访问管理控制台获取访问密钥AK/SK，获取方式请参见https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html。
ak = os.getenv("AccessKeyID")
sk = os.getenv("SecretAccessKey")
# 【可选】如果使用临时AKSK和SecurityToken访问OBS，则同样推荐通过环境变量获取
security_token = os.getenv("SecurityToken")
#  server填写Bucket对应的Endpoint, 这里以华北-北京四为例，其他地区请按实际情况填写。
server = "obs.cn-east-4.myhuaweicloud.com"
# 创建obsClient实例
# 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
# 使用访问OBS
log_dir = '/wenge/log'

def get_log_objects(log_dir: str, client: ObsClient) -> set[namedtuple]:
    """
    获取指定目录下的所有日志文件
    """
    bucket, _, dir = log_dir.strip('/').partition('/')
    print(bucket, dir)
    resp = obsClient.listObjects(bucket, prefix=dir)
    target_objs = {}
    for o in resp.body.contents:
        if '/' in o['key'].removeprefix(dir).strip('/'):
            # ignore logs in subfolders
            continue
        print(o['key'])
        if o['key'].endswith('.log'):
            print(o['key'])
            target_objs.add(namedtuple(o))
    return target_objs

print(get_log_objects(log_dir=log_dir, client=obsClient))

# 关闭obsClient
obsClient.close()