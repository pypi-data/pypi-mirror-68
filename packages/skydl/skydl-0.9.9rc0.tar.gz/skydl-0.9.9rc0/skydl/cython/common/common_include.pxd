from libcpp.string cimport string
from libcpp cimport bool as bool_t
# cdef extern from "<iostream>" namespace "std" nogil:
#     pass

# 需要引用cc内容(这是早期版本cython头文件的机制)
cdef extern from "../../../../src/skydl/cython_extends/common/global_info.cc" nogil:
    pass

cdef extern from "../../../../src/skydl/utils/version.cc" nogil:
    pass

cdef extern from "../../../../src/skydl/cython_extends/common/timer_util.cc" nogil:
    pass


# Decalre the class with cdef
cdef extern from "../../../../src/skydl/cython_extends/common/global_info.h" namespace "skydl::cython" nogil:
    cdef cppclass GlobalInfo:
        GlobalInfo() except +
        string getVersion()

cdef extern from "../../../../src/skydl/cython_extends/common/timer_util.h" namespace "skydl::cython" nogil:
    cdef cppclass TimerUtil:
        TimerUtil() except +
        TimerUtil(string, bool_t, string) except +
        void setTaskName(string)
        void setEnablePrint(bool_t)
        void setTimeUnit(string) # seconds,milliseconds,microseconds,nanoseconds,picoseconds
        void clear_and_start_timing()
        double stop_and_accumulate_timing()
        @staticmethod
        void sleep(int, string)

