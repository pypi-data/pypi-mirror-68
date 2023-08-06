import unittest
import paho.mqtt.client
from iot_gw.proxy.mqtt import MqttProxy
from mockito import mock, verify, when



class Message:
    def __init__(self,topic,payload,qos=0):
        self.topic=topic
        self.payload=payload.encode('utf-8')
        self.qos=qos

class MqttProxyTest(unittest.TestCase):

    def test_attach_topic(self):
        listenerMock = mock()
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='client_id').thenReturn(mqttMock)
        proxy = MqttProxy('client_id','username','password',on_attach=listenerMock.on_attach)
        message = Message('/attach','device_id')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).on_attach('device_id')
        verify(mqttMock,times=1).subscribe('/event/device_id')
        verify(mqttMock,times=1).subscribe('/state/device_id')

    def test_unattach_topic(self):
        listenerMock = mock()
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='client_id').thenReturn(mqttMock)
        proxy = MqttProxy('client_id','username','password',on_unattach=listenerMock.on_unattach)
        message = Message('/unattach','device_id')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).on_unattach('device_id')
        verify(mqttMock,times=1).unsubscribe('/event/device_id')
        verify(mqttMock,times=1).unsubscribe('/state/device_id')

    def test_config(self):
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='client_id').thenReturn(mqttMock)
        proxy = MqttProxy('client_id','username','password')
        proxy.config('device_id','configuration')
        verify(mqttMock,times=1).publish(
            topic='/config/device_id',
            payload='configuration',
            qos=0
        )
    
    def test_commands(self):
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='client_id').thenReturn(mqttMock)
        proxy = MqttProxy('client_id','username','password')
        proxy.commands('device_id','command')
        verify(mqttMock,times=1).publish(
            topic='/commands/device_id',
            payload='command',
            qos=0
        )

    def test_state_topic(self):
        listenerMock = mock()
        proxy = MqttProxy('client_id','username','password',on_state=listenerMock.on_state)
        message = Message('/state/device_id','state')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).on_state('device_id',b'state')

    def test_event_topic(self):
        listenerMock = mock()
        proxy = MqttProxy('client_id','username','password',on_event=listenerMock.on_event)
        message = Message('/event/device_id','event')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).on_event('device_id',b'event')



    
