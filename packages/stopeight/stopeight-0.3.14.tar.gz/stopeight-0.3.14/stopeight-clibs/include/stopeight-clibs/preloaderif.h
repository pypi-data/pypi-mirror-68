// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef PRELOADERIF_H
#define PRELOADERIF_H

//#include <memory>
#include <vector>

namespace speczilla {

	template<typename T,typename ReturnType>class PreloaderIF
	{
	public:
		//makes implementation!!
		//PreloaderIF<T>();
		//PreloaderIF<T, ReturnType>(std::vector<T>* s);
		//pybind11: *** stack smashing detected ***: <unknown> terminated
		//virtual ~PreloaderIF<T, ReturnType>() {};

		//pybind11: *** stack smashing detected ***: <unknown> terminated
		//virtual ReturnType operator()() =0;
	};
}

#endif
