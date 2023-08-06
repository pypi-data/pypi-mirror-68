# cython: profile=False
# distutils: language=c++
# cython: embedsignature=True
# cython: language_level=3
# cython: c_string_type=unicode, c_string_encoding=utf8
#-----------------------------------------------------------------------------
# Copyright (c) 2020, Allen B. Riddell
#-----------------------------------------------------------------------------
from cpython.version cimport PY_MAJOR_VERSION
# from skydl.cython.examples.demo.cdemo cimport CythonCallDemo
include "./cdemo_include.pxd"

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef unicode _text(s):
    if type(s) is unicode:
        return <unicode>s
    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
            return (<bytes>s).decode('ascii')
    elif isinstance(s, unicode):
        return unicode(s)
    else:
        raise TypeError("Could not convert to unicode.")

cdef string _string(s) except *:
    cdef string c_str = _text(s).encode("utf-8")
    return c_str

cdef class PyCythonDemo:
    cdef CythonCallDemo c_mydemo  # Hold a C++ instance which we're wrapping
    def __cinit__(self, value):
        self.c_mydemo = CythonCallDemo(value)

    def __dealloc__(self):
        # del self.c_mydemo
        print("PyCythonDemo#__dealloc__ called!!!")
        # if self.c_mydemo != NULL:
        #     del self.c_mydemo
        #     self.info(f"PyCythonDemo#__dealloc__()...deleted c_mydemo, del之后self.c_mydemo={self.c_mydemo}")
        #     self.c_mydemo = NULL
        # else:
        #     print("PyCythonDemo#__dealloc__()...c_mydemo本来就为null不需要delete!")

    def mul(self, m):
        return self.c_mydemo.mul(m)

    def add(self, b, c):
        return self.c_mydemo.add(b, c)

    def sayHello(self, name):
        self.c_mydemo.sayHello(name)

    def sayHelloWithStr(self, name)->string:
        print(f"cdef sayHelloWithStr#name={_string(name)}")
        return self.c_mydemo.sayHelloWithStr(name)

    def countdown(self, count):
        self.c_mydemo.countdown(count)


