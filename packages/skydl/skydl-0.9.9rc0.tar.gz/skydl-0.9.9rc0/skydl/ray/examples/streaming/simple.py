# -*- coding: utf-8 -*-
import logging
import time
import ray
from skydl.ray.streaming_0_8_2.python.operator import OpType, PStrategy
from skydl.ray.ray_streaming_util import StreamingRecord, DefaultStreamingSource, DefaultStreamingEnvConfigV082
from skydl.ray.streaming_0_8_2.python.streaming import Environment
from skydl.common.date_utils import DateUtils
from skydl.ray.ray_streaming_util import register_custom_serializer

# define logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def splitter(line):
    # return line.split()
    return line + "-by-splitter"


def filter_fn(word):
    if "f" in word:
        return True
    return False


if __name__ == "__main__":
    ray.init(local_mode=False)
    register_custom_serializer(StreamingRecord)
    register_custom_serializer(OpType)
    register_custom_serializer(PStrategy)
    env = Environment(DefaultStreamingEnvConfigV082(background_flush=True,
                                                prefetch_depth=10))

    def attribute_selector(tuple):
        return tuple[1]

    def key_selector(tuple):
        return tuple[0]

    class CustormSource(DefaultStreamingSource):
        def __init__(self):
            self._count = 0

        def get_next(self):
            self._count += 1
            time.sleep(1*self._count)
            now_str = DateUtils.now_to_str()
            print(f"CustormSource#get_next...{now_str}, count={self._count}")
            if self._count % 20 == 0:
                # print("***get_next_nvl***:" + str(self._count))
                return StreamingRecord("ok", "data", str(self._count) + "-uuunited\nStates-" + now_str)
            else:
                return StreamingRecord("ok", "data", str(self._count) + "-United States-" + now_str)

    def map_fn(record):
        print(f"simple map_fn={record}")
        time.sleep(30)
        return record

    def inspect_log(record):
        print(f"inspect#record.type={record.type}")
        time.sleep(20)
        logger.info(record.data + ",finished:" + DateUtils.now_to_str())
        return record

    stream = env.source(
                CustormSource()
            ).round_robin(
            ).map(
                map_fn=map_fn,
                name="simple_map"
            ).inspect(
                inspect_log
            )
    # stream = env.read_text_file(args.input_file) \
    #             .shuffle() \
    #             .flat_map(splitter) \
    #             .set_parallelism(2) \
    #             .key_by(key_selector) \
    #             .sum(attribute_selector) \
    #             .inspect(print)  # Prints the contents of the
    start = time.time()
    env_handle = env.execute()
    ray.get(env_handle)
    end = time.time()
    logger.info("Elapsed time: {} secs".format(end - start))
    logger.info("Output stream id: {}".format(stream.id))
    print("end!")
