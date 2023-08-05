"""
pangu_base.py

 Copyright (c) 2016-2019 Alan Yorinks All right reserved.

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

# Use argparse and signal if you wish to implement the argparse
# code located at the bottom of this file.

# import argparse
# import signal
# import sys

import socket
import time
import msgpack
import zmq
import psutil


class PanguBase(object):
    """

    This is the base class for all Python Pangu components,
    encapsulating and acting as an abstraction layer for zeromq and message pack
    functionality.

    Pangu components are derived by inheriting from this class and
    overriding its methods as necessary.

    Pangu components have the capability to both publish and subscribe to user
    defined messages using the Pangu backplane.

    To import into  the derived class use:

           from python_pangu.pangu_base import PanguBase

    """

    def __init__(self, back_plane_ip_address=None, subscriber_port='16103',
                 publisher_port='16130', process_name='None', loop_time=.1,
                 external_message_processor=None, receive_loop_idle_addition=None,
                 connect_time=0.3):
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

        :param loop_time: Receive loop sleep time.

        :param external_message_processor: external method to process messages

        :param receive_loop_idle_addition: an external method called in the idle section
                                           of the receive loop

        :param connect_time: a short delay to allow the component to connect to the Backplane
        """

        # call to super allows this class to be used in multiple inheritance scenarios when needed
        super(PanguBase, self).__init__()

        if not hasattr(self, 'TOPIC'):
            self.TOPIC = ADAPTER_TOPIC  # message topic: the message from adapter
        if not hasattr(self, 'EXTENSION_ID'):
            self.EXTENSION_ID = "eim"

        self.external_message_processor = external_message_processor
        self.receive_loop_idle_addition = receive_loop_idle_addition
        self.connect_time = connect_time

        self.back_plane_ip_address = '127.0.0.1'

        self.subscriber_port = subscriber_port
        self.publisher_port = publisher_port

        self.loop_time = loop_time

        print('\n************************************************************')
        print(process_name + ' using Back Plane IP address: ' + self.back_plane_ip_address)
        print('Subscriber Port = ' + self.subscriber_port)
        print('Publisher  Port = ' + self.publisher_port)
        print('Loop Time = ' + str(loop_time) + ' seconds')
        print('************************************************************')

        # establish the zeromq sub and pub sockets and connect to the backplane
        self.my_context = zmq.Context()
        self.subscriber = self.my_context.socket(zmq.SUB)
        connect_string = "tcp://" + self.back_plane_ip_address + ':' + self.subscriber_port
        self.subscriber.connect(connect_string)

        self.publisher = self.my_context.socket(zmq.PUB)
        connect_string = "tcp://" + self.back_plane_ip_address + ':' + self.publisher_port
        self.publisher.connect(connect_string)

        # Allow enough time for the TCP connection to the Backplane complete.
        time.sleep(self.connect_time)

    def set_subscriber_topic(self, topic):
        """
        This method sets a subscriber topic.

        You can subscribe to multiple topics by calling this method for
        each topic.

        :param topic: A topic string
        """

        if not type(topic) is str:
            raise TypeError('Subscriber topic must be python_pangu string')

        self.subscriber.setsockopt(zmq.SUBSCRIBE, topic.encode())

    def publish_payload(self, payload, topic=''):
        """
        This method will publish a python_pangu payload and its associated topic

        :param payload: Protocol message to be published

        :param topic: A string value
        """

        # make sure the topic is a string
        if not type(topic) is str:
            raise TypeError('Publish topic must be python_pangu string', 'topic')

        # create python_Pangu message pack payload
        message = msgpack.packb(payload, use_bin_type=True)

        pub_envelope = topic.encode()
        self.publisher.send_multipart([pub_envelope, message])

    def receive_loop(self):
        """
        This is the receive loop for Pangu messages.

        This method may be overwritten to meet the needs
        of the application before handling received messages.

        """
        while True:
            try:
                data = self.subscriber.recv_multipart(zmq.NOBLOCK)
                self.incoming_message_processing(data[0].decode(), msgpack.unpackb(data[1], raw=False))
            # if no messages are available, zmq throws this exception
            except zmq.error.Again:
                try:
                    if self.receive_loop_idle_addition:
                        self.receive_loop_idle_addition()
                    time.sleep(self.loop_time)
                except KeyboardInterrupt:
                    self.clean_up()
                    raise KeyboardInterrupt

    def incoming_message_processing(self, topic, payload):
        """
        Override this method with a custom Pangu message processor for subscribed messages.

        :param topic: Message Topic string.

        :param payload: Message Data.
        """
        if self.external_message_processor:
            self.external_message_processor(topic, payload)
        else:
            print('this method should be overwritten in the child class', topic, payload)

    def clean_up(self):
        """
        Clean up before exiting - override if additional cleanup is necessary

        """
        self.publisher.close()
        self.subscriber.close()
        self.my_context.term()
