import pravega_client
import json
import math
import os
import requests
import time
import unittest

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>ß'
bearer_token = os.environ.get("BEARER_TOKEN")
# By default Pravega Controller is listening at localhost:9090
controller_url = "tcp://localhost:9090"
topic = "Twitter_streaming"
multiple_time = 200
# topic = "debug"
print(bearer_token)

class TwitterStream():
    def __init__(self):
        self.url = "https://api.twitter.com/2/tweets/sample/stream?expansions=author_id"

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2SampledStreamPython"
        return r

    def save_json_resp(self, json_str, f):
        f.write((json.dumps(json_str, indent=4, sort_keys=True))+'\n')
        return

    def connect_to_endpoint(self, f, pravega_producer=None, num_to_get=None, debug=True):
        response = requests.request("GET", self.url, auth=self.bearer_oauth, stream=True)
        print(response.status_code)
        msg_cnt = 0
        msg_all = 0
        time_log = TimeLog()

        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                if debug:
                    pass
                    # print(json.dumps(json_response, indent=4, sort_keys=True))

                self.save_json_resp(json_response, f)

                if pravega_producer:
                    print(json_response)
                    print(type(json_response))
                    print(str(json_response))
                    t = str(json_response)
                    print(type(t))
                    # for i in range(0, multiple_time):
                    # pravega_producer.writer.write_event(json_response)
                    pravega_producer.writer.write_event(t)

                msg_cnt += 1
                if num_to_get != None and msg_cnt >= num_to_get:
                    msg_all += msg_cnt
                    print("Current Batch:{}".format(msg_cnt * multiple_time))
                    print("From Start:{:.2f} Seconds".format(time_log.from_start()))
                    print("Since Last Time: {:.2f} Seconds".format(time_log.from_last()))
                    print("Current Twitter API Speed: {} Tweets/Second".format(
                            math.floor(msg_cnt * multiple_time / time_log.from_last())))
                    print("Average Twitter API Speed: {} Tweets/Second".format(
                            math.floor(msg_all * multiple_time / time_log.from_start())))
                    time_log.lap()
                    print("___________________Next Batch___________________")
                    # kafka_producer.flush()
                    msg_cnt = 0
                    # time.sleep(5)
                    # break
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

class TimeLog():
    def __init__(self):
        self.start_time = time.time()
        self.last_time = time.time()

    def from_start(self):
        current_time = time.time()
        # return diff time, unit seconds
        return current_time - self.start_time

    def from_last(self):
        current_time = time.time()
        res = current_time - self.last_time
        return res

    def lap(self):
        self.last_time = time.time()
        return


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
        self.asssertEqual(True, stream_result, "Stream creation status")

    def create_writer(self, scope_name, stream_name):
        self.writer = self.stream_manager.create_writer(scope_name, stream_name)


def main():
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

    producer.writer.write_event("TEST")

    twitter_stream = TwitterStream()
    f = open('tmp_data_folder/sampled_data_save_t1.txt', 'w')
    twitter_stream.connect_to_endpoint(f, producer, num_to_get=20)


if __name__ == "__main__":
    main()
