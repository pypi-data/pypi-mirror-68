// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef MEAN_H
#define MEAN_H

#include <vector>

// mean.h is compiled by msvc, mean_impl.h is compiled by llvm4
// Hide everything SYCL
// For hiding and dual implementation, NAME MUST BE THE SAME
// AND NO IMPLEMENTATIONS IN HERE

#include "shared_types.h"

#include "preloaderif.h"

namespace speczilla {

	template<typename T>class Mean : public PreloaderIF<T, double>
	{
	public:
		Mean<T>(std::vector<T>* s);

		~Mean<T>();

		double operator()();


	private:
		//needs to be there to avoid crt error
		//hack: length of pointer on amd_win10_64
		//doesnt work; crash when remove in debug from presonus
		char buf[6];//sizeofPTR
	};
}
#endif
