import pravega_client
import json
import math
import os
import requests
import time
import unittest


class PravegaProducer(unittest.TestCase):
    def __init__(self, controller_url):
        super(PravegaProducer, self).__init__()
        self.controller_url = controller_url
        self.stream_manager = None
        self.writer = None

    def create_manager(self):
        self.stream_manager = pravega_client.StreamManager(self.controller_url)

    def create_scope(self, scope_name):
        scope_result = self.stream_manager.create_scope(scope_name)
        print("Scope Creation Status: ", scope_result)
        self.assertEqual(True, scope_result, "Scope creation status")

    def create_stream(self, scope_name, stream_name, segment_num=1):
        stream_result = self.stream_manager.create_stream(scope_name, stream_name, segment_num)
        print("Stream Creation Status: ", stream_result)
        self.assertEqual(True, stream_result, "Stream creation status")

    def create_writer(self, scope_name, stream_name):
        self.writer = self.stream_manager.create_writer(scope_name, stream_name)


def main():
    controller_url = "tcp://localhost:9090"

    producer = PravegaProducer(controller_url)
    producer.create_manager()

    scope_exist = True
    # scope_name = "scopeTwitter"
    # stream_name = "streamTwitter"
    scope_name = "my-scope"
    stream_name = "my-stream"
    if not scope_exist:
        producer.create_scope(scope_name)
        producer.create_stream(scope_name, stream_name)

    producer.create_writer(scope_name, stream_name)

    tmp = {'data': {'author_id': '1453669322568646665', 'id': '1478508261934567424', 'text': 'RT @DieBroodtGuy: In Belgium we don\'t say "surprise visit" we say "kwas in de buurt dus ik dacht kspring efkes binnen".'}, 'includes': {'users': [{'id': '1453669322568646665', 'name': 'Tess-toss der’on', 'username': 'vleugjeman'}, {'id': '1193621118722232321', 'name': '𝕯𝖗𝖆𝖌𝖔𝖓 𝕮𝖔𝖗𝖓𝖊𝖙𝖙𝖔', 'username': 'DieBroodtGuy'}]}}

    tmp = str(tmp)
    producer.writer.write_event(tmp)
    producer.writer.flush()



if __name__ == "__main__":
    main()
