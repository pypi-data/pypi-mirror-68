// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef MEAN_H
#define MEAN_H

#include <vector>

#include <stopeight-clibs/shared_types.h>

#include <stopeight-clibs/preloaderif.h>

namespace speczilla {

	template<typename T>class Mean : public PreloaderIF<T, double>
	{
	public:
		Mean<T>(std::vector<T>* s);

		~Mean<T>();

		double operator()();


	private:
		std::vector<T>* buf;
	};
}
#endif
