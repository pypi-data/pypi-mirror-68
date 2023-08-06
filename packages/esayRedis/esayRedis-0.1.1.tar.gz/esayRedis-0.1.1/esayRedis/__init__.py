import redis
# from redlock.lock import RedLock
# import asyncio
# import time
import fastapi
import pydantic
import starlette.requests

class EsayRedis:
    def __init__(self):
        self.redis_pool = None
    
    def init_app(self,app:fastapi.FastAPI=None,config:pydantic.BaseSettings=None):

        if config is not None:
            self.config = config
        else:
            self.config = RedisConfig()

        app.state.REDIS = self

    def init(self):
        if self.redis_pool is not None:
            raise RedisError('Redis is already initialized')

        self.redis_pool = redis.ConnectionPool(**self.getconfig())
        self.conTest()
        # exception handel by redis
        
    def Redis(self):

        return redis.StrictRedis(connection_pool=self.redis_pool)
    def conTest(self):

        redis.StrictRedis(connection_pool=self.redis_pool).dbsize()
        # exception handel by redis

    def getconfig(self):
        opts = dict(
            host=self.config.redis_host,
            port=self.config.redis_port,
            db=self.config.redis_db,
            decode_responses = self.config.redis_decode_responses,
            socket_timeout = self.config.redis_connection_timeout,
            password=self.config.redis_password,
            #min_connections=self.config.redis_pool_minsize,
            max_connections=self.config.redis_pool_maxsize,
        )
        return opts



class RedisError(Exception):
    pass

class RedisConfig(pydantic.BaseSettings):
    class Config:
        env_prefix = ''
        use_enum_values = True
    redis_host: str = '192.168.201.169'
    redis_port: int = 6379
    redis_password: str = None
    redis_db: int = 0
    redis_connection_timeout: int = 1
    redis_decode_responses=True
    redis_pool_minsize: int = 1
    redis_pool_maxsize: int = 50



app = fastapi.FastAPI()
esayredis = EsayRedis()

esayredis.init_app(app=app)
esayredis.init()
r = esayredis.Redis()
r.set("foodd","va")
s = r.get("foodd")
print(s)










 

