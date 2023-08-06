# -*- coding: utf-8 -*-
from dataclasses import dataclass
from skydl.ray.streaming_0_8_2.python.config import Config


def register_custom_serializer(cls):
    import ray
    import cloudpickle

    def custom_serializer(obj):
        return cloudpickle.dumps(obj)

    def custom_deserializer(serialized_obj):
        return cloudpickle.loads(serialized_obj)

    return ray.register_custom_serializer(cls, custom_serializer, custom_deserializer)


class DefaultStreamingEnvConfigV082(object):
    """
    default ray streaming env config for ray streaming V0.8.2
    """
    def __init__(self, parallelism=1, channel="native"):
        self.parallelism = parallelism
        self.channel_type = Config.NATIVE_CHANNEL if channel == "native" else Config.MEMORY_CHANNEL


class DefaultStreamingSource(object):
    """default streaming source implement"""
    def get_next(self):
        # get current record
        return None


@dataclass
class StreamingRecord(object):
    """
    A class used to streaming transformer
    """
    status: str  # "ok|fail"
    type: str   # "data|error"
    data: object  # e.g. [12.1, 13.3, 11.00, 12.34]


if __name__ == '__main__':
   obj = StreamingRecord("ok", "data", [12.1, 13.3, 11.00, 12.34])
   print(f"obj={obj}, obj.type={obj.type}")

