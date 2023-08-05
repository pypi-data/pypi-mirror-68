// Copyright (C) 2017 Fassio Blatter
// GNU Lesser General Public License, version 2.1

#pragma once
#include <array>
#include <vector>
#include <iterator>

template<typename T, size_t Size = 2,
	typename tf= typename std::enable_if_t<std::is_arithmetic<T>::value>
	> class Vector {
public:
	using element = typename std::array<T, Size>;
	typedef typename element::value_type value_type;
	typedef typename element::reference reference;

	Vector<T, Size,tf>& __init(std::initializer_list<T> list);

	std::array<T, Size> coords;
};

template<typename Container, typename tf = typename std::enable_if_t<std::is_pod<typename Container::value_type>::value>> class Vectors;//forward declaration! same as in real declaration below

/* Row Major 2D*/
template<typename Container> class Matrix {
public:
	using PodClass = typename Container::value_type;
	using T = typename Container::value_type::value_type;

	friend class Matrix;
	friend class Vectors<Container>;
	
	Matrix(const Matrix& other) = default;
	Matrix(Matrix&& other) = default;
	explicit Matrix(T x1, T x2, T x3, T y1, T y2, T y3, T z1, T z2, T z3);
	std::array<T,9>* data();

	Matrix& operator=(const Matrix& other) = default;
	bool operator!=(const Matrix& other){
		return (elems != other.elems);
	}
	bool operator==(const Matrix& other){
		return (elems == other.elems);
	}
	
	static Matrix identity();

	//MSVC: function return type (and signature) is read before alias definition
	typename Container::value_type::value_type det();
	
	bool isSingular();
	
	static Matrix scale(T x, T y);
	
	static Matrix rotate(T deg);
	
	static Matrix translate(T x, T y);
	double static _radToDeg(double rad);
	double static _degToRad(double deg);

private:
	static Matrix mul(const Matrix a, const Matrix b);
	void apply3(Vectors<Container>& transform);
	void apply2(Vectors<Container>& transform);
private:
	std::array<T,9> elems;
};

//todo disable type conversions here?
template<typename Container> class Stack : public std::vector<Matrix<Container>> {

public:
	using PodClass = typename Container::value_type;
	using T = typename PodClass::value_type;

	Stack();
	
	void identity();
	void scale(T x, T y);
	//this was void rotate(FLOAT deg); why?!
	void rotate(T deg);
	void translate(T x, T y);
};

template<typename Container,
	typename// = typename std::enable_if_t<std::is_pod<PodClass>::value>
> // same as in forward declaration above!
class Vectors : public Container {
	//todo
	//we cannot make Vectors a pod type
	//AND std::vector can not use memory of numpy_array; (they're both in stack)
	//-> no move constructor from numpy array
public:
	using Container::Container;
	Vectors();
	Vectors(const Container& other);
	Vectors(Container&& other);
	Vectors& operator=(Container&& other);

	using PodClass = typename Container::value_type;
	using T = typename PodClass::value_type;

	void apply(Stack<Container>& stack);

	/*const T* _to_C_array(){
		if (this->size()>0)
			return &(this->at(0))[0];
		else
			return nullptr;
	}*/
};
