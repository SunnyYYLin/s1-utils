# 引入模块
import os
from obs import ObsClient
from collections import namedtuple

# 推荐通过环境变量获取AKSK，这里也可以使用其他外部引入方式传入，如果使用硬编码可能会存在泄露风险。
# 您可以登录访问管理控制台获取访问密钥AK/SK，获取方式请参见https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html。
ak = os.getenv("HuaweiCloudAccessKeyID")
sk = os.getenv("HuaweiCloudSecretAccessKey")
# 【可选】如果使用临时AKSK和SecurityToken访问OBS，则同样推荐通过环境变量获取
security_token = os.getenv("SecurityToken")
#  server填写Bucket对应的Endpoint, 这里以华北-北京四为例，其他地区请按实际情况填写。
server = "obs.cn-east-4.myhuaweicloud.com"
# 创建obsClient实例
# 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
# 使用访问OBS
log_dir = '/wenge/log'

def get_log_objects(log_dir: str, client: ObsClient, suffix='.log') -> list[dict]:
    """
    Retrieves a list of log objects from a specified directory in an OBS bucket.
    Args:
        log_dir (str): The directory path in the OBS bucket where logs are stored. 
                       It should be in the format 'bucket_name/directory/'.
        client (ObsClient): The OBS client instance used to interact with the OBS service.
        suffix (str, optional): The file suffix to filter log files. Defaults to '.log'.
    Returns:
        list[dict]: A list of dictionaries representing the log objects that match the specified suffix.
    Raises:
        AssertionError: If the response status from the OBS service is not successful (< 300).
    """
    bucket, _, dir = log_dir.strip('/').partition('/')
    dir += '/'
    print(bucket, dir)
    resp = obsClient.listObjects(bucket, prefix=dir, delimiter="/")
    print(resp)
    assert resp.status < 300, f"listObjects failed: {resp.status} {resp.body}"
    return [obj for obj in resp.body.contents if obj.key.endswith(suffix)]

print(get_log_objects(log_dir=log_dir, client=obsClient))

# 关闭obsClient
obsClient.close()