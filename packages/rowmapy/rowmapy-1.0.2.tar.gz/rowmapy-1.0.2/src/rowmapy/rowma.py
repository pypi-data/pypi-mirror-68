import socketio
import uuid
import json
import requests

class Rowma:
    def __init__(self, base_url = 'https://rowma.moriokalab.com'):
        self.base_url = base_url
        self.sio = socketio.Client()
        self.uuid = str(uuid.uuid4())
        self.namespace = '/rowma'
        self.handlers = {}

    def connect(self):
        self.sio.connect(self.base_url, namespaces=[self.namespace])
        # sleep 1 second for connection establishment
        self.sio.sleep(1)
        payload = { 'applicationUuid': self.uuid }
        self.sio.emit('register_application', data=payload, namespace=self.namespace)
        self.sio.on('topic_to_application', handler=self._baseHandler, namespace=self.namespace)

    def run_launch(self, uuid, command):
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = { 'destination': destination, 'command': command }
        self.sio.emit('run_launch', data=payload, namespace=self.namespace)

    def publish_topic(self, uuid, msg):
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = { 'destination': destination, 'msg': msg }
        self.sio.emit('delegate', payload, namespace=self.namespace)

    def set_topic_route(self, dest_uuid, topic_dest_type, topic_dest_uuid, topic):
        destination = { 'type': 'robot', 'uuid': dest_uuid }
        topic_destination = { 'type': topic_dest_type, 'uuid': topic_dest_uuid }
        msg = {
          'op': 'subscribe',
          'topicDestination': topic_destination,
          'topic': topic
        }
        payload = {
                'destination': destination,
                'msg': msg
                }
        self.sio.emit('delegate', payload, namespace=self.namespace)

    def run_rosrun(self, uuid, command, args=''):
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = {
                'destination': destination,
                'command': command,
                'args': args
                }
        self.sio.emit('run_rosrun', payload, namespace=self.namespace)

    def kill_nodes(self, uuid, rosnodes):
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = {
                'destination': destination,
                'command': command,
                'args': args
                }
        self.sio.emit('run_rosrun', payload, namespace=self.namespace)

    # TODO: Error handling
    def get_current_connection_list(self):
        r = requests.get(self.base_url + '/list_connections')
        return json.loads(r.text)

    # TODO: Error handling
    def get_robot_status(self, uuid):
        params = { 'uuid': uuid }
        r = requests.get(self.base_url + '/robots', params=params)
        return json.loads(r.text)

    def subscribe(self, topic, handler, namespace=None):
        self.handlers[topic] = handler

    def set_robot_uuid(self, robot_uuid):
        payload = {
                'uuid': self.uuid,
                'robotUuid': robot_uuid
                }
        self.sio.emit('update_application', payload, namespace=self.namespace)

    def _baseHandler(self, msg):
        if msg['topic'] in self.handlers:
            handler = self.handlers[msg['topic']]
            handler(msg)
