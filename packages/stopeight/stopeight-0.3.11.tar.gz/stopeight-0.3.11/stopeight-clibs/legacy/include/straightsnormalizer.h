// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef STRAIGHTSNORMALIZER_H
#define STRAIGHTSNORMALIZER_H

#include "turncalculator.h"
#include "listswitchable.h"
#include "straightscalculator.h"

template<typename T> class StraightsNormalizer : public StraightsCalculator<T>
{
public:
    StraightsNormalizer<T>();
    template<typename F> StraightsNormalizer<T>(F& list);

};

#endif // STRAIGHTSNORMALIZER_H
