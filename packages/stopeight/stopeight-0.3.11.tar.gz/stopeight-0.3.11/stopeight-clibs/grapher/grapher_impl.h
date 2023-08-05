// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef GRAPHER_H
#define GRAPHER_H

#include <vector>

#include <stopeight-clibs/shared_types.h>

#include <stopeight-clibs/preloaderif.h>

namespace speczilla {

	template<typename T>class Buffer : public PreloaderIF<T, std::vector<sp::timecode<T>>>
	{
	public:
		Buffer<T>(std::vector<T>* s);
		explicit Buffer<T>(std::vector<T>* s, size_t showSamples, size_t samplesPerVector=1, double unitaryLength = 1, bool relative = false, double average = 0.0f, double angleScale = 1.0f);

		~Buffer<T>();

		std::vector<sp::timecode<T>> operator()();

	private:
		std::vector<T>* buf;
		size_t _samplesPerVector,_showSamples;
		double _unitaryLength;
		bool _relative;
		double _average;
		double _angleScale;
	};
}
#endif
