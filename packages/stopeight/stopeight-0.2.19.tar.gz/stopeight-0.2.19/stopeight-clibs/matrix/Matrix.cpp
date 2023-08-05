// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#include "stopeight-clibs/Matrix.h"
#include "stopeight-clibs/shared_types.h"
#include <cmath>
#include <algorithm>
//#include "GLPlatform.h"

// not available on windows:
#ifndef M_PI
#define M_PI        3.14159265358979323846264338327950288
#endif

template<typename T, size_t Size, typename tf> Vector<T, Size,tf>& Vector<T,Size,tf>::__init(std::initializer_list<T> list) {
	std::copy(std::begin(list),std::end(list),std::begin(coords));
	std::fill(std::begin(coords)+list.size(), std::end(coords), T(0));
	return *this;
}
template Vector<double>& Vector<double>::__init(std::initializer_list<double>);
template Vector<float>& Vector<float>::__init(std::initializer_list<float>);

template<typename Container, typename tf> Vectors<Container,tf>::Vectors() : Container() {
}
//todo span
template Vectors<std::vector<sp::timecode<float>>>::Vectors();
template Vectors<std::vector<sp::timecode<double>>>::Vectors();
template<typename Container, typename tf> Vectors<Container,tf>::Vectors(const Container& other) : Container(other) {
//	int test = 5/0;
//	*this = Vectors<Container,tf>();//other;
}
//todo span
template Vectors<std::vector<sp::timecode<float>>>::Vectors(const std::vector<sp::timecode<float>>& other);
template Vectors<std::vector<sp::timecode<double>>>::Vectors(const std::vector<sp::timecode<double>>& other);
template<typename Container, typename tf> Vectors<Container,tf>::Vectors(Container&& other) : Container{std::move(other)} {
	//Vectors<Container,tf> temp = std::move(other);
	//*this = temp;
	//*this = static_cast<Container>(other);
	//*this = std::move(other);
}
//todo span
template Vectors<std::vector<sp::timecode<float>>>::Vectors(std::vector<sp::timecode<float>>&& other);
template Vectors<std::vector<sp::timecode<double>>>::Vectors(std::vector<sp::timecode<double>>&& other);
template<typename Container, typename tf> Vectors<Container,tf>& Vectors<Container,tf>::operator=(Container&& other) {
	//Vectors<Container,tf> temp = std::move(other);
	Container::operator=(std::move(other));
	return *this;
}
//todo span
template Vectors<std::vector<sp::timecode<float>>>& Vectors<std::vector<sp::timecode<float>>>::operator=(std::vector<sp::timecode<float>>&& other);
template Vectors<std::vector<sp::timecode<double>>>& Vectors<std::vector<sp::timecode<double>>>::operator=(std::vector<sp::timecode<double>>&& other);

//propagating: par
template<typename Container, typename tf>void Vectors<Container,tf>::apply(Stack<Container>& stack) {
	auto& me = *this;
	auto first = std::find_if(std::begin(stack), std::end(stack), [](Matrix<Container>& m){ return !m.isSingular();});
	if (first!=std::end(stack)){
#if DEVELOPMENT
		if (*first==Matrix<Container>::identity())
			throw std::logic_error("multiplying identity matrix has performance penalty. Check before adding to stack.");
#endif
		Matrix<Container> all = *first;
		std::for_each(++first, std::end(stack), [&all](Matrix<Container>& m) {
#if DEVELOPMENT
			if (m==Matrix<Container>::identity())
				throw std::logic_error("multiplying identity matrix has performance penalty. Check before adding to stack.");
#endif
			if (!m.isSingular())
				all = Matrix<Container>::mul(all,m);
		});
		static const size_t size = PodClass{}.coords.size();
		if (size < 2)
			throw std::logic_error("Matrix class does not work with vector dimensions lower than 2");
		else if (size == 2)
			all.apply2(me);
		else
			all.apply3(me);
	}
	/*std::for_each(std::rbegin(stack), std::rend(stack), [&me](Matrix<Container>& m) {
		m.apply(me);
	});*/
}
template void Vectors<std::vector<Vector<float>>>::apply(Stack<std::vector<Vector<float>>>& stack);
template void Vectors<std::vector<Vector<double>>>::apply(Stack<std::vector<Vector<double>>>& stack);
//todo span
template void Vectors<std::vector<sp::timecode<float>>>::apply(Stack<std::vector<sp::timecode<float>>>& stack);
template void Vectors<std::vector<sp::timecode<double>>>::apply(Stack<std::vector<sp::timecode<double>>>& stack);

/* Row Major 2D*/
template<typename Container> Matrix<Container>::Matrix(T x1, T x2, T x3, T y1, T y2, T y3, T z1, T z2, T z3) {
	elems[0] = x1;
	elems[1] = x2;
	elems[2] = x3;
	elems[3] = y1;
	elems[4] = y2;
	elems[5] = y3;
	elems[6] = z1;
	elems[7] = z2;
	elems[8] = z3;
}
template Matrix<std::vector<Vector<float>>>::Matrix(float x1, float x2, float x3, float y1,
							   float y2, float y3, float z1, float z2, float z3);
