#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sky.li (13751020500@163.com)
# @Desc    : 工程配置项

class MSG_TAG:
    msg_reg = 0  # reg(ch) // 注册一个通道
    msg_unreg = 1  # unreg(ch) // 取消注册一个通道
    msg_send = 2  # send(ch, data) // (客户端)发送数据到通道
    msg_recv = 3  # recv(ch, data) // (客户端收到)从数据通道收到数据


# 服务端 port
SERVER_PORT = 20101

# 协议头
MAGIC_HEAD = "__a4z1v1"
