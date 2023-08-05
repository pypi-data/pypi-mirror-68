// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CLIFFSNORMALIZER_H
#define CLIFFSNORMALIZER_H

#include "areacalculator.h"
#include "turnnormalizer.h"
#include "cornernormalizer.h"

template<typename T> class CliffsNormalizer : public AreaCalculator<T>
{
public:
    CliffsNormalizer<T>();
    template<typename F> CliffsNormalizer<T>(F& list);

    // these methods are being used for cleaning up the segments before the corner detection
    void cliffFilters();
};

#endif // CLIFFSNORMALIZER_H
