# -*- coding: utf-8 -*-
import sys
from layer import SendLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
credentials = ("5219993837042","xAhP79MiyDWWgoMswUa+dPZuSiQ=")
contMessage = (sys.argv[1], sys.argv[2])
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__==  "__main__":
	layers = (
				SendLayer,
				(YowIqProtocolLayer,YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer,YowCallsProtocolLayer,YowMediaProtocolLayer),
				YowLoggerLayer,
				YowCoderLayer,
				YowCryptLayer,
				YowStanzaRegulator,
				YowNetworkLayer
			)
	stack = YowStack(layers)
	stack.setProp(SendLayer.PROP_CONTENT, contMessage)
	stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
	stack.setCredentials(credentials)
	stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
	try:
		stack.loop()
	except AuthError as e:
		print("Authentication Error: %s" % e.message)