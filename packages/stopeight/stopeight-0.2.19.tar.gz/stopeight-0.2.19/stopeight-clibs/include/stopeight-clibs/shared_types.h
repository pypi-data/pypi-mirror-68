// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef SHARED_TYPES_H
#define SHARED_TYPES_H

#include <vector>
#include <array>
#include <tuple>
#include <cassert>
#include <algorithm>

namespace sp {

	enum class FixpointType {
		EMPTY,
		FIXPOINT
	};

	enum class tctype
	{
		EMPTY,
		SWING,
		CREST,
		DUNE,
		EDGE,
		LEGALSEGMENT,
		CLIFF,
		SPIRAL,
		//Corner??
		STRAIGHT
	};

	enum class covertype {
		EMPTY,
		SWELL,
		SPIRAL,
		ZIGZAG
	};
	//const sp::tctype turns[3] = { tctype::SWING,tctype::CREST,tctype::SPIRAL };
	//ENABLE_IF does work for classes (not in MSVC doc)
	template<class T, size_t Size = 2,
		typename = typename std::enable_if_t<std::is_arithmetic<T>::value
		>
	> struct timecode {//inheritance AND data members present, or tuple: not pod
		using element = typename std::array<T, Size>;
		//timecode(std::initializer_list<T>) = delete;
		/*timecode<T,Size>& operator=(std::initializer_list<T>& other) {
			static_assert(other.size() == std::tuple_size<element>::value);
			auto e = element{other};
			this->coords = e;
			this->clear_types();
			return *this;
		}*/
		timecode<T, Size>& __init(std::initializer_list<T> list){//U x = U(0), U y = U(0), U z = U(1)) {
			//todo compile-time/stack loops?
			std::copy(std::begin(list),std::end(list),std::begin(coords));
			std::fill(std::begin(coords)+list.size(), std::end(coords), T(0));
			this->clear_types();
			return *this;
		}
		timecode<T,Size>& operator+=(const timecode<T,Size>& other) {
			//assert(this->type==FixpointType::EMPTY && other.type==FixpointType::EMPTY);
			std::transform(std::begin(this->coords), std::end(this->coords), std::begin(other.coords), std::begin(this->coords), std::plus<T>{});
			return *this;
		}
		bool operator==(const timecode<T,Size>& other) {
			return std::equal(std::begin(this->coords), std::end(this->coords),std::begin(other.coords)) ;
		}

		typedef typename element::value_type value_type;
		typedef typename element::reference reference;
		sp::FixpointType category() {
			return type;
		}
		void set_category(sp::FixpointType type) {
			this->type = type;
		}
		void clear_types() {
			type = sp::FixpointType::EMPTY;
			tct_type = sp::tctype::EMPTY;
			cov_type = sp::covertype::EMPTY;
		}

//todo get/set element-wise with templated size
		value_type get_x() { return coords[0]; };
		value_type get_y() { return coords[1]; };
		void set_x(value_type other) { coords[0] = other; };
		void set_y(value_type other) { coords[1] = other; };

	//public: //assignment operator does not work when private members present and no CLASS constructor
	//construction by order of appearance!
		element coords;//1
		sp::FixpointType type;//2
		sp::tctype tct_type;//3
		sp::covertype cov_type;//4
	};
	/*template<typename T> timecode<T> make_timecode(T x,T y,FixpointType type= FixpointType::EMPTY) {
		timecode<T> tc;
		tc.set_x(x);
		tc.set_y(y);
		tc.set_category(type);
		return tc;
	};*/

	//todo unify with inclass operator
	template<typename T>bool operator==(const sp::timecode<T> a,const sp::timecode<T> b){
		return std::equal(std::begin(a.coords), std::end(a.coords),std::begin(b.coords)) ;
	}
	
	template<typename T> using input_iterator = typename std::enable_if_t < std::is_base_of<std::input_iterator_tag, typename std::iterator_traits<T>::iterator_category>::value>; //&& std::is_arithmetic<typename std::iterator_traits<T>::value_type::value_type>::value>;
	template<typename T> using random_access = typename std::enable_if_t<std::is_base_of<std::random_access_iterator_tag, typename std::iterator_traits<T>::iterator_category>::value>; //&& std::is_arithmetic<typename std::iterator_traits<T>::value_type::value_type>::value>;

	struct sharing_functor_tag {};
	struct propagating_functor_tag : sharing_functor_tag {};
	struct readonly_functor_tag : propagating_functor_tag {};
	template<class R,class... Args> class functor {//: public std::function<R,Args...> {
	public:
		virtual ~functor() {};
		virtual R operator()(Args... arguments) = 0;
	};
	//member variables can be assigned from within operator(), strictly sequential
	template<class R, class... Args> class sharing_functor : public functor<R, Args...> {
	public:
		using functor_category = sharing_functor_tag;
	};
	//member variables can be assigned from within operator(), but this is non-blocking
	//is it still sequential when out of order threads terminate earlier?
	template<class R, class... Args> class propagating_functor : public sharing_functor<R, Args...> {
	public:
		using functor_category = propagating_functor_tag;
	};
	//member variables (should) not be assigned from within operator()
	template<class R, class... Args> class readonly_functor : public propagating_functor<R, Args...> {
	public:
		using functor_category = readonly_functor_tag;
	};
	template<class Ftor> struct functor_traits{
		using functor_category = typename Ftor::functor_category;
	};

}

#endif
