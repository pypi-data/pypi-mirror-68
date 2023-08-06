# -*- coding: utf-8 -*-
from twisted.python import log
from twisted.internet import reactor, ssl

from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

import json
from collections import namedtuple


class SparkWorksWebSocketMessage(object):
    __timestamp = None
    __resource_uri = None
    __value = None

    def __init__(self, jsonString=None, timestamp=None, resourceUri=None, value=None):
        dictionary = json.loads(jsonString, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.__timestamp = dictionary.timestamp
        self.__resource_uri = dictionary.resourceUri
        self.__value = dictionary.value

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ': '))

    def value(self):
        return self.__value

    def resource_system_name(self):
        return self.__resource_uri

    def timestamp(self):
        return self.__timestamp


class SparkWorksWebSocket(object):
    __url = None
    __token = None
    __handler = None
    __configuration = None

    class SparkWorksWebSocketClientProtocol(WebSocketClientProtocol):
        def onJoin(self):
            print("onJoin")

        def onOpen(self):
            print("onOpen")

        def onMessage(self, payload, isBinary):
            message = payload.decode('utf8')
            self.messageReceived(SparkWorksWebSocketMessage(jsonString=message))

        def messageReceived(self, message):
            pass

        def onClose(self, wasClean, code, reason):
            print("WebSocket connection closed: {}".format(reason))

    class SparkWorksWebSocketConnectionFactory(WebSocketClientFactory, ReconnectingClientFactory):

        def clientConnectionFailed(self, connector, reason):
            print("Client connection failed .. retrying ..")
            self.retry(connector)

        def clientConnectionLost(self, connector, reason):
            print(self.url)
            print("Client connection lost .. retrying ..")
            self.retry(connector)

    def __init__(self, url='wss://ws.sparkworks.net/websocket', configuration=None, token=None, handler=None):
        self.__url = url
        self.__token = token
        self.__handler = handler
        self.__configuration = configuration

    def start(self):
        token = None
        if self.__token is not None:
            token = self.__token
        elif self.__configuration is not None:
            self.__configuration.connect()
            token = self.__configuration.access_token
        factory = self.SparkWorksWebSocketConnectionFactory(self.__url + "?access_token=" + token)
        factory.protocol = self.__handler
        # SSL client context: default
        ##
        if factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        connectWS(factory, contextFactory)
        reactor.run()
