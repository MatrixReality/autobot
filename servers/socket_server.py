#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

import redis

SOCKET_HOST = '192.168.1.4' #TODO: get os.env
SOCKET_PORT = 50001

HOST_REDIS='localhost'
PORT_REDIS=6379

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
    async with websockets.serve(time, SOCKET_HOST, SOCKET_PORT):
        await asyncio.Future()  # run forever


asyncio.run(websocketserver())