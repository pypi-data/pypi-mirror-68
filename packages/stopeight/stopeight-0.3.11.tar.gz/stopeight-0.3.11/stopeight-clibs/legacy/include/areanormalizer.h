// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREANORMALIZER_H
#define AREANORMALIZER_H

#include "areacalculator.h"
#include "turnnormalizer.h"
#include "cornernormalizer.h"

template<typename T> class AreaNormalizer : public AreaCalculator<T>
{
public:
    AreaNormalizer<T>();
    template<typename F> AreaNormalizer<T>(F& list);

    // these methods are being used for cleaning up the segments before the corner detection
    void areaFilters();

    // crafting out spirals: 3point segment direction change
    void removeInlays();
};

#endif // AREANORMALIZER_H
