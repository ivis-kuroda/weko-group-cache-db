import redis
from redis import sentinel

from . import config


class RedisConnection:
    """Redis connection class

    Attributes:
        redis_type(str): redis type(redis or sentinel)

    Methods:
        connection(db): Establish Redis connection and return Redis store object
        redis_connection(db): Establish Redis connection and return Redis store object
        sentinel_connection(db): Establish Redis sentinel connection and return Redis store object
    """
    def __init__(self):
        self.redis_type = config.CACHE_TYPE
    
    def connection(self, db) -> redis.Redis:
        """Establish Redis connection and return Redis store object

        Arguments:
            db(int): Redis db number what connect to

        Returns:
            redis.Redis: Redis store object
        """
        store = None
        try:
            if self.redis_type == 'redis':
                store = self.redis_connection(db)
            elif self.redis_type == 'sentinel':
                store = self.sentinel_connection(db)
            if not store:
                raise Exception('Failed to connect to Redis')
        except Exception as ex:
            raise ex
        
        return store
    
    def redis_connection(self, db):
        """Establish Redis connection and return Redis store object

        Arguments:
            db(int): Redis db number what connect to

        Returns:
            redis.Redis: Redis store object
        """
        store = None
        try:
            redis_url = config.REDIS_URL + str(db)
            store = redis.Redis.from_url(redis_url)
        except Exception as ex:
            raise ex

        return store

    def sentinel_connection(self, db):
        """Establish Redis sentinel connection and return Redis store object

        Arguments:
            db(int): Redis db number what connect to

        Returns:
            redis.Redis: Redis store object
        """
        store = None
        try:
            sentinels = sentinel.Sentinel(config.CACHE_REDIS_SENTINELS, decode_responses=False)
            store = sentinels.master_for(config.CACHE_REDIS_SENTINEL_MASTER, db=db)
        except Exception as ex:
            raise ex

        return store
