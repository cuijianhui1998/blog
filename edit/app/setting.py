import os


class BaseConfig:
    SECRET_KEY = b's\x97_\x95\xcd\xc5\x8c\xa37I\x95\xe9\xcc+-\xa0\xb9\x9a\xef\x04\r\xc7\xd3l'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOW_IMAGE_EXTENSIONS = ['jpg','png','ico','gif']
    FINISHED_MESSAGE = ['你知道吗','告诉你个小技巧','听说','我刚刚知道','号外号外']

    MAIL_VALIDATE_KEY = 'A75mNHZgOMEJ1fqmixtEjUdWmTQa7CdVV9VnjXIOEGDEj6SYzh'

    # 定时任务设置
    JOBS = [{
            'id': 'job1',
            'func': 'app.lib.redis_thumb:redis_to_mysql',
            'trigger': 'interval',
            'seconds': 24*3600
        }]
    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/blog?charset=utf8'

    QINIU_ACCESS_KEY = 'yqSGVN0FE4wkhVX2S4xAWlqDOtze7PYpHdV9WAVc'
    QINIU_SECRET_KEY = '4tMN1Rf4hClLnonAEkP4rel9U3W4rTIFfCkRpJVp'
    QINIU_BUCKET_NAME = 'private-blog-image'
    QINIU_BUCKET_DOMAIN = 'private-blog.cuijianhui.com'

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1450938973@qq.com'
    MAIL_PASSWORD = 'vscodnbujwyxihcg'

class ProductionConfig(BaseConfig):
    ENV = 'production'
    username = os.getenv('MYSQL_USERNAME')
    password = os.getenv('MYSQL_PASSWORD')
    port = os.getenv('MYSQL_PORT')
    database = os.getenv('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@localhost:{port}/{database}?charset=utf8'.format(
        username=username,
        password=password,
        port=port,
        database=database
    )

    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
    QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT  = os.getenv('MAIL_PORT ')
    MAIL_USE_SSL  = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME ')
    MAIL_PASSWORD  = os.getenv('MAIL_PASSWORD ')

class TestConfig(BaseConfig):
    TESTING = True

config = {
    'development':DevelopmentConfig,
    'testing':TestConfig,
    'production':ProductionConfig
}