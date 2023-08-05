// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNNORMALIZER_H
#define TURNNORMALIZER_H

#include "turncalculator.h"
#include "listswitchable.h"

template<typename T> class TurnNormalizer : public TurnCalculator<T>
{
public:
    TurnNormalizer<T>();
    template<typename F> TurnNormalizer<T>(F& list);


    //ACL: foreign
    // this will just produce a whole lot of straight lines
    void smoothingJitter(int pos);
    // supposed to produce curves -> will be replaced by dot product intrapolation
    void risingJitter(int pos);

    void tripletFilters();
};

#endif // TURNNORMALIZER_H
