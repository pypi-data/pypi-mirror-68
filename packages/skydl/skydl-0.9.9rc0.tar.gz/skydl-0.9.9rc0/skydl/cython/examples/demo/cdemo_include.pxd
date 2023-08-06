cdef extern from "string" namespace "std" nogil:
    cdef cppclass string:
        char* c_str()
# from libcpp.string cimport string

# 需要引用cc内容(这是早期版本cython头文件的机制)
cdef extern from "../../../../../src/skydl/cython_extends/examples/demo/demo.cc" nogil:
    pass

# Decalre the class with cdef
cdef extern from "../../../../../src/skydl/cython_extends/examples/demo/demo.h" namespace "skydl::cython" nogil:
    cdef cppclass CythonCallDemo:
        CythonCallDemo() except +
        CythonCallDemo(int) except +
        int a
        str get_ustrings()
        int mul(int)
        int add(int, int)
        void countdown(int)
        void sayHello(char*)
        string sayHelloWithStr(string &str)
