"""
pangu_base_aio.py

 Copyright (c) 2018-2019  All right reserved.

 Python pangu is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from __future__ import unicode_literals

import zmq.asyncio
import socket
import asyncio
import msgpack
import sys
import zmq
import psutil


# adapter data
ADAPTER_TOPIC = "adapter/extensions/data"  # 来自插件的消息，topic


# noinspection PyMethodMayBeStatic
class PanguBaseAIO(object):
    """

    This is the asyncio base class for Python Pangu components,
    encapsulating and acting as an abstraction layer for zeromq and message pack
    functionality.

    Pangu components are derived by inheriting from this class and
    overriding its methods as necessary.

    Pangu components have the capability to both publish and subscribe to user
    defined messages using the Pangu ai-adapter-core.

    To import into  the derived class use:

           from python_pangu.pangu_base_aio import PanguBaseAIO

    """

    def __init__(self, back_plane_ip_address=None, subscriber_port='16103',
                 publisher_port='16130', process_name='None',
                 external_message_processor=None, receive_loop_idle_addition=None,
                 connect_time=0.3, subscriber_list=None, event_loop=None):

        """
        The __init__ method sets up all the ZeroMQ "plumbing"

        :param back_plane_ip_address: pangu_base back_planeIP Address -
                                      if not specified, it will be set to the
                                      local computer.

        :param subscriber_port: pangu_base back plane subscriber port.
               This must match that of the pangu_base backplane

        :param publisher_port: pangu_base back plane publisher port.
                               This must match that of the pangu_base backplane.

        :param process_name: Component identifier in banner at component startup.

        :param external_message_processor: external method to process messages

        :param receive_loop_idle_addition: an external method called in the idle section
                                           of the receive loop

        :param connect_time: a short delay to allow the component to connect to the Backplane
        """

        # call to super allows this class to be used in multiple inheritance scenarios when needed
        super(PanguBaseAIO, self).__init__()

        
        if not hasattr(self, 'TOPIC'):
            self.TOPIC = ADAPTER_TOPIC  # message topic: the message from adapter
        if not hasattr(self, 'EXTENSION_ID'):
            self.EXTENSION_ID = "eim"
            
        self.backplane_exists = False

        self.back_plane_ip_address = None
        self.external_message_processor = external_message_processor
        self.receive_loop_idle_addition = receive_loop_idle_addition
        self.connect_time = connect_time
        self.subscriber_list = subscriber_list
        self.my_context = None
        self.subscriber = None
        self.publisher = None
        self.the_task = None

        if event_loop:
            self.event_loop = event_loop
        else:
            # fix for "not implemented" bugs in Python 3.8
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            self.event_loop = asyncio.get_event_loop()

        self.back_plane_ip_address = '127.0.0.1'

        self.subscriber_port = subscriber_port
        self.publisher_port = publisher_port

        print('\n************************************************************', flush=True)
        print(process_name + ' using Back Plane IP address: ' + self.back_plane_ip_address, flush=True)
        print('Subscriber Port = ' + self.subscriber_port, flush=True)
        print('Publisher  Port = ' + self.publisher_port, flush=True)
        print('************************************************************', flush=True)

    # noinspection PyUnresolvedReferences
    async def begin(self):
        # establish the zeromq sub and pub sockets and connect to the backplane
        if not self.my_context:
            self.my_context = zmq.asyncio.Context()
        # noinspection PyUnresolvedReferences
        self.subscriber = self.my_context.socket(zmq.SUB)
        connect_string = "tcp://" + self.back_plane_ip_address + ':' + self.subscriber_port
        self.subscriber.connect(connect_string)

        self.publisher = self.my_context.socket(zmq.PUB)
        connect_string = "tcp://" + self.back_plane_ip_address + ':' + self.publisher_port
        self.publisher.connect(connect_string)

        if self.subscriber_list:
            for topic in self.subscriber_list:
                await self.set_subscriber_topic(topic)


        print('self.subscriber', self.subscriber, flush=True)
        print('self.publisher', self.publisher, flush=True)
        # Allow enough time for the TCP connection to the Backplane complete.
        # time.sleep(self.connect_time)
        await asyncio.sleep(self.connect_time)

        # start the receive_loop
        self.the_task = self.event_loop.create_task(self.receive_loop())

    async def pack(self, data):
        return msgpack.packb(data, use_bin_type=True)

    async def unpack(self, data):
        return msgpack.unpackb(data, raw=False)


    async def message_template(self):
        '''
        todo: attr

        topic: self.TOPIC
        payload:
            extension_id?
            content
            sender
            timestamp?
        '''
        message_template = {
            "payload": {
                "content": {},
                "sender": self.name,
                "extension_id": self.EXTENSION_ID
            }
        }
        return message_template

    async def publish(self, message):
        assert isinstance(message, dict)
        topic = message.get('topic')
        payload = message.get("payload")
        if not topic:
            topic = self.TOPIC
        if not payload.get("extension_id"):
            payload["extension_id"] = self.EXTENSION_ID

        await self.publish_payload(payload, topic)

    async def get_extension_id(self):
        return self.EXTENSION_ID

    async def publish_payload(self, payload, topic=''):
        """
        This method will publish a python_pangu payload and its associated topic

        :param payload: Protocol message to be published

        :param topic: A string value
        """

        # make sure the topic is a string
        if not type(topic) is str:
            raise TypeError('Publish topic must be python_pangu string', 'topic')

        message = await self.pack(payload)

        pub_envelope = topic.encode()
        await self.publisher.send_multipart([pub_envelope, message])
        # await asyncio.sleep(1)

    async def receive_loop(self):
        """
        This is the receive loop for pangu messages.

        This method may be overwritten to meet the needs
        of the application before handling received messages.

        """
        while True:
            data = await self.subscriber.recv_multipart()
            payload = await self.unpack(data[1])
            await self.incoming_message_processing(data[0].decode(), payload)
            

    async def start_the_receive_loop(self):
        """

        """
        self.the_task = self.event_loop.create_task(self.receive_loop())

    async def incoming_message_processing(self, topic, payload):
        """
        Override this method with a custom pangu message processor for subscribed messages.

        :param topic: Message Topic string.

        :param payload: Message Data.
        """

        print('this method should be overwritten in the child class', topic, payload, flush=True)

    # noinspection PyUnresolvedReferences
    async def set_subscriber_topic(self, topic):
        """
        This method sets a subscriber topic.

        You can subscribe to multiple topics by calling this method for
        each topic.

        :param topic: A topic string
        """

        if not type(topic) is str:
            raise TypeError('Subscriber topic must be python_pangu string')

        self.subscriber.setsockopt(zmq.SUBSCRIBE, topic.encode())

    async def clean_up(self):
        """
        Clean up before exiting - override if additional cleanup is necessary

        """
        await self.publisher.close()
        await self.subscriber.close()
        await self.my_context.term()
