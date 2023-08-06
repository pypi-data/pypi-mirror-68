# cython: profile=False
# distutils: language=c++
# cython: embedsignature=True
# cython: language_level=3
# cython: c_string_type=unicode, c_string_encoding=utf8
#-----------------------------------------------------------------------------
# Copyright (c) 2020, Allen B. Riddell
#-----------------------------------------------------------------------------
include "./common_include.pxd"

cdef class PyCommon:
    cdef GlobalInfo c_global_info
    def __cinit__(self):
        self.c_global_info = GlobalInfo()

    def __dealloc__(self):
        # del self.c_global_info
        pass

    def get_version(self)->string:
        return self.c_global_info.getVersion()


cdef class PyTimerUtil:
    cdef TimerUtil* c_timer_util
    def __cinit__(self, task_name="", enable_print=True, time_unit="milliseconds"):
        self.c_timer_util = new TimerUtil(task_name, enable_print, time_unit)

    def __dealloc__(self):
        if self.c_timer_util != NULL:
            del self.c_timer_util
            self.c_timer_util = NULL
        # print("PyTimerUtil#__dealloc__触发了。。。")

    def start_timer(self):
        self.c_timer_util.clear_and_start_timing()

    def stop_timer(self)->double:
        return self.c_timer_util.stop_and_accumulate_timing()

    @staticmethod
    def sleep(time, unit="milliseconds"):
        return TimerUtil.sleep(time, unit)


