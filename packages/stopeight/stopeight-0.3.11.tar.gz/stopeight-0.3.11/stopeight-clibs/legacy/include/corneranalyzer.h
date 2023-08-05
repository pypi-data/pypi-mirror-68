// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CORNERANALYZER_H
#define CORNERANALYZER_H

#include "cornernormalizer.h"
#include "listcopyable.h"
#include "analyzer.h"
#include "cliffscalculator.h"

template<typename T> class CornerAnalyzer : public CornerNormalizer<T>
{
public:
    CornerAnalyzer<T>();
    template<typename F> CornerAnalyzer<T>(F& list);

    // implementation of "clean" math; as opposed to old_code shrinkToDeltas
    ListCopyable<dpoint> getFirstCorner();
};

#endif // CORNERANALYZER_H
