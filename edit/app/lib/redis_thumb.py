from app import create_app
from app.models import Article,Thumb,db

def myredis(enigne=None):
    import redis
    if enigne==None:
        enigne=redis
    pool = enigne.ConnectionPool(host='127.0.0.1',port=6379,password='')
    redis = enigne.Redis(connection_pool=pool)
    return redis

APP = None
def get_app():
    global APP
    APP = APP if APP is not None else create_app()

def redis_to_mysql():
    get_app()
    with APP.app_context():
        print("hello")
        redis = myredis()
        articles = Article.query.all()
        redis.delete('thumbs_total')
        thumbs = redis.keys(pattern='thumb-*')
        for thumb in thumbs:
            aid = int(thumb.decode().split('-')[1])
            uid_list = redis.smembers(thumb)
            for uid in uid_list:
                with db.submit_data():
                    t = Thumb()
                    t.auth_id=int(uid)
                    t.article_id=aid
                    db.session.add(t)
            redis.delete(thumb)
        for article in articles:
            redis.hset('thumbs_total',article.id,len(article.thumbs))
        print("执行了一次定时任务")


