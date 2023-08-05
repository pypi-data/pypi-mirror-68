#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sky.li (13751020500@163.com)
# @Desc    : similar to nodejs famous Event/Emitter,#
#            BUT, combine on/off to on(name, handle):canceller


class EventEmitter:
    _regCallbacks = {}

    def __init__(self):
        self._regCallbacks = {}

    def emit(self, name, *args):
        cbs = self._regCallbacks.get(name)
        if cbs == None:
            # print(name, 'has not callback')
            return
        for cb in cbs:
            cb(*args)

    def on(self, name, callback):
        cbs = self._regCallbacks.get(name)
        if callback == None:
            raise Exception('set callback with None')
        if cbs == None:
            cbs = []
            self._regCallbacks[name] = cbs

        for cb in cbs:
            if cb == callback:
                return
        cbs.append(callback)

        def can():
            nonlocal cbs
            cbs = [cb for cb in cbs if cb != callback]
            self._regCallbacks[name] = cbs

        return can

    def setCallback(self, name, callback):
        if callback == None:
            raise Exception('set callback with None')
        cbs = []
        if callback != None:
            cbs.append(callback)
        self._regCallbacks[name] = cbs


# def test():
#     emitter = EventEmitter()
#     ta = None

#     def _(a):
#         nonlocal ta
#         ta = a
#     emitter.on('test', _)

#     tb = None

#     def _(b):
#         nonlocal tb
#         tb = b
#     canb = emitter.on('test', _)
#     emitter.emit('test', 1)

#     assert (ta == 1)
#     assert (tb == 1)

#     canb()
#     emitter.emit('test', 2)
#     assert (ta == 2)
#     assert (tb == 1)

#     tc = None

#     def _(c):
#         nonlocal tc
#         tc = c
#     emitter.setCallback('test1', _)
#     emitter.emit('test1', 3)
#     assert (ta == 2)
#     assert (tb == 1)
#     assert (tc == 3)

#     emitter.setCallback('test1', None)
#     emitter.emit('test1', 4)
#     assert (ta == 2)
#     assert (tb == 1)
#     assert (tc == 3)


# test()
