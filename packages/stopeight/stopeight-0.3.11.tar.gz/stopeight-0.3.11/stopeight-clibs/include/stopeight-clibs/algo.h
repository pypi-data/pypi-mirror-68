// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#ifndef ALGO_H
#define ALGO_H

#include <stopeight-clibs/angle_functions.h>

namespace grapher {

	template<typename T> using it_pair = std::pair< typename std::vector<sp::timecode<T>>::iterator, typename std::vector<sp::timecode<T>>::iterator >;

	template<class InputIterator, class OutputIterator,
		typename = typename std::enable_if_t<std::is_base_of<std::random_access_iterator_tag, typename std::iterator_traits<InputIterator>::iterator_category>::value && std::is_arithmetic<typename std::iterator_traits<InputIterator>::value_type>::value>
	> void __differences(InputIterator begin, InputIterator end, OutputIterator begin2);

	//OVERLOAD: multiple functions for class hierarchy (btw. SPECIALISATION is only for class-templates)
	template<class InputIterator, class OutputIterator,
		typename = typename std::enable_if_t<std::is_base_of<std::input_iterator_tag, typename std::iterator_traits<InputIterator>::iterator_category>::value && std::is_arithmetic<typename std::iterator_traits<InputIterator>::value_type>::value>
	> void __calculate_rotations(InputIterator begin, InputIterator end, OutputIterator begin2, sp::sharing_functor<double,double>& angleFunction);
	//readonly functor and input_iterator_tag combination is nonsense
	template<class InputIterator, class OutputIterator,
		typename = typename std::enable_if_t<std::is_base_of<std::input_iterator_tag, typename std::iterator_traits<InputIterator>::iterator_category>::value && std::is_arithmetic<typename std::iterator_traits<InputIterator>::value_type>::value>
	> void __calculate_rotations(InputIterator begin, InputIterator end, OutputIterator begin2, sp::readonly_functor<double,double>& angleFunction);


	template<class InputIterator, class OutputIterator,
		typename = typename std::enable_if_t<std::is_base_of<std::random_access_iterator_tag, typename std::iterator_traits<InputIterator>::iterator_category>::value && std::is_arithmetic<typename std::iterator_traits<InputIterator>::value_type>::value>
	> void __apply_rotation_matrix(InputIterator begin, InputIterator end, OutputIterator begin2);

	class _fixpoints {
	public:
		_fixpoints(std::vector<size_t>& points);
		~_fixpoints();
		template <class InputIterator, class OutputIterator,
		typename = typename sp::random_access<InputIterator>
		>void operator()(InputIterator begin, InputIterator end, OutputIterator begin2);
	private:
		std::vector<size_t>& _fixPoint_indices;
	};

	class _blocks {
	public:
		_blocks(size_t samplesPerVector);
		~_blocks();
		template <class InputIterator, class OutputIterator>void operator()(InputIterator begin, InputIterator end, OutputIterator begin2);
	private:
		size_t _samplesPerVector;
	};

	template <class InputIterator, class OutputIterator>void _sum_blocks(InputIterator begin, InputIterator end, OutputIterator begin2);//freedom vector or deque//type in or out?

	template <class InputIterator, class OutputIterator,
		typename = typename sp::input_iterator<InputIterator>
	>void _append(InputIterator begin, InputIterator end, OutputIterator begin2);

	template<class T> class __differences_To_VG {
	public:
		__differences_To_VG(size_t samplesPerVector, double vectorLength, std::vector<size_t> fixPoints_indices = std::vector<size_t>(1, 0));
		~__differences_To_VG();

		//TEMPLATE: one function for multiple types
        template <class UnaryFunction,
			typename = typename std::enable_if_t<std::is_base_of<sp::sharing_functor<double, double>, UnaryFunction>::value>//std::enable_if_t<std::is_base_of<sp::readonly_functor<double,double>,UnaryFunction>::value>
		>
			//mass allocation of different types, so no iterator-functor paradigm here
			std::vector<sp::timecode<T>> operator()(std::vector<T>& differences, UnaryFunction& angleFunction);

	private:
		size_t _samplesPerVector;
		double _vectorLength;
		std::vector<size_t> _fixPoint_indices;
	};

	int samples_To_VG_vectorSize(int inputSize, int samplesPerVector=1);
	double samples_To_VG_vectorLength(int showSamples, double unitaryLength = 1);

	template<class T> class samples_To_VG {
	public:
		//experimental value from notation2.wav => sin(1.0f/300.0f)
		samples_To_VG(size_t samplesPerVector, double vectorLength, std::vector<size_t> fixPoints_indices = std::vector<size_t>(1, 0));
		~samples_To_VG();

		//uses functions with allocations, so no iterator-functor paradigm either!
		template <class UnaryFunction> std::vector<sp::timecode<T>> operator()(std::vector<T>& samples, UnaryFunction& angleFunction);

	private:
		size_t _samplesPerVector;
		double _vectorLength;
		std::vector<size_t> _fixPoint_indices;
	};
}
#endif
