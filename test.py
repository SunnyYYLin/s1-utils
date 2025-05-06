# 引入模块
import os
from obs import ObsClient

OBS_SERVER = "obs.cn-east-4.myhuaweicloud.com"
ak = os.getenv("HuaweiCloudAccessKeyID")
sk = os.getenv("HuaweiCloudSecretAccessKey")
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=OBS_SERVER)
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
    print(len(resp.body.contents))
    assert resp.status < 300, f"listObjects failed: {resp.status} {resp.body}"
    return [obj for obj in resp.body.contents if obj.key.endswith(suffix)]

print(get_log_objects(log_dir=log_dir, client=obsClient))

# 关闭obsClient
obsClient.close()