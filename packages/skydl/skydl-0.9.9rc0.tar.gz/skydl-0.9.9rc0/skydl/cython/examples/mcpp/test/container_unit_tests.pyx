# cython: profile=False
# distutils: language=c++
# cython: embedsignature=True
# cython: language_level=3
# cython: c_string_type=unicode, c_string_encoding=utf8
#-----------------------------------------------------------------------------
# Copyright (c) 2020, Allen B. Riddell
#-----------------------------------------------------------------------------
from skydl.cython.examples.mcpp.container cimport *
from libcpp.memory cimport unique_ptr
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp.pair cimport pair
from libcpp.list cimport list
from libcpp.deque cimport deque
from cython.operator cimport dereference as deref

def run_emplace_object_move_vector():
    cdef vector[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](2,4))
    emplace_object_move(v,i)
    return {'size':v.size(),'first':deref(v[0]).first,'second':deref(v[0]).second}

def run_emplace_object_pos_move_vector():
    cdef vector[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](6,7))
    emplace_object_move(v,i)
    i.reset(new pair[int,int](2,4))
    #Cython will not allow a simple
    #assignment to p. We must
    #name a cdef type
    cdef vector[unique_ptr[pair[int,int]]].iterator p = emplace_object_pos_move(v,v.begin(),i)
    return {'size':v.size(),'first':deref(p).get().first,'second':deref(p).get().second}

def run_push_back_move_vector():
    cdef vector[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](2,4))
    push_back_move(v,i)
    return {'size':v.size(),'first':deref(v[0]).first,'second':deref(v[0]).second}

def run_push_front_move_list():
    cdef list[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](2,4))
    push_front_move(v,i)
    b = v.begin()
    return {'size':v.size(),'first':deref(b).get().first,'second':deref(b).get().second}

def run_push_front_move_deque():
    cdef deque[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](2,4))
    push_front_move(v,i)
    return {'size':v.size(),'first':deref(v[0]).first,'second':deref(v[0]).second}

def run_emplace_object_move_map():
    cdef map[unsigned,unique_ptr[pair[int,int]]] c
    cdef pair[int,unique_ptr[pair[int,int]]] i
    i.first=1
    i.second.reset(new pair[int,int](2,4))
    emplace_object_move(c,i)
    x = c.begin()
    return {'size':c.size(),
            'first':deref(x).second.get().first,
            'second':deref(x).second.get().second}

def run_emplace_vector():
    cdef vector[pair[int,int]] v
    emplace(v,2,4)
    return {'size':v.size(),'first':v[0].first,'second':v[0].second}

def run_emplace_vector_unique_ptr():
    cdef vector[unique_ptr[pair[int,int]]] v
    #Here, we use the constructor unique_ptr<T>(T *).
    #For this case, Cython needs us to typecast so that
    #the second template type is correctly deduced.
    emplace(v,<pair[int,int]*>new pair[int,int](2,4))
    return {'size':v.size(),'first':deref(v[0]).first,'second':deref(v[0]).second}

def run_emplace_pos_move_vector_unique_ptr():
    cdef vector[unique_ptr[pair[int,int]]] v
    emplace_pos_move(v,v.end(),<pair[int,int]*>new pair[int,int](6,7))
    #Cython will not allow a simple
    #assignment to p. We must
    #name a cdef type
    cdef vector[unique_ptr[pair[int,int]]].iterator p
    p = emplace_pos_move(v,v.begin(),<pair[int,int]*>new pair[int,int](2,4))
    return {'size':v.size(),'first':deref(p).get().first,'second':deref(p).get().second}

def run_emplace_pos_move_vector_unique_ptr2():
    cdef vector[unique_ptr[pair[int,int]]] v
    cdef unique_ptr[pair[int,int]] i
    i.reset(new pair[int,int](6,7))
    #Here, we cast the type to "reference to unique_ptr",
    #which makes this call compatible w/above def'n
    emplace_pos_move(v,v.end(),<unique_ptr[pair[int,int]]&>i)
    #Cython will not allow a simple
    #assignment to p. We must
    #name a cdef type
    i.reset(new pair[int,int](2,4))
    cdef vector[unique_ptr[pair[int,int]]].iterator p
    p = emplace_pos_move(v,v.begin(),<unique_ptr[pair[int,int]]&>i)
    return {'size':v.size(),'first':deref(p).get().first,'second':deref(p).get().second}

def run_emplace_move_vector():
    cdef vector[pair[int,int]] v
    emplace_move(v,2,4)
    return {'size':v.size(),'first':v[0].first,'second':v[0].second}

