// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef CONTAINERS_H
#define CONTAINERS_H

#include <vector>
#include "stopeight-clibs/shared_types.h"

namespace stopeight {
	//template<typename T> using bounds = std::pair< typename std::vector<T>::iterator, typename std::vector<T>::iterator >;
	//has to be sequential, random access to avoid copy
	template<typename DataType, typename bounds = std::pair< typename std::vector<DataType>::iterator, typename std::vector<DataType>::iterator >>//same as it_pair shared_types
	//enable_if check for contiguous allocation, ie. std::vector::iterator
	class blocks : public std::vector<bounds> {
	public:
		explicit blocks(bounds vec, const size_t seg_size = 1);

		static size_t calculateSize(size_t vec_size, size_t seg_size);
		

	private:
		static size_t mySize(const bounds vec, size_t seg_size);
		//needed in initializer
		static size_t endFull(size_t vec_size, size_t seg_size);
		//static int addedFixPoints(const bounds<DataType> vec);
		bounds _vec;
		size_t _seg_size;
	};
}
#endif
