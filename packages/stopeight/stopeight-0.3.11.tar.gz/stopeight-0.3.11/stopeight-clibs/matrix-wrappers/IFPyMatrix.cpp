// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1
#include "git.h"
#include <stopeight-clibs/Matrix.h>
#include <stopeight-clibs/shared_types.h>

#include <pybind11/pybind11.h>

//For TimeCode, Vectors
#include <pybind11/numpy.h>
//For Stack
#include <pybind11/stl.h>

#undef NDEBUG
#include <iostream>

using namespace pybind11;

PYBIND11_MODULE(matrix, m){
	if(GitMetadata::Populated()) {
		object sha;
	        if(GitMetadata::AnyUncommittedChanges()) {
			sha = cast(GitMetadata::CommitSHA1()+"+dirty");
	        } else {
			sha = cast(GitMetadata::CommitSHA1());
		}
		m.attr("version") = sha;
	}
	enum_<sp::FixpointType>(m,"FixpointType",module_local(false))
		.value("EMPTY",sp::FixpointType::EMPTY)
		.value("FIXPOINT",sp::FixpointType::FIXPOINT);
	enum_<sp::tctype>(m,"tctype",module_local(false))
		.value("EMPTY",sp::tctype::EMPTY)
		.value("SWING",sp::tctype::SWING)
		.value("CREST",sp::tctype::CREST)
		.value("DUNE",sp::tctype::DUNE)
		.value("EDGE",sp::tctype::EDGE)
		.value("LEGALSEGMENT",sp::tctype::LEGALSEGMENT)
		.value("CLIFF",sp::tctype::CLIFF)
		.value("SPIRAL",sp::tctype::SPIRAL)
		//Corner??
		.value("STRAIGHT",sp::tctype::STRAIGHT);
	enum_<sp::covertype>(m,"covertype",module_local(false))
		.value("EMPTY",sp::covertype::EMPTY)
		.value("SWELL",sp::covertype::SWELL)
		.value("SPIRAL",sp::covertype::SPIRAL)
		.value("ZIGZAG",sp::covertype::ZIGZAG);
    PYBIND11_NUMPY_DTYPE(sp::timecode<double>, coords, type, tct_type, cov_type);
	class_<sp::timecode<double>> time_code(m,"TimeCode");
	time_code.def(init([](double x, double y){
		sp::timecode<double> tc{};
		return tc.__init({x,y});
	}))
	.def_readwrite("type", &sp::timecode<double>::type)
	.def_readwrite("tct_type", &sp::timecode<double>::tct_type)
	.def_readwrite("cov_type", &sp::timecode<double>::cov_type);
	
//// enables append, insert, etc. but overwrites init constructors below
//// not possible because it's numpy
//	bind_vector<Vectors<std::vector<sp::timecode<double>>>>(m,"Vectors", buffer_protocol())
    class_<Vectors<std::vector<sp::timecode<double>>>>(m,"Vectors",buffer_protocol())
	.def(init<>())
 	.def(init([](array_t<sp::timecode<double>,array::c_style> buffer){
		auto info = buffer.request();
		// There is an existing bug in NumPy (as of v1.11): trailing bytes are
    	// not encoded explicitly into the format string. This will supposedly
		// get fixed in v1.12; for further details, see these:
		// - https://github.com/numpy/numpy/issues/7797
		// - https://github.com/numpy/numpy/pull/7798
		// Because of this, we won't use numpy's logic to generate buffer format
		// strings and will just do it ourselves.
		//if (info.format != format_descriptor<sp::timecode<double>>::format()){
		//	throw std::runtime_error("Incompatible format: Expected a timecode array format descriptor");
		//	}
		if (info.itemsize != sizeof(sp::timecode<double>))
			throw std::runtime_error("Incompatible format: Expected timecode size items");
		if (info.ndim!= 1)
			throw std::runtime_error("Incompatible buffer dimensions");
		size_t size = info.shape[0];
		if (info.strides[0]!=sizeof(sp::timecode<double>))
			throw std::runtime_error("Incompatible format: Incompatible step size");
		auto data = static_cast<sp::timecode<double>*>(info.ptr);
		auto vector = new Vectors<std::vector<sp::timecode<double>>>(data,data+info.shape[0]);
		return vector;
	}))
 	.def_buffer([](Vectors<std::vector<sp::timecode<double>>>& vectors) -> buffer_info{
	return buffer_info(
		vectors.data(),
		sizeof(sp::timecode<double>),
		format_descriptor<sp::timecode<double>>::format(),
		1,
		{size_t(vectors.size())},
		{sizeof(sp::timecode<double>)}
	);
	})
	.def("ptr",[](Vectors<std::vector<sp::timecode<double>>> &vecs){
		std::cout<<vecs.data();
	}) 
	.def("apply",&Vectors<std::vector<sp::timecode<double>>>::apply)
	.def("__array__",[](Vectors<std::vector<sp::timecode<double>>> &vecs)->array_t<sp::timecode<double>,array::c_style>{return cast(vecs);})
	.def("__iter__", [](Vectors<std::vector<sp::timecode<double>>> &v) {
       return make_iterator(v.begin(), v.end());
    }, keep_alive<0, 1>())
	.def("__len__", [](const Vectors<std::vector<sp::timecode<double>>> &v) { return v.size(); })
	;
	m.def("ptr",[](array_t<sp::timecode<double>,array::c_style> buffer){
		auto info = buffer.request();
		std::cout<<info.ptr;
	});

	class_<Stack<std::vector<sp::timecode<double>>>>(m,"Stack")
	.def(init<>())
	.def("identity",&Stack<std::vector<sp::timecode<double>>>::identity)
	.def("scale",&Stack<std::vector<sp::timecode<double>>>::scale)
	.def("rotate",&Stack<std::vector<sp::timecode<double>>>::rotate)
	.def("translate",&Stack<std::vector<sp::timecode<double>>>::translate)
	;
}
