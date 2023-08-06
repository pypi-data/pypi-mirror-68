#include <pybind11/pybind11.h>
#include "skydl/pybind11_extends/examples/demo/demo.cc"
namespace py = skydl::pybind11;

PYBIND11_MODULE(cdemo, m) {
    // optional module docstring
    m.doc() = "pybind11 example plugin";

    // define add function
    m.def("add", &py::add, "A function which adds two numbers");

    // bindings to Pet class
    pybind11::class_<py::Pet>(m, "Pet")
        .def(pybind11::init<const std::string &, int>())
        .def("go_for_a_walk", &py::Pet::go_for_a_walk)
        .def("get_hunger", &py::Pet::get_hunger)
        .def("get_name", &py::Pet::get_name);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}