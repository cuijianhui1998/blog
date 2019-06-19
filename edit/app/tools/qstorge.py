from qiniu import Auth,put_data

QINIU_ACCESS_KEY = 'yqSGVN0FE4wkhVX2S4xAWlqDOtze7PYpHdV9WAVc'
QINIU_SECRET_KEY = '4tMN1Rf4hClLnonAEkP4rel9U3W4rTIFfCkRpJVp'
QINIU_BUCKET_NAME = 'private-blog-image'
QINIU_BUCKET_DOMAIN = 'private-blog.cuijianhui.com'

def uploadImg(fileData):
    access_key = QINIU_ACCESS_KEY
    secret_key = QINIU_SECRET_KEY
    q = Auth(access_key,secret_key)
    bucket_name = QINIU_BUCKET_NAME
    token = q.upload_token(bucket_name,None,3600)
    ret,info = put_data(token,None,fileData)
    if info.status_code == 200:
        # 获取七牛云保存的图片名称
        fileName = ret.get("hash")
        # 拼接完整图片url路径返回
        imgUrl = "http://{}/{}".format(QINIU_BUCKET_DOMAIN, fileName)
        return imgUrl
