# -*- coding: utf-8 -*-
import datetime
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
import threading
import sys

class SendLayer(YowInterfaceLayer):

	PROP_CONTENT = "to + msg"

	def __init__(self):
		super(SendLayer, self).__init__()
		self.ackQueue = []
		self.lock = threading.Condition()

	@ProtocolEntityCallback("success")
	def onSuccess(self, successProtocolEntity):
		self.lock.acquire()
		self.phone, self.message= self.getProp(self.__class__.PROP_CONTENT)
		messageEntity = TextMessageProtocolEntity(self.message.encode('utf-8'), to = "%s@s.whatsapp.net" % self.phone)
		self.ackQueue.append(messageEntity.getId())
		self.toLower(messageEntity)
		self.lock.release()

	@ProtocolEntityCallback("ack")
	def onAck(self, entity):
		self.lock.acquire()
		if entity.getId() in self.ackQueue:
			self.ackQueue.pop(self.ackQueue.index(entity.getId()))

		if not len(self.ackQueue):
			self.lock.release()
			self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
			sys.exit(0)

		self.lock.release()