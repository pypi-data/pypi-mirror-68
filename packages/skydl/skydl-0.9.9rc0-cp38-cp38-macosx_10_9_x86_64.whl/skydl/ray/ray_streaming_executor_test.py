# -*- coding: utf-8 -*-
import ray
import time
import logging
import threading
import argparse
from skydl.common.date_utils import DateUtils
from skydl.ray.streaming_0_8_2.python.operator import OpType, PStrategy
from skydl.ray.streaming_0_8_2.python.streaming import DataStream, Environment
from skydl.ray.ray_ring_buffer import RayRingBuffer
from skydl.ray.ray_streaming_executor import RayStreamingExecutor
from skydl.ray.ray_streaming_util import DefaultStreamingSource, register_custom_serializer, StreamingRecord, \
    DefaultStreamingEnvConfigV082

# define logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RayStreamingExecutorSample(RayStreamingExecutor):
    """
    ray流计算执行器sample
    """
    @property
    def ray_ring_buffer(self):
        return self._ray_ring_buffer

    def __init__(self, args_parser=None):
        super().__init__(args_parser)
        self._ray_ring_buffer = RayRingBuffer(1000)

        def exec_forever():
            try:
                count = 0
                while True:
                    count += 1
                    self.ray_ring_buffer.put(str(count) + "*aaa")
                    time.sleep(4)
            except Exception as e:
                logger.error("error occurred at exec_forever ringbuffer put, %s", str(e))
        put_ring_buffer_thread = threading.Thread(target=exec_forever, args=())
        put_ring_buffer_thread.setDaemon(True)
        put_ring_buffer_thread.start()

    def build_stream(self, env) -> DataStream:
        class RayStreamingSource(DefaultStreamingSource):
            @property
            def global_queue(self):
                return self._global_queue

            @property
            def ringbuffer(self):
                return self._ringbuffer

            def __init__(self, ray_ring_buffer):
                self._count = 0
                self._ringbuffer = ray_ring_buffer

            def get_next(self):
                self._count += 1
                logger.info("source will get something...")
                something = self.ringbuffer.get()
                logger.info("source got something=" + something)
                time.sleep(0.5)
                return StreamingRecord("ok", "data", str(self._count) + "-" + something)

        def splitter_fn(record):
            """convert record to another record list, e.g. [record]"""
            logger.info("splitter: " + record.data)
            return [StreamingRecord("ok", "data", split_str + "-splitter-" + DateUtils.now_to_str()) for split_str in record.data.split("-")]

        def handle_record_fn(record):
            """处理回测的逻辑"""
            logger.info(f"handle_record_fn={record}")
            time.sleep(3)
            logger.info(record.data + ", finished:" + DateUtils.now_to_str())
            return StreamingRecord("ok", "data", 0.999)

        stream = env.source(
            RayStreamingSource(self.ray_ring_buffer)
        ).round_robin(
        ).flat_map(
            splitter_fn
        ).map(
            handle_record_fn
        ).set_parallelism(1)  # 2020-04-11 TODO: 目前V0.8.2只完美支持设置map上游(即flat_map)>=下游的并行度
        return stream


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ready to run server!")
    parser.add_argument("--streaming_parallelism", default=1, type=int, help="ray streaming parallelism")
    args_parser = parser.parse_args()
    ray.init(address="localhost:6379")
    register_custom_serializer(StreamingRecord)
    register_custom_serializer(OpType)
    register_custom_serializer(PStrategy)
    env = Environment(DefaultStreamingEnvConfigV082(parallelism=args_parser.streaming_parallelism))
    stream = RayStreamingExecutorSample(
        args_parser=args_parser
    ).execute(env)
