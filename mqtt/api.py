import time

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.client as client

        
class MqttClient():

    '''
    client_id: 字符串类。连接到代理时使用的唯一客户端ID,当client_id为零长度或无，则将随机生成一个,
在这种情况下，clean_session参数必须为True。    
    clean_session:布尔类。
        如果为True，代理将在断开连接时删除有关此客户端的所有信息。
        如果为False，则客户端是持久客户端，当客户端断开连接时，将保留订阅信息和排队消息。
        注意:客户端永远不会在断开连接时丢弃自己的传出消息。
    示例:
        client = MqttClient("jiangxingai",self.client_session)    
    '''
    def __init__(self,client_id,client_session):
        self.client = mqtt.Client(client_id,client_session)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnetc = self._on_disconnect
        self.client_id = client_id

    '''
    max_msg: 整型。最大消息数，这些消息可以一次通过其网络流,默认为20。增加此值将消耗更多内存，但可以增加吞吐量。
    user_data: 用户定义的任何类型的数据
        注意:在大多数情况下，必须在连接到connecting 之前完成此操作
    示例:
        client.setConfigure(10,None)
    '''
    def set_configure(self,max_msg=20,user_data=None):
        self.client.user_data_set(user_data)
        self.client.max_inflight_messages_set(max_msg)

    '''
    _on_connect: 当代理响应我们的连接请求时调用
    _on_message:在收到客户端订阅的主题的消息,与现有主题过滤器回调不匹配时调用。
    _on_disconnect:当客户端与代理断开连接时调用
    '''
    def _on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def _on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def _on_disconnect(self,client,userdata,rc):
        print("disconnect")
        if rc!=0:
            print("Unexpected disconnection.") # 可能由网络错误引起

    '''
    host:字符串类。远程代理的主机名或IP地址
    port:整型。要连接的服务器主机的网络端口。默认为1883
    keepalive:整型。与代理通信之间允许的最长时间（以秒为单位）。如果没有交换其他消息，则控制客户端将ping消息发送给代理的速率
    bind_address:字符串类。假设存在多个接口，则绑定此客户端的本地网络接口的IP地址
    示例:
        client.connetc("100.2.2.1",1883,64,"192.168.1.2")
    '''
    def connect(self,host,port=1883,keepalive=60,bind_address=""):
        self.client.connect(host,port,keepalive,bind_address)
        self.host = host
        self.port = port
        self.keepalive = keepalive

    '''
    user/passwd:字符串类。为代理身份验证设置用户名和密码。必须在connect *（）之前调用。
    示例:
        client.user_pw_set("user","password")
    '''        
    def user_pw_set(self,user,passwd):
        self.client.username_pw_set(user,passwd)    

    '''
    topic:字符串类。发布遗嘱消息的主题。
    msg:字符串类,要作为遗嘱发送的消息。如果没有给出，或者设置为None，则将使用零长度消息作为遗嘱。传递int或float将导致有效负载转换为表示该数字的字符串。如果您希望发送一个真正的int / float，请使用struct.pack（）来创建所需的有效负载。
    qos:整型。
        级别0：尽力而为。消息发送者会想尽办法发送消息，但是遇到意外并不会重试。
        级别1：至少一次。消息接收者如果没有知会或者知会本身丢失，消息发送者会再次发送以保证消息接收者至少会收到一次，当然可能造成重复消息。
        级别2：恰好一次。保证这种语义肯定会减少并发或者增加延时，不过丢失或者重复消息是不可接受的时候，级别2是最合适的。
    示例:
        client.will_set('test_topic','this is test message',0)
    '''
    def will_set(self,topic,msg,qos): 
        self.client.will_set(topic,msg,qos,True)
        
    '''
    topic:字符串类。类似will_set中的参数
    msg:字符串类,发送的消息。类似will_set中的参数
    qos:整型。类似will_set中的参数
    示例:
        clien..publish('chat','this is test message',0,False)
    '''
    def publish(self,topic,msg,qos,retain=False):
        publish.single(topic,msg,qos,retain,self.host,self.port,self.client_id,self.keepalive)
    
    '''
    topic:字符串类。类似will_set中的参数
    qos:整型。类似will_set中的参数
    callback:对于该主题收到的消息进行特定处理
    示例:
        client.subscribe('chat',0,myCallback)
    '''
    def subscribe(self,topic,qos,callback):
        self.client.subscribe(topic,qos)
        self.client.message_callback_add(topic,callback)


    def unsubscribe(self,topic):
        self.client.message_callback_remove(topic)
        self.client.unsubscribe(topic)


class MqttApi():
    
    def __init__(self,client_id="jiangxingai",client_session=False):
        self.client_id = client_id
        self.client_session = client_session
    
    def new_client(self):
        return MqttClient(self.client_id,self.client_session)


def myCallback(client,userdata,msg):
    print("mu callback function:   "+msg.topic+" : "+str(msg.payload))


if __name__=='__main__':
    c = MqttApi("jiangxingai").new_client()
    c.set_configure(10,None)
    c.user_pw_set("user","password")
    c.connect("127.0.0.1",1883,60,"127.0.0.1")
    c.will_set('test_topic','this is test message',0)



    #1.sub
    c.subscribe('send',2,myCallback)
    c.subscribe('send2',2,myCallback)
    info = client.topic_matches_sub(myCallback,'send')
    print(info)
    c.client.loop_forever()


'''
    #2.publish
    num=0
    client.will_set('test_topic','this is test message',0)
    while True:
        try:
            client.publish('chat',num,2)
        except:
            pass
        num += 1
        print(num)
        time.sleep(2)


'''