template Matrix<std::vector<Vector<double>>>::Matrix(double x1, double x2, double x3, double y1,
							   double y2, double y3, double z1, double z2, double z3);
//todo span
template Matrix<std::vector<sp::timecode<float>>>::Matrix(float x1, float x2, float x3, float y1,
							   float y2, float y3, float z1, float z2, float z3);
template Matrix<std::vector<sp::timecode<double>>>::Matrix(double x1, double x2, double x3, double y1,
							   double y2, double y3, double z1, double z2, double z3);

template<typename Container> std::array<typename Container::value_type::value_type,9>* Matrix<Container>::data(){
	return &elems;
}
template std::array<double,9>* Matrix<std::vector<Vector<double>>>::data();
template std::array<float,9>* Matrix<std::vector<Vector<float>>>::data();
//todo span
template std::array<double,9>* Matrix<std::vector<sp::timecode<double>>>::data();
template std::array<float,9>* Matrix<std::vector<sp::timecode<float>>>::data();

template<typename Container> Matrix<Container> Matrix<Container>::identity() {
	auto m = Matrix<Container>{	T(1),T(0),T(0),
		T(0),T(1),T(0),
		T(0),T(0),T(1)
	};
	return std::move(m);
}
template Matrix<std::vector<Vector<float>>> Matrix<std::vector<Vector<float>>>::identity();
template Matrix<std::vector<Vector<double>>> Matrix<std::vector<Vector<double>>>::identity();

template<typename Container> typename Container::value_type::value_type Matrix<Container>::det() {
	auto& e = elems;
	auto det = e[0]*e[4]*e[8]+e[1]*e[5]*e[6]+e[2]*e[3]*e[7]-e[0]*e[5]*e[6]-e[1]*e[3]*e[8]-e[2]*e[4]*e[6];
	return det;
}
template float Matrix<std::vector<Vector<float>>>::det();
template double Matrix<std::vector<Vector<double>>>::det();

template<typename Container> bool Matrix<Container>::isSingular(){
#if DEVELOPMENT
	return (det()==0);
#else
	return false;
#endif
}

template<typename Container> Matrix<Container> Matrix<Container>::scale(T x, T y) {
	auto m = Matrix<Container>{	T(x),T(0),T(0),
		T(0),T(y),T(0),
		T(0),T(0),T(1)
	};
	return std::move(m);
}
template Matrix<std::vector<Vector<float>>> Matrix<std::vector<Vector<float>>>::scale(float x, float y);
template Matrix<std::vector<Vector<double>>> Matrix<std::vector<Vector<double>>>::scale(double x, double y);
//todo span
template Matrix<std::vector<sp::timecode<float>>> Matrix<std::vector<sp::timecode<float>>>::scale(float x, float y);
template Matrix<std::vector<sp::timecode<double>>> Matrix<std::vector<sp::timecode<double>>>::scale(double x, double y);

template<typename Container> Matrix<Container> Matrix<Container>::rotate(T deg) {
	T rad = _degToRad(deg);
	auto m = Matrix<Container>{	T(cos(rad)),T(-sin(rad)),T(0),
						T(sin(rad)),T(cos(rad)),T(0),
						T(0),T(0),T(1)
	};
	return std::move(m);
}
template Matrix<std::vector<Vector<float>>> Matrix<std::vector<Vector<float>>>::rotate(float deg);
template Matrix<std::vector<Vector<double>>> Matrix<std::vector<Vector<double>>>::rotate(double deg);
//todo span
template Matrix<std::vector<sp::timecode<float>>> Matrix<std::vector<sp::timecode<float>>>::rotate(float deg);
template Matrix<std::vector<sp::timecode<double>>> Matrix<std::vector<sp::timecode<double>>>::rotate(double deg);

template<typename Container> Matrix<Container> Matrix<Container>::translate(T x, T y) {
	auto m = Matrix<Container>{	T(1),T(0),T(x),
		T(0),T(1),T(y),
		T(0),T(0),T(1)
	};
	return std::move(m);
}
template Matrix<std::vector<Vector<float>>> Matrix<std::vector<Vector<float>>>::translate(float x, float y);
template Matrix<std::vector<Vector<double>>> Matrix<std::vector<Vector<double>>>::translate(double x, double y);

template<typename Container>double Matrix<Container>::_radToDeg(double rad) { return rad * (180.0 / M_PI); }//  pi/rad = 180/x, x(pi/rad)=180, x=180/(pi/rad)
template double Matrix<std::vector<Vector<float>>>::_radToDeg(double rad);
template double Matrix<std::vector<Vector<double>>>::_radToDeg(double rad);
template<typename Container>double Matrix<Container>::_degToRad(double deg) { return deg / (180.0 / M_PI); }

