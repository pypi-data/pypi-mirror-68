// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#include "containers.h"

#include <stdint.h>

namespace stopeight {

	template<typename DataType, typename bounds> blocks<DataType,bounds>::blocks(bounds vec, const size_t seg_size)
			: std::vector<bounds>(mySize(vec,seg_size))
			, _vec{ vec }
			, _seg_size(seg_size)
		{
			size_t origin_size = std::distance(_vec.first,_vec.second);//_vec.size();
			size_t n = size_t(0);
			size_t o = this->size()-size_t(1);
			size_t _endFull = endFull(origin_size, _seg_size);
			for (size_t i = seg_size; i <= _endFull; i += seg_size) {
                //Windows
				//auto v = std::pair<std::vector<DataType>::iterator, std::vector<DataType>::iterator>(_vec.first + i - seg_size, _vec.first + i - 1);
				auto v = bounds(_vec.first + i - seg_size, _vec.first + i - size_t(1) );
				this->at(n++) = v;
			}
			if (_endFull != origin_size) {
				auto l = origin_size - _endFull;
                //Windows
				//auto v = std::pair<std::vector<DataType>::iterator, std::vector<DataType>::iterator>(_vec.second - l, _vec.second - 1);
				auto v = bounds(_vec.second - l, _vec.second - size_t(1) );
				this->at(o) = v;
			}
		};
	template blocks<sp::timecode<double>,std::pair< std::vector<sp::timecode<double>>::iterator,std::vector<sp::timecode<double>>::iterator >>::blocks(std::pair< typename std::vector<sp::timecode<double>>::iterator, typename std::vector<sp::timecode<double>>::iterator > vec, const size_t seg_size);
	template blocks<sp::timecode<float>,std::pair< std::vector<sp::timecode<float>>::iterator,std::vector<sp::timecode<float>>::iterator >>::blocks(std::pair< typename std::vector<sp::timecode<float>>::iterator, typename std::vector<sp::timecode<float>>::iterator > vec, const size_t seg_size);
	template blocks<sp::timecode<int16_t>,std::pair< std::vector<sp::timecode<int16_t>>::iterator,std::vector<sp::timecode<int16_t>>::iterator >>::blocks(std::pair< typename std::vector<sp::timecode<int16_t>>::iterator, typename std::vector<sp::timecode<int16_t>>::iterator > vec, const size_t seg_size);
	
	template<typename DataType,typename bounds> size_t blocks<DataType,bounds>::calculateSize(size_t vec_size, size_t seg_size) {
			if (vec_size > seg_size) {
				if ((vec_size%seg_size) == size_t(0) ) {
					return vec_size / seg_size;
				}
				else {
					return (vec_size / seg_size) + size_t(1) ;
				}
			}
			else {
				return 1;
			}
		};
		

		template<typename DataType, typename bounds> size_t blocks<DataType,bounds>::mySize(const bounds vec, size_t seg_size) {
			// a fixpoint in a block of 1 can not be separated
			//auto a = addedFixPoints(vec);
			auto x = calculateSize(std::distance(vec.first,vec.second), seg_size);
			// we need at least one more than total number of fixpoints
			//if (x > a)
			//	return x+a;
			//else
			return x;
		}
		//needed in initializer
		template<typename DataType, typename bounds> size_t blocks<DataType,bounds>::endFull(size_t vec_size, size_t seg_size) {
			if ((vec_size % seg_size) == size_t(0) )
				return vec_size;
			else
				return vec_size - (vec_size%seg_size);
		}
		

//	template<typename DataType> size_t blocks<DataType>::addedFixPoints(const bounds<DataType> vec) {
//		return 0;
//	}

//#include "shared_types.h"
//	template<> size_t blocks<sp::element>::addedFixPoints(const bounds<sp::element> vec){
//		return std::count_if(vec.first, vec.second, [](sp::element& t) {
//			//return !sp::is<sp::empty<sp::element::value_type>>(dynamic_cast<sp::element*>(t));
//			return t->category == sp::tctype::FIXPOINT; 
//		});
//	}
};
