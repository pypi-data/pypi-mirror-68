// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CORNERCALCULATOR_H
#define CORNERCALCULATOR_H

#include "listswitchable.h"

template<typename T> class CornerCalculator : public ListSwitchable<T>
{
public:
    CornerCalculator<T>();
    template<typename F> CornerCalculator<T>(F& list);

};

#endif // CORNERCALCULATOR_H
