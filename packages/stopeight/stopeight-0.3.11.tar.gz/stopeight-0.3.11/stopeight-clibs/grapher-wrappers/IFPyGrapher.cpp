// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1
#include "git.h"
#include <stopeight-clibs/shared_types.h>
#include <stopeight-clibs/grapher.h>
#include <stopeight-clibs/algo.h>
#include <stopeight-clibs/angle_functions.h>
#include <stopeight-clibs/Matrix.h>

#undef NDEBUG
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

using namespace pybind11;

PYBIND11_MODULE(grapher, m){
	if(GitMetadata::Populated()) {
		object sha;
	        if(GitMetadata::AnyUncommittedChanges()) {
			sha = cast(GitMetadata::CommitSHA1()+"+dirty");
	        } else {
			sha = cast(GitMetadata::CommitSHA1());
		}
		m.attr("version") = sha;
	}
	object matrix_module = module::import("stopeight.matrix");
//redefinition
//todo link to matrix python module
//    PYBIND11_NUMPY_DTYPE(sp::timecode<double>,coords,type,tct_type,cov_type);
    class_<std::vector<double>>(m,"VectorDouble",buffer_protocol())
	.def(init<>())
	.def(init([](array_t<double,array::c_style> buffer){
		auto info = buffer.request();
		if (info.format != format_descriptor<double>::format())
			throw std::runtime_error("Incompatible format: Expected a double array format descriptor");
		if (info.itemsize != sizeof(double))
			throw std::runtime_error("Incompatible format: Expected double size items");
		if (info.ndim!= 1)
			throw std::runtime_error("Incompatible buffer dimensions");
		auto data = static_cast<double*>(info.ptr);
		auto vector =  new std::vector<double>(data,data+info.shape[0]);
		return vector;
	}))
	.def_buffer([](std::vector<double>& vector) -> buffer_info{
		return buffer_info(
			vector.data(),
			sizeof(double),
			format_descriptor<double>::format(),
			1,
			{size_t(vector.size())},
			{sizeof(double)}
		);
		})
	.def("create_vector_graph", [](std::vector<double>& vec, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->Vectors<std::vector<sp::timecode<double>>>{
		auto op = speczilla::Buffer<double>(&vec,vec.size(),samplesPerVector,unitaryLength,relative,average,averageScale);
		return op();//is sp::result, not std::vector<timecode>
    },arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0);
	/* .def("create_vector_graph", [](std::vector<double>& vec, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->std::vector<sp::timecode<double>>{
		//same code as grapher, except:
		//PreloaderIF or Destructor -> stack smash?
		using T = double;
		std::vector<T>* buf(&vec);
        T vectorLength = grapher::samples_To_VG_vectorLength(buf->size(), unitaryLength);
		auto output = std::vector<sp::timecode<T>>{};
		if (buf->size() > 2) {
			std::vector<T> differences = std::vector<T>(buf->size(), 0.0);
			grapher::__differences(std::begin(*buf), std::end(*buf), std::begin(differences));

			//in general if uneven, middle is on left side
			//-1 differences, -1 size
			auto dvg = (grapher::__differences_To_VG<T>(samplesPerVector, vectorLength, std::vector<size_t>(1, (((vec.size() - 1) / 2) - 1))));
			if (relative) {
				angle::relative afunc = angle::relative(std::begin(differences) + 1, std::end(differences),average,averageScale);
				output = dvg(differences, afunc);//((vectorSize * 2) + add);
			}
			else {
				//propagation means not par_unseq? introduce class for angle?
				angle::independent afunc = angle::independent(std::begin(differences) + 1, std::end(differences),average,averageScale);
				output = dvg(differences, afunc);//((vectorSize * 2) + add);
			}
		}
		return output;
	},arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0)*/
	;
	m.def("create_vector_graph", [](std::vector<double>& vec, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->array_t<sp::timecode<double>,array::c_style>{
		auto op = speczilla::Buffer<double>(&vec,vec.size(),samplesPerVector,unitaryLength,relative,average,averageScale);
		Vectors<std::vector<sp::timecode<double>>> result = Vectors<std::vector<sp::timecode<double>>>{std::move(op())};
		return cast(result);//is sp::result, not std::vector<timecode>
	},arg("vector"),arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0);
	//this works!!
	/*m.def("create_vector_graph", [](array_t<double,array::c_style> buffer, int samplesPerVector, double unitaryLength, bool relative , double average, double averageScale)->Vectors<std::vector<sp::timecode<double>>>{
		auto info = buffer.request();
		if (info.format != format_descriptor<double>::format())
			throw std::runtime_error("Incompatible format: Expected a double array format descriptor");
		if (info.itemsize != sizeof(double))
			throw std::runtime_error("Incompatible format: Expected double size items");
		if (info.ndim!= 1)
			throw std::runtime_error("Incompatible buffer dimensions");
		auto data = static_cast<double*>(info.ptr);
		auto vector = std::vector<double>(data,data+info.shape[0]);
		auto op = speczilla::Buffer<double>(&vector,vector.size(),samplesPerVector,unitaryLength,relative,average,averageScale);
		return Vectors<std::vector<sp::timecode<double>>>{op()};//is sp::result, not std::vector<timecode>
    },arg("vector"),arg("samplesPerVector")=1,arg("unitaryLength")=1.0,arg("relative")=false,arg("average")=0.0,arg("averageScale")=1.0);*/

	//basically the same as Vector, but not requiring matrix.h
    /*class_<std::vector<sp::timecode<double>>>(m,"VectorTimeCodeDouble",buffer_protocol())
	.def(init<>())
	// .def(init([](array_t<sp::timecode<double>,array::c_style> buffer){
	// 	auto info = buffer.request();
	// 	// There is an existing bug in NumPy (as of v1.11): trailing bytes are
    // 	// not encoded explicitly into the format string. This will supposedly
	// 	// get fixed in v1.12; for further details, see these:
	// 	// - https://github.com/numpy/numpy/issues/7797
	// 	// - https://github.com/numpy/numpy/pull/7798
	// 	// Because of this, we won't use numpy's logic to generate buffer format
	// 	// strings and will just do it ourselves.
	// 	if (info.format != format_descriptor<sp::timecode<double>>::format()){
	// 		throw std::runtime_error("Incompatible format: Expected a timecode array format descriptor");
	// 		}
	// 	if (info.itemsize != sizeof(sp::timecode<double>))
	// 		throw std::runtime_error("Incompatible format: Expected timecode size items");
	// 	if (info.ndim!= 1)
	// 		throw std::runtime_error("Incompatible buffer dimensions");
	// 	size_t size = info.shape[0];
	// 	if (info.strides[0]!=sizeof(sp::timecode<double>))
	// 		throw std::runtime_error("Incompatible format: Incompatible step size");
	// 	auto data = static_cast<sp::timecode<double>*>(info.ptr);
	// 	auto vector = new std::vector<sp::timecode<double>>(data,data+size);
	// 	return vector;
	// }))
	.def_buffer([](std::vector<sp::timecode<double>>& vector) -> buffer_info{
		return buffer_info(
			vector.data(),
			sizeof(sp::timecode<double>),
			format_descriptor<sp::timecode<double>>::format(),
			1,
			{size_t(vector.size())},
			{sizeof(sp::timecode<double>)}
		);
		})
	.def("__array__",[](std::vector<sp::timecode<double>> &vec)->array_t<sp::timecode<double>,array::c_style>{return cast(vec);})
	;*/

//    class_<samples_To_VG<double>>(m,"Samples_To_VG")
//            .def(init<size_t,double,std::vector<size_t>>())//needs std::vector<size_t> type
////            .def("exec",overload_cast<fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&>(&samples_To_VG::operator()<fexec,vector_single<double>,vector_pair<double>,angle::angle>))
////            .def("exec",overload_cast<fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&>(&samples_To_VG::operator()))
////            .def("exec",(void (samples_To_VG::*)(fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&)) &samples_To_VG::operator()<fexec,vector_single<double>,vector_pair<double>,angle::angle> )
////            .def("exec",(void (samples_To_VG::*)(fexec&, vector_single<double>,vector_single<double>,vector_pair<double>,angle::angle&)) &samples_To_VG::operator() )
//            .def("exec", &samples_To_VG<double>::operator()<angle::sharing_angle&>)//return type needs definition of sp::result!!!
//            ;

}
