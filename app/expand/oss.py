# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-03-23.
__author__ = 'Allen xu'
import oss2,json,time,datetime,hmac,base64
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import app.secure as secure
from hashlib import sha1 as sha
expire_time = 30
class StsToken():
    """AssumeRole返回的临时用户密钥
    :param str access_key_id: 临时用户的access key id
    :param str access_key_secret: 临时用户的access key secret
    :param int expiration: 过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
    :param str security_token: 临时用户Token
    :param str request_id: 请求ID
    """
    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''
def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def fetch_sts_token(access_key_id, access_key_secret, role_arn):
    """子用户角色扮演获取临时用户的密钥
    :param access_key_id: 子用户的 access key id
    :param access_key_secret: 子用户的 access key secret
    :param role_arn: STS角色的Arn
    :return StsToken: 临时用户密钥
    """
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    req = AssumeRoleRequest.AssumeRoleRequest()
    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('oss-python-sdk-example')
    body = clt.do_action_with_exception(req)
    j = json.loads(oss2.to_unicode(body))
    token = StsToken()
    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')
    return token


# 获取token，默认为只读权限，当iswrite = true时读写
def get_sts_token(iswrite = ''):
    if iswrite == "write":
        token  = fetch_sts_token(secure.oss_access_key_id,secure.oss_access_key_secret,secure.write_sts_role_arn)
    else:
        token  = fetch_sts_token(secure.oss_access_key_id,secure.oss_access_key_secret,secure.read_sts_role_arn)
    return token


def get_token():
    sts_token = get_sts_token('write')
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire = get_iso_8601(expire_syncpoint)
    path = time.strftime('%Y%m%d')
    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(path+'/');
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())
    h = hmac.new(sts_token.access_key_secret.encode(), policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {}
    token_dict['accessid'] = sts_token.access_key_id
    token_dict['host'] = secure.oss_host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = path+'/'
    result = json.dumps(token_dict)
    return result



