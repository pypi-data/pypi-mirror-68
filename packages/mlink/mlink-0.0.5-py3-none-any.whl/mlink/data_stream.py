#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sky.li (13751020500@163.com)
# @Desc    : 数据包解析工具类

import asyncio

# 字节流解析
class DataStream:
    def __init__(self):
        self._datas = []
        self._reqCount = -1
        self._recvFuture = None  # 接收字节future
        self._toMatch = []  # 匹配头
        self._recvTillFuture = None  # 接收匹配字节 future
        self._recvLoop = asyncio.get_event_loop()

    # 字节流收到匹配 buff
    async def recv(self, n):
        self._reqCount = n
        self._recvFuture = asyncio.Future()
        self._recvLoop.call_soon_threadsafe(self._tryRecv)
        return await self._recvFuture

    # 字节流收到匹配 buff

    def isEmpty(self):
        return len(self._datas) == 0

    # 字节流收到匹配 buff
    async def recvTill(self, buff):
        self._toMatch = []
        for byte in buff:
            self._toMatch.append(byte)
        self._recvTillFuture = asyncio.Future()
        self._recvLoop.call_soon_threadsafe(self._tryRecvTill)
        await self._recvTillFuture

    def _tryRecvTill(self):
        if self._recvTillFuture == None:
            return
        while True:  # lable tryRecv
            noMatch = False
            for i in range(len(self._toMatch)):
                # no more byte now
                if i == len(self._datas):
                    return
                if self._toMatch[i] != self._datas[i]:
                    self._datas.pop(0)
                    noMatch = True
                    break
            if not noMatch:
                break

        res = self._recvTillFuture
        self._recvTillFuture = None
        self._datas = self._datas[len(self._toMatch):]
        self._toMatch = []
        res.set_result(None)

    def _tryRecv(self):
        if (self._recvFuture == None):
            return
        if (len(self._datas) >= self._reqCount):
            rest = self._datas[self._reqCount:]
            nbytes = self._datas[:self._reqCount]
            self._datas = rest
            self._reqCount = -1

            res = self._recvFuture
            self._recvFuture = None
            res.set_result(nbytes)
    
    # 填入数据
    def feedBytes(self, data):
        for byte in data:
            self._datas.append(byte)
        self._tryRecv()
        self._tryRecvTill()


# def __test():
#     ds = DataStream()
#     head = [b for b in bytes("_8weurswea_", 'utf-8')]

#     async def t1():
#         data = await ds.recv(2)
#         assert (data == [1, 2])
#         data = await ds.recv(3)
#         assert (data == [3, 4, 5])
#         await ds.recvTill(head)
#         assert (ds._datas == [11, 23])

#     async def t2():
#         await asyncio.sleep(1)
#         ds.feedBytes([1])
#         ds.feedBytes([2])
#         ds.feedBytes([3, 4])
#         ds.feedBytes([5, 6])

#         ds.feedBytes(head)
#         ds.feedBytes([11, 23])
#         print('from t2')

#     asyncio.gather(t2(), t1())

#     async def main():
#         t = await asyncio.gather(t2(), t1())
#         print(t)

#     asyncio.run(main())


# __test()
