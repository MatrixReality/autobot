#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import redis

from dotenv import dotenv_values

config = dotenv_values("../.env")
WEBSOCKET_HOST = config["WEBSOCKET_HOST"]
WEBSOCKET_PORT = config["WEBSOCKET_PORT"]
HOST_REDIS = config["HOST_REDIS"]
PORT_REDIS = config["PORT_REDIS"]

redis_service = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, db=0)

def reverserd_iterator(iter):
    return reversed(list(iter))

async def time(websocket, path):
    redis_service.flushdb()
    while True:
        for key in redis_service.scan_iter("display_log:*"):
            msg = str(redis_service.get(key))
            print(msg)
            await websocket.send(msg)
            redis_service.delete(key)
        
        distance_log = redis_service.get("distance_log")
        if distance_log is not None:
            msg = str(distance_log)
            print(msg)
            await websocket.send(msg)
            #redis_service.delete("distance_log")        

async def websocketserver():
    async with websockets.serve(time, WEBSOCKET_HOST, WEBSOCKET_PORT):
        await asyncio.Future()  # run forever


asyncio.run(websocketserver())