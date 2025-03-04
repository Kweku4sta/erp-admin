import json
from typing import Dict, Union

import redis 

from config.setting import settings


class Cacher:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


    def set_value(self, key: str, value: any, expiry: int):
        if isinstance(value, dict):
            value = json.dumps(value)
        self.redis.set(key, value, ex=expiry)

    def get_value(self, key: str)-> Union[Dict, str]:
        value = self.redis.get(key)
        if value:
            try:
                return  json.loads(value.decode("utf-8"))
            except json.JSONDecodeError:
                return value.decode("utf-8")
        return None
    
    def delete_key(self, key: str):
        self.redis.delete(key)

