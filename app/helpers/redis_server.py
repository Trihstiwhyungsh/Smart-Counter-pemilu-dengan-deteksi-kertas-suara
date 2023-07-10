import os
import json
from datetime import timedelta
import redis.asyncio as redis
from redis.connection import ConnectionError
from app import helpers, HTTPStatus

response, message = helpers.response, helpers.constants.message
is_redis_ssl: bool = os.getenv("REDIS_SSL") == "True"

redis_server = redis.Redis(
    host=os.getenv("REDIS_HOST", default="localhost"),
    port=int(os.getenv("REDIS_PORT", default="6379")),
    password=os.getenv("REDIS_PASS", default=""),
    ssl=is_redis_ssl)

async def save(key, value):
    try:
        print(f"Redis connected: {await redis_server.ping()}")
        my_dict = json.dumps({
            "credential": value,
        })
        dict_bytes = bytes(my_dict, 'utf-8')
        await redis_server.set(key, dict_bytes)
        return await redis_server.expire(key, timedelta(minutes=30))
    except ConnectionError:
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message.ERROR.get('ERROR_INTERNAL_SERVER'))
    except TypeError:
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_BAD_REQUEST'))
    finally:
        await redis_server.close()

async def load(key):
    try:
        print(f"Redis connected: {await redis_server.ping()}")
        otp_code = await redis_server.get(key)
        return json.loads(otp_code)
    except ConnectionError:
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message.ERROR.get('ERROR_INTERNAL_SERVER'))
    except RuntimeError:
        return await load(key)
    except TypeError:
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_OTP_CODE_INVALID'))
    finally:
        redis_server.close()

async def unload(key):
    try:
        print(f"Redis connected: {await redis_server.ping()}")
        return await redis_server.delete(key)
    except ConnectionError:
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message.ERROR.get('ERROR_INTERNAL_SERVER'))
    finally:
        redis_server.close()
