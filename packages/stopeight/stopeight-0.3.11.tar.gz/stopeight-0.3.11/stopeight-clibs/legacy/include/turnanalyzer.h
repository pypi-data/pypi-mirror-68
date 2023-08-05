// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNANALYZER_H
#define TURNANALYZER_H

#include "turnnormalizer.h"
#include "listcopyable.h"
#include "straightsanalyzer.h"
#include "corneranalyzer.h"

template<typename T> class TurnAnalyzer : public TurnNormalizer<T>
{
public:
    TurnAnalyzer<T>();
    template<typename F> TurnAnalyzer<T>(F& list);

    ListCopyable<dpoint> getFirstTurnByTriplets();
    // This is replacement for old_code scalar/crest approach
    ListCopyable<dpoint> getFirstTriplet();
};

#endif // TURNANALYZER_H
