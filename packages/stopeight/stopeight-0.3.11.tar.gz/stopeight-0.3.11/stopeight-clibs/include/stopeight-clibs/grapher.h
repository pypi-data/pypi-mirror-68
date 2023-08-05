// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef GRAPHER_H
#define GRAPHER_H

#include <vector>

// grapher.h is compiled by msvc, grapher_impl.h is compiled by llvm4
// Hide everything SYCL
// For hiding and dual implementation, NAME MUST BE THE SAME
// AND NO IMPLEMENTATIONS IN HERE

#include "shared_types.h"

#include "preloaderif.h"

namespace speczilla {

	template<typename T>class Buffer : public PreloaderIF<T, std::vector<sp::timecode<T>>>
	{
	public:
		Buffer<T>(std::vector<T>* s);
		explicit Buffer<T>(std::vector<T>* s, size_t showSamples, size_t samplesPerVector = 1, double unitaryLength = 1, bool relative = false, double average = 0.0f, double angleScale = 1.0f);

		~Buffer<T>();

		std::vector<sp::timecode<T>> operator()();

	private:
		//needs to be there to avoid crt error
		//hack: length of pointer on amd_win10_64
		//doesnt work; crash when remove in debug from presonus
		char buf[6];//sizeofPTR
		char _samplesPerVector[sizeof(size_t)], _showSamples[sizeof(size_t)];
		char _unitaryLength[sizeof(double)];
		bool _relative;
		char _average[sizeof(double)];
		char _angleScale[sizeof(double)];
	};
}
#endif