template<typename Container> Matrix<Container> Matrix<Container>::mul(const Matrix<Container> a, const Matrix<Container> b) {
	auto m = Matrix<Container>{	a.elems[0] * b.elems[0]+a.elems[1] * b.elems[3]+a.elems[2] * b.elems[6],	//c00
						a.elems[0] * b.elems[1]+a.elems[1] * b.elems[4]+a.elems[2] * b.elems[7],	//c01
						a.elems[0] * b.elems[2]+a.elems[1] * b.elems[5]+a.elems[2] * b.elems[8],	//c02
						a.elems[3] * b.elems[0]+a.elems[4] * b.elems[3]+a.elems[5] * b.elems[6],	//c10
						a.elems[3] * b.elems[1]+a.elems[4] * b.elems[4]+a.elems[5] * b.elems[7],	//c11
						a.elems[3] * b.elems[2]+a.elems[4] * b.elems[5]+a.elems[5] * b.elems[8],	//c12
						a.elems[6] * b.elems[0]+a.elems[7] * b.elems[3]+a.elems[8] * b.elems[6],	//c20
						a.elems[6] * b.elems[1]+a.elems[7] * b.elems[4]+a.elems[8] * b.elems[7],	//c21
						a.elems[6] * b.elems[2]+a.elems[7] * b.elems[5]+a.elems[8] * b.elems[8]		//c22
	};
	return std::move(m);
}

//this may have to be compiled with a different compiler: NOT HEADER ONLY
//readonly: par_unseq
template<typename Container> void Matrix<Container>::apply3(Vectors<Container>& transform) {
	auto& e = elems;
	std::transform(std::begin(transform), std::end(transform), std::begin(transform), [&e](PodClass a) {
		return PodClass{}.__init(	{
			(e[0]* a.coords[0] +e[1]* a.coords[1] +e[2]* a.coords[2]),
			(e[3]* a.coords[0] +e[4]* a.coords[1] +e[5]* a.coords[2]),
			(e[6]* a.coords[0] +e[7]* a.coords[1] +e[8]* a.coords[2])}
		);
	});
}
template<typename Container> void Matrix<Container>::apply2(Vectors<Container>& transform) {
	auto& e = elems;
	std::transform(std::begin(transform), std::end(transform), std::begin(transform), [&e](PodClass a) {
		return PodClass{}.__init({
			(e[0] * a.coords[0] + e[1] * a.coords[1] + e[2] * 1),
			(e[3] * a.coords[0] + e[4] * a.coords[1] + e[5] * 1)}
		);
	});
}

template<typename Container> Stack<Container>::Stack() : std::vector<Matrix<Container>>() {};
template<> Stack<std::vector<Vector<float>>>::Stack() : std::vector<Matrix<std::vector<Vector<float>>>>() {};
template<> Stack<std::vector<Vector<double>>>::Stack() : std::vector<Matrix<std::vector<Vector<double>>>>() {};
//todo span
template<> Stack<std::vector<sp::timecode<float>>>::Stack() : std::vector<Matrix<std::vector<sp::timecode<float>>>>() {};
template<> Stack<std::vector<sp::timecode<double>>>::Stack() : std::vector<Matrix<std::vector<sp::timecode<double>>>>() {};

template<typename Container> void Stack<Container>::identity(){
	this->clear();
}
template void Stack<std::vector<Vector<float>>>::identity();
template void Stack<std::vector<Vector<double>>>::identity();
//todo span
template void Stack<std::vector<sp::timecode<float>>>::identity();
template void Stack<std::vector<sp::timecode<double>>>::identity();

template<typename Container> void Stack<Container>::scale(T x,T y){
	if (!(( T(1.0)==x)&&( T(1.0)==y)))
		this->push_back( Matrix<Container>::scale(x,y));
}
template void Stack<std::vector<Vector<float>>>::scale(float x,float y);
template void Stack<std::vector<Vector<double>>>::scale(double x,double y);
//todo span
template void Stack<std::vector<sp::timecode<float>>>::scale(float x,float y);
template void Stack<std::vector<sp::timecode<double>>>::scale(double x,double y);

template<typename Container> void Stack<Container>::rotate(T deg){
	if (!(deg== T(0.0) ))
		this->push_back( Matrix<Container>::rotate(deg));
}
template void Stack<std::vector<Vector<float>>>::rotate(float deg);
template void Stack<std::vector<Vector<double>>>::rotate(double deg);
//todo span
template void Stack<std::vector<sp::timecode<double>>>::rotate(double deg);
template void Stack<std::vector<sp::timecode<float>>>::rotate(float deg);

template<typename Container> void Stack<Container>::translate(T x,T y){
	if (!(( T(0.0)==x)&&( T(0.0)==y)))
		this->push_back( Matrix<Container>::translate(x, y));
}
template void Stack<std::vector<Vector<float>>>::translate(float x,float y);
template void Stack<std::vector<Vector<double>>>::translate(double x,double y);
template void Stack<std::vector<sp::timecode<float>>>::translate(float x,float y);
template void Stack<std::vector<sp::timecode<double>>>::translate(double x,double y);