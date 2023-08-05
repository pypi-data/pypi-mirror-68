// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef STRAIGHTSANALYZER_H
#define STRAIGHTSANALYZER_H

#include "turnnormalizer.h"
#include "listcopyable.h"
#include "straightscalculator.h"

template<typename T> class StraightsAnalyzer : public StraightsCalculator<T>
{
public:
    StraightsAnalyzer<T>();
    template<typename F> StraightsAnalyzer<T>(F& list);

    bool checkIfSectionIsStraightLine(qreal sumLengthFactor);
};

#endif // STRAIGHTSANALYZER_H
