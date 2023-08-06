import time
import json
import logging
import io
import os
import yaml
from flask import Flask, request
from .bridge.gcp import MqttBridge
from .proxy.mqtt import MqttProxy
from .device import DeviceManager

app = Flask(__name__)
bridge = None
proxy = None
device_manager = None
configuration = None

def init(config_path=None, default_config=None):
    global bridge, device_manager, configuration
    configuration = _load_config(config_path,default_config)
    bridge = MqttBridge(configuration['bridge'],on_config=_on_config,on_commands=_on_commands)
    device_manager = DeviceManager(configuration['storage'])
    bridge.connect()
    if 'mqtt' in configuration:
        _init_mqtt(configuration['mqtt'],_attach,_unattach,_publish_event,_publish_state)
    else:
        logging.debug('MQTT proxy is disabled')
    return app

@app.route('/',methods = ['GET'])
def index():
    return 'OK'

@app.route('/device/<device_id>',methods = ['GET'])
def get_device(device_id):
    device = device_manager.get_device(device_id)
    return json.dumps(device.toJson())

@app.route('/device/<device_id>/attach', methods = ['POST'])
def attach(device_id):
    response = _attach(device_id)
    return 'OK' if response is True else 'KO'

@app.route('/device/<device_id>/state', methods = ['POST'])
def publish_state(device_id):
    response = _publish_state(json.dumps(request.json),device_id)
    return 'OK' if response is True else 'KO' 

@app.route('/device/<device_id>/event', methods = ['POST'])
def publish_event(device_id):
    response = _publish_event(json.dumps(request.json),device_id)
    return 'OK' if response is True else 'KO'

def _load_config(config_path='/etc/iot-gw/configuration.yml',default_config=None):
    if config_path is None or not os.path.isfile(config_path):
        result = default_config
    else:
        with io.open(config_path,'r') as stream:
            result = yaml.safe_load(stream)
    return result

def _init_mqtt(config,on_attach=None,on_unattach=None,on_event=None,on_state=None):
    global proxy
    proxy = MqttProxy(
        'gateway',
        config['login'],
        config['password'],
        config['ca_certs_file'] if 'ca_certs_file' in config else None,
        on_attach=_attach,
        on_unattach=_unattach,
        on_state=_publish_state,
        on_event=_publish_event)    
    proxy.connect(config['hostname'],config['port'])
    logging.debug("MQTT proxy is enable: {}".format(proxy.is_connected()))

def _publish_event(device_id,event):
    logging.debug("publish event {}/{}".format(device_id,event))
    return bridge.publish(event,device_id)

def _publish_state(device_id,state):
    logging.debug("publish state {}/{}".format(device_id,state))
    return bridge.publish(state,device_id,'state')

def _attach(device_id):
    logging.debug("attach {}".format(device_id))
    device = device_manager.get_device(device_id)
    return bridge.attach(device_id,device.get_token(get_project_id()))

def _unattach(device_id):
    logging.debug("unattach {}".format(device_id))
    device = device_manager.get_device(device_id)
    return bridge.unattach(device_id,device.get_token(get_project_id()))

def _on_config(device_id,configuration):
    global proxy
    proxy.config(device_id,configuration)

def _on_commands(device_id,commands):
    global proxy
    proxy.commands(device_id,commands)

def get_project_id():
    return configuration['bridge']['project_id'] 

