// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef ANGLE_FUNCTIONS
#define ANGLE_FUNCTIONS

#include <numeric>
#include <vector>
#include <functional>
#include <math.h>
#include <limits>
#include "stopeight-clibs/shared_types.h"

namespace angle {

	//template<typename T> using vector_T = typename std::vector<T>::iterator;

	template <class Iterator>double __average(Iterator begin, Iterator end) {
			//todo sum should not be propagating
			auto sum = std::accumulate(begin, end, 0.0, [](double first, double second) {
				return first += fabs(second);

			});
			return sum / std::distance(begin, end);
	};

	//templating struct / class differentiation not possible
	class averageScaled {
	public:
		template<typename av_it>averageScaled(av_it begin, av_it end, double average, double angleScale)
			: av((average == 0.0) ? __average(begin, end) : average)
			, _angleScale((angleScale == 0.0) ? std::numeric_limits<double>::min() : angleScale) {
		}
	protected:
		double av;
		double _angleScale;
	};

	class sharing_angle : public averageScaled, public sp::sharing_functor<double, double> {
	public:
		template<typename Iterator> sharing_angle(Iterator begin, Iterator end, double average, double angleScale) :averageScaled(begin, end, average, angleScale) {};
	};

	//operator() contains assignments of class members that have to be applied sequentially
	class propagating_angle : public averageScaled, public sp::propagating_functor<double, double> {
	public:
		template<typename Iterator> propagating_angle(Iterator begin, Iterator end, double average, double angleScale) :averageScaled(begin, end, average, angleScale) {};
	};

	//operator() can contain assignments of class members, but they dont have to be in sequence
	class vectorized_angle : public averageScaled, public sp::readonly_functor<double, double> {
	public:
		template<typename Iterator> vectorized_angle(Iterator begin, Iterator end, double average, double angleScale) :averageScaled(begin, end, average, angleScale) {};
	};

	class relative2 : public propagating_angle {
	public:
		template<typename Iterator>relative2(Iterator begin, Iterator end, double average=0.0, double angleScale=1.0,double initialAngle = 0.0) : propagating_angle(begin, end, average, angleScale), _previous(initialAngle) {};
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			auto absdiff = 0;
			_previous += atan((d / av)*_angleScale / av);
			return (_previous);
		};
	private:
		double _previous;
	};

	class independent2 : public vectorized_angle {
	public:
		template<typename Iterator>independent2(Iterator begin, Iterator end, double average = 0.0, double angleScale = 1.0) : vectorized_angle(begin, end, average, angleScale) {};
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			return atan((d / av)*_angleScale / av);
		};
	};

	class relative : public propagating_angle {
	public:
		template<typename Iterator>relative(Iterator begin, Iterator end, double average = 0.0, double angleScale = 1.0, double initialAngle = 0.0) : propagating_angle(begin, end, average, angleScale), _previous(initialAngle) {};
		//propagating
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			_previous += atan(d*_angleScale / av);
			return (_previous);
		};
	private:
		double _previous;
	};

	class independent : public vectorized_angle {
	public:
		template<typename Iterator>independent(Iterator begin, Iterator end, double average = 0.0, double angleScale = 1.0) : vectorized_angle(begin, end, average, angleScale) {};
		//non-propagating
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			return atan(d*_angleScale / av);
		};
	};

	/*class test : public vectorized_angle {
	public:
		template<typename Iterator>test(Iterator begin, Iterator end) : vectorized_angle(begin, end) {};
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			return 300 * asin(d);
		};
	};

	class test2 : public propagating_angle {
	public:
		template<typename Iterator>test2(Iterator begin, Iterator end, double initialAngle = 0.0) : propagating_angle(begin, end), _previous(initialAngle) {};
		double operator()(double d) {
			if (d == 0.0 || av == 0.0)
				return double(0.0);
			double inc = d - av;
			if (inc <= 0)
				inc = 0;
			_previous += atan((inc) / av);
			return (_previous);
		};
	private:
		double _previous;
	};

	class test3 : public vectorized_angle {
	public:
		test3(double dummer) {};
		double operator()(double d) {
			return atan(d);
		};
	private:
	};*/
}

#endif
