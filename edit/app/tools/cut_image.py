import os

from skimage import io
from matplotlib import pyplot as plt

def get_specification_image(imageFile):
    '''

    :param imageFile: 接受一个image文件
    :return: 返回一个图片文件,高宽比为760:463
    '''
    picture = io.imread(imageFile)
    slice_width, slice_height, _ = picture.shape
    if slice_height > slice_width * 1.5:
        # 加1是为了防止得到的值为0
        height_crop = int((slice_height - slice_width * 1.5) // 2) + 1
        width_crop = 1

    if slice_height < slice_width * 1.5:
        height_crop = 1
        width_crop = int((slice_width - (slice_height / 1.5)) // 2) + 1

    img_data = picture[width_crop:-width_crop, :, :]
    img_data = img_data[:, height_crop:-height_crop, :]
    io.imsave('girl.png',img_data)
    with open('girl.png','rb') as f:
        data = f.read()
    return data


def delete_file():
    os.remove('girl.png')
