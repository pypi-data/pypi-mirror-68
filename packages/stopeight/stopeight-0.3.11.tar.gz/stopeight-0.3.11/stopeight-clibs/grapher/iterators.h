// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef ITERATORS_H
#define ITERATORS_H

/*
	Not used because last hast to be known, implemented in containers.h
*/

namespace stopeight {
	//has to be random access; is forward
	template<typename IteratorType> class block_iterator : public std::iterator<std::forward_iterator_tag,
																				std::pair<IteratorType,IteratorType> > {
	public:
		explicit block_iterator(IteratorType& rand, IteratorType& rand2, const int seg_size=1) : _first(rand), _last(rand2), _pos(0), _seg_size(seg_size) {
			if (_seg_size > std::distance(_first, _last)) {
				_seg_size = std::distance(_first, _last);
			}
			//case _first>_last
		};
		//const, arg const
		bool operator==( block_iterator<IteratorType>& b) {
			std::pair<IteratorType, IteratorType> a* = construct();
			bool result = false;
			if ((a->first == b->first) && (a->second == b->second))
				result = true;
			delete a;
			return result;
		};
		//const, arg const
		bool operator!=( block_iterator<IteratorType>& b) {
			std::pair<IteratorType, IteratorType>* a = construct();
			bool result = false;
			if ((a->first != b->first) || (a->second != b->second))
				result = true;
			delete a;
			return result;
		};
		block_iterator<IteratorType>& operator++() {
			block_iterator<IteratorType> tmp = *this;
			_pos += _seg_size;
			return tmp;
		};
		block_iterator<IteratorType> operator++(int i) {
			_pos += i*_seg_size;
			return this;
		};
		//const
		std::pair<IteratorType, IteratorType>& operator*() {
			std::pair<IteratorType, IteratorType>& a = *(construct());
			return a;
		}
		//const
		std::pair<IteratorType, IteratorType>* operator->() {
			std::pair<IteratorType, IteratorType>* a = construct();
			return a;
		}
		//This should be in container or independent function
		//full iterator with pos set from outside,
		//or short iterator with pos=0
		/*block_iterator end() {
			return blockiterator<IteratorType>(_first, _first, _seg_size);
			//int d = std::distance(_first, _last)
			//int i = d / _seg_size;
			//IteratorType current,end;
			//if (remainder() == 0)
			//	current = _first + (i - 1)*_seg_size;
			//else
			//	current = _first + (i)*_seg_size;
		}*/


	private:
		//if _seg_size=1 and std::distance =1, pos=0, then legal and remainder=0 => current, end=last-1
		bool _legalPos() { return (_pos < std::distance(_first, _last)); };
		int remainder() { return std::distance(_first, _last) % _seg_size; };
		std::pair<IteratorType, IteratorType>* construct() {
			if (_legalPos()) {
				IteratorType& current = _first + _pos;
				if (std::distance(current, _last) >= _seg_size){
					IteratorType& end = current + _seg_size;
					return new std::pair<IteratorType, IteratorType>{ current,end };
				} else {
					IteratorType& end = current + remainder();
					return new std::pair<IteratorType, IteratorType>{ current,end };
				}
			}
			else {
				IteratorType& current = _last;
				IteratorType& end = _last;
				return new std::pair<IteratorType, IteratorType>{ current,end };
			}
		};
		IteratorType& _first,_last;
		int _pos, _seg_size;
	};
}
#endif