import time
import threading

import paho.mqtt.client as mqtt


settings={
	'client':{
		'client_id':'jiangxingai', #can't change after instance
		'client_session':False,    #can't change
		'host':'127.0.0.1', 	   #can't change
		'port':1883,        	   #cantt change
		'keeplive':60,      	   #can't change
		'bind_addr':None,   	   #can't change
	},
	'con':{
		'user_data':None,
		'max_msg':20,
	},
	'secure':{
		'user':'jiangxing',
		'passwd':'ai',
		'will':'this is a abnormal event',
		'retain':True,
	},
	'delay':{  #reconnect delay
		'min':1,
		'max':120,
	},
}

class MqttApi():

	def __init__(self):
		self.client = mqtt.Client(settings['client']['client_id'],settings['client']['client_session'])
#		self.client = mqtt.Client()
		self._callback_set()

	def reinitClient(self):
#		self.client.reinitialise(settings['client']['client_id'],settings['client']['clean_session'])
		self.client.user_data_set(settings['con']['user_data'])
		self.client.max_inflight_messages_set(settings['con']['max_msg'])
		self.client.reconnect_delay_set(settings['delay']['min'],settings['delay']['max'])

	def _callback_set(self):
		self.client.on_connect = self._on_connect
		self.client.on_message = self._on_message
		self.client.on_disconnetc = self._on_disconnect
		
	def _user_pw_set(self):
		self.client.username_pw_set(settings['secure']['user'],settings['secure']['passwd'])	

	def will_set(self,topic,msg,qos): 
		self.client.will_set(topic,msg,qos,settings['secure']['retain'])
	
	def _on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))

	def _on_message(self,client, userdata, msg):
		print(msg.topic+" "+str(msg.payload))

	def _on_disconnect(client,userdata,msg):
		if rc!=0:
			print("Unexpected disconnection.") # 可能由网络错误引起
	
	def connect(self):
		if None != settings['client']['bind_addr']:
			self.client.connect(settings['client']['host'],settings['client']['port'],settings['client']['keeplive'],settings['con']['bind_addr'])
		else:
			self.client.connect(settings['client']['host'],settings['client']['port'],settings['client']['keeplive'])

	def publish(self,topic,data,qos):
		#raise RuntimeError('testError')
		info = self.client.publish(topic,data,qos,settings['secure']['retain'])
		print(info.rc)
	
	def subscribe(self,topic,qos):
		self.client.subscribe(topic,qos)
	
	def loop(self,timeout=None):
		thread = threading.Thread(target=self._loop,args=(timeout,))
		thread.start()

	def _loop(self,timeout=None):
		if not timeout:
			self.client.loop_forever()
		else:
			self.client.loop(timeout)

if __name__=='__main__':
	m = MqttApi()
	m.reinitClient()
	m._user_pw_set()
	m.connect()
	m.will_set('test_topic','this is test message',0)

	#1.sub
	m.subscribe('test_topic',0)
	m.loop()

	#2.publish
	#m.publish('chat','this is test message',0)
	#m.loop()
	#while True:
	#	m.publish('chat','send information in while',2)
	#	time.sleep(2)



