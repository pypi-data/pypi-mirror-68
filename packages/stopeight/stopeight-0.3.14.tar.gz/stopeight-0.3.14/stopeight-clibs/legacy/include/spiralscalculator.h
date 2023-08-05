// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef SPIRALSCALCULATOR_H
#define SPIRALSCALCULATOR_H

#include "listswitchable.h"

template<typename T> class SpiralsCalculator : public ListSwitchable<T>
{
public:
    SpiralsCalculator<T>();
    template<typename F> SpiralsCalculator<T>(F& list);

};

#endif // SPIRALSCALCULATOR_H
