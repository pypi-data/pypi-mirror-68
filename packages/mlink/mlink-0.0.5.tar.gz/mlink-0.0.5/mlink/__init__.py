#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sky.li (13751020500@163.com)
# @Desc    : mlink 接口

import asyncio
import websockets
from . import config
from . import message_packer
from . import pyevent

MessagePacker = message_packer.MessagePacker
EventEmitter = pyevent.EventEmitter

# 事件泵
_emitter = EventEmitter()
_URL = "ws://localhost:"+str(config.SERVER_PORT)

# 连接后的客户端, WebSocketClientProtocol
_client = None

# 打包/解包器
_dataPacker = MessagePacker()

# 注册的数据通道
_channels = {}

# 是否关闭
_close = False

# 读入数据 Future, as Promise in nodejs
_getDataFuture = None

# 连接 Future, Future, as Promise in nodejs
_onConnectFuture = None

# 状态
_isStated = False


class _Channel:
    """数据通道类"""

    def __init__(self, chId):
        self.emitter = EventEmitter()
        self._chId = chId
        self.recvFuture = None
        self._sendloop = asyncio.get_event_loop()
        # 向server 注册该通道
        sData = [config.MSG_TAG.msg_reg, self._chId]
        packedData = _dataPacker.pack(sData)
        asyncio.run_coroutine_threadsafe(_client.send(bytes(packedData)),self._sendloop)

    def send(self, data):
        """向server 发送数据"""
        sData = [d for d in data]
        sData.insert(0, self._chId)
        sData.insert(0, config.MSG_TAG.msg_send)
        packedData = _dataPacker.pack(sData)
        asyncio.run_coroutine_threadsafe(_client.send(bytes(packedData)),self._sendloop)

    async def recv(self):
        """server 收到数据"""
        self.recvFuture = asyncio.Future()
        ret = await self.recvFuture
        self.recvFuture = None
        return ret

    def _doRecv(self, data):
        if self.recvFuture != None:
            self.recvFuture.set_result(data)

    def close(self):
        """关闭通道"""
        del _channels[self._chId]
        sData = [config.MSG_TAG.msg_unreg, self._chId]
        packedData = _dataPacker.pack(sData)
        asyncio.run_coroutine_threadsafe(_client.send(bytes(packedData)),self._sendloop)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def doUnpack(data):
    """解包回调"""
    tag = data[0]
    if tag == config.MSG_TAG.msg_recv:
        chId = data[1]
        data = data[2:]
        ch = _channels.get(chId)
        if ch != None:
            ch._doRecv(data)
    else:
        raise Exception('wrong msg tag', tag)


def _reset():
    """重置状态"""
    global _client, _dataPacker, _channels, _close, _getDataFuture
    # 连接后的客户端, WebSocketClientProtocol
    _client = None
    # 打包/解包器
    _dataPacker = MessagePacker()
    # 注册解包回调
    _dataPacker.onUnpack(doUnpack)
    # 注册的数据通道
    _channels = {}
    # 是否关闭
    _close = False
    # 读入数据 Future, as Promise in nodejs
    _getDataFuture = None
    # 连接 Future, Future, as Promise in nodejs
    _onConnectFuture = None
    _isStated = False


async def getData():
    """协程, 从websocket数据"""
    global _client, _onConnectFuture
    try:
        async with websockets.connect(_URL) as websocket:
            print('client connected successfully to', _URL)
            _client = websocket
            _onConnectFuture.set_result(None)
            _onConnectFuture = None
            while not _close:
                try:
                    data = await websocket.recv()
                    _dataPacker.feedBytes(data)
                except Exception as ex:
                    for (_, ch) in _channels.items():
                        if(ch.recvFuture is not None):
                            ch.recvFuture.set_exception(
                                Exception('fail to recv, maybe cause by remote closing'))
                    _reset()
                    return
    except Exception as ex:
        print(ex)

    if _onConnectFuture != None:
        _onConnectFuture.set_exception(
            ('unable to connect to server'))
    _reset()


async def start():
    """ 启动服务 """
    global _onConnectFuture
    global _getDataFuture
    global _isStated
    if _isStated:
        return
    _reset()
    _isStated = True

    _onConnectFuture = asyncio.Future()
    _getDataFuture = asyncio.ensure_future(getData())
    await _onConnectFuture


async def stop():
    """ 停止服务 """
    global _close, _client
    global _isStated
    if not _isStated:
        return
    _isStated = False

    _close = True
    if _client != None:
        await _client.close()
        _client = None
    if _getDataFuture != None:
        _getDataFuture.cancel()
    _reset()


def getChannel(chId):
    """取得channel"""
    ch = _channels.get(chId)
    if ch == None:
        ch = _Channel(chId)
        _channels[chId] = ch
    return ch
