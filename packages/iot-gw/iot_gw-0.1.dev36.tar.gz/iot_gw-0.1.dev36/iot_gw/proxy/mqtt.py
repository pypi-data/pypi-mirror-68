import time
import ssl
import logging
from enum import Enum
import paho


class MqttProxy:
    def __init__(self,client_id,username,password,ca_certs_file=None,on_attach=None,on_unattach=None,on_event=None,on_state=None):
        self.__client_id=client_id
        self.__client=paho.mqtt.client.Client(client_id=client_id)
        self.__client.username_pw_set(username=username,password=password)
        if not ca_certs_file is None:
            logging.debug("Enable TLS")
            self.__client.tls_set(ca_certs_file,tls_version= ssl.PROTOCOL_TLSv1_2)
        self.__client.enable_logger(logging)
        self.__client.on_connect=self.__on_connect
        self.__client.on_disconnect=self.__on_disconnect
        self.__client.on_message=self.on_message
        self.__attach_handler=on_attach
        self.__unattach_handler=on_unattach
        self.__event_handler=on_event
        self.__state_handler=on_state
        self.__is_connected=False
        self.__topicHandlers={
            'attach' : self.__on_attach_message,
            'unattach' : self.__on_unattach_message,
            'state' : self.__on_state_message,
            'event' : self.__on_event_message
        }
        
    def connect(self,hostname='localhost',port='1883',timeout=5,async_connect=True):
        if async_connect:
            self.__client.connect_async(hostname,int(port))
            self.__client.loop_start()
            self.__wait_for_connection(timeout)
        else:
            self.__client.connect(hostname,port)
        return self.is_connected()

    def is_connected(self):
        return self.__is_connected

    def config(self,device_id,configuration):
        logging.debug("Config device {}: {}".format(device_id,configuration))
        self.__client.publish(
            topic="/config/{}".format(device_id),
            payload=configuration,
            qos=0)

    def commands(self,device_id,command):
        logging.debug("Commands device {}: {}".format(device_id,command))
        self.__client.publish(
            topic="/commands/{}".format(device_id),
            payload=command,
            qos=0)

    def on_message(self,client,userdata,message):
        payload = str(message.payload.decode('utf-8'))
        logging.debug(
            'Received message \'{}\' on topic \'{}\' with Qos {}'
            .format(payload, message.topic, str(message.qos))
        )
        topics= list(filter(lambda t : len(t) > 0,message.topic.split('/')))
        if topics[0] in self.__topicHandlers:
            self.__topicHandlers[topics[0]](message.payload,topics[1:])
        else:
            logging.warn("MQTT proxy have receiced message on an unknown topic: %s",topics[0])

    def __on_attach_message(self,payload,subtopics):
        device_id=payload.decode('utf-8')
        self.__client.subscribe('/event/{}'.format(device_id))
        self.__client.subscribe('/state/{}'.format(device_id))
        if not self.__attach_handler is None:
            self.__attach_handler(device_id)

    def __on_unattach_message(self,payload,subtopics):
        device_id=payload.decode('utf-8')
        self.__client.unsubscribe('/event/{}'.format(device_id))
        self.__client.unsubscribe('/state/{}'.format(device_id))
        if not self.__unattach_handler is None:
            self.__unattach_handler(device_id)

    def __on_event_message(self,payload,subtopics):
        if not self.__event_handler is None:
            self.__event_handler(subtopics[0],payload)

    def __on_state_message(self,payload,subtopics):
        if not self.__state_handler is None:
            self.__state_handler(subtopics[0],payload)

    def __on_connect(self,client,userdata,flags,rc):
        logging.debug("MQTT client %s connection is up" % self.__client_id)
        self.__client.subscribe('/attach',qos=1)
        self.__client.subscribe('/unattach',qos=1)
        self.__is_connected=True

    def __on_disconnect(self,client,userdate,rc):
        logging.debug("MQTT client %s connection is down" % self.__client_id)
        self.__is_connected=False


    def __wait_for_connection(self, timeout=5):
        total_time = 0
        while not self.__is_connected and total_time < timeout:
            logging.debug("wait_for_connection %d" % timeout)
            if timeout > 0:
                total_time +=1
            time.sleep(1)
        if not self.__is_connected:
            raise RuntimeError('Could not connect to MQTT server.')
        logging.debug("wait_for_connection terminated %s" % self.is_connected)

