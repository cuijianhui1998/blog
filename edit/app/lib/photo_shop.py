import os

from flask import current_app
from qiniu import Auth,put_data
from skimage import io


def uploadImg(fileData):
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']
    q = Auth(access_key,secret_key)
    bucket_name = current_app.config['QINIU_BUCKET_NAME']
    token = q.upload_token(bucket_name,None,3600)
    ret,info = put_data(token,None,fileData)
    if info.status_code == 200:
        # 获取七牛云保存的图片名称
        fileName = ret.get("hash")
        # 拼接完整图片url路径返回
        imgUrl = "http://{}/{}".format(current_app.config['QINIU_BUCKET_DOMAIN'], fileName)
        return imgUrl

def get_specification_image(imageFile):
    '''

    :param imageFile: 接受一个image文件
    :return: 返回一个图片文件,高宽比为760:463
    '''
    picture = io.imread(imageFile)
    slice_width, slice_height, _ = picture.shape
    width_crop=1
    height_crop = 1
    if slice_height > slice_width * 1.5:
        # 加1是为了防止得到的值为0
        height_crop = int((slice_height - slice_width * 1.5) // 2) + 1

    if slice_height < slice_width * 1.5:

        width_crop = int((slice_width - (slice_height / 1.5)) // 2) + 1

    img_data = picture[width_crop:-width_crop, :, :]
    img_data = img_data[:, height_crop:-height_crop, :]
    io.imsave('girl.png',img_data)
    with open('girl.png','rb') as f:
        data = f.read()
    return data


def delete_file():
    os.remove('girl.png')
