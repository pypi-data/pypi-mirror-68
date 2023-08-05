// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREACALCULATOR_H
#define AREACALCULATOR_H

#include "listswitchable.h"
#include "calculator.h"

template<typename T> class AreaCalculator : public ListSwitchable<T>
{
public:
    AreaCalculator<T>();
    template<typename F> AreaCalculator<T>(F& list);

    // a.k.a integration up to triangle / curvature not included
    qreal sumOfDxAreasRotY();

    // should be static OR member of List
    qreal triangleArea(QPointF A, QPointF B, QPointF C);
    // "pure" diameter
    qreal lengthFromStartToEnd();


};

#endif // AREACALCULATOR_H
