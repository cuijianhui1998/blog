
from app.models import Article,Thumb,db
def myredis(enigne=None):
    import redis
    if enigne==None:
        enigne=redis
    pool = enigne.ConnectionPool(host='127.0.0.1',port=6379,password='')
    redis = enigne.Redis(connection_pool=pool)
    return redis

def redis_to_mysql():
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


