#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sky.li (13751020500@163.com)
# @Desc    : 协议包工具类

import asyncio
from . import config
from . import data_stream
from . import pyevent

DataStream = data_stream.DataStream
EventEmitter = pyevent.EventEmitter

_magic_head = bytes(config.MAGIC_HEAD, 'utf-8')


# 协议包打包解包
class MessagePacker:
    _emitter: EventEmitter = EventEmitter()
    _stream: DataStream = DataStream()

    def __init__(self):
        self._isPacking = False
        self._emitter: EventEmitter = EventEmitter()
        self._stream: DataStream = DataStream()

    # 得到协议包
    def pack(self, data):
        msg = [b for b in _magic_head]
        l = len(data)
        lo = (l & 0x00ff)
        hi = (l & 0xff00) >> 8
        msg.append(lo)
        msg.append(hi)
        for byte in data:
            msg.append(byte)
        return msg

    # 解协议包
    async def _unpack(self):
        if (self._isPacking):
            raise Exception('packing')
        self._isPacking = True
        while True:
            data = await self._unpackOnce()
            self._emitter.emit('unpack', data)
            if self._stream.isEmpty():
                break
        self._isPacking = False

    async def _unpackOnce(self):
        await self._stream.recvTill(_magic_head)
        lohi = await self._stream.recv(2)
        lo, hi = lohi[0], lohi[1]
        len = hi * 0xff + lo
        data = await self._stream.recv(len)
        return data

    # 当解出完整包
    def onUnpack(self, h):
        return self._emitter.on('unpack', h)

    # 送入字节
    def feedBytes(self, data):
        if (not self._isPacking):
            asyncio.ensure_future(self._unpack())
        self._stream.feedBytes(data)


# def __test():
#     import asyncio

#     async def test3():
#         print('............test MessagePacker1')
#         data = [33, 44]
#         dataRecv = None
#         s = MessagePacker()

#         def cb(d):
#             print('cb', d)
#             nonlocal dataRecv
#             dataRecv = d
#         s.onUnpack(cb)
#         s.feedBytes([1, 2])
#         await asyncio.sleep(0)
#         s.feedBytes([3, 4])
#         packed = s.pack(data)
#         print('packed', packed)
#         s.feedBytes(packed)
#         await asyncio.sleep(0.1)
#         assert (s._isPacking == False)
#         s.feedBytes([5])
#         await asyncio.sleep(0.1)
#         assert (s._isPacking == True)
#         s.feedBytes([6, 7])
#         await asyncio.sleep(0.1)
#         assert (s._isPacking == True)

#         await asyncio.sleep(0.2)
#         assert (data == dataRecv)
#         assert (s._stream._datas == [])
#         print('MessagePacker1 pass')

#     asyncio.run(test3())


# __test()
