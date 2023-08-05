// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef STRAIGHTSCALCULATOR_H
#define STRAIGHTSCALCULATOR_H

#include "listswitchable.h"
#include "calculator.h"

template<typename T> class StraightsCalculator : public ListSwitchable<T>
{
public:
    StraightsCalculator<T>();
    template<typename F> StraightsCalculator<T>(F& list);

    // length of curve between "all"! points / curvature not included
    qreal sumLength();

    qreal sumRotYFrom(int start);
    // erroneos integration
    qreal sumOfLinesRotY();
};

#endif // STRAIGHTSCALCULATOR_H
