// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "spiralscalculator.h"

template<> SpiralsCalculator<dpoint>::SpiralsCalculator() : ListSwitchable<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> SpiralsCalculator<dpoint>::SpiralsCalculator(F& list) : ListSwitchable<dpoint>(list){
    ListSwitchable<dpoint> c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<SpiralsCalculator<dpoint>& >(c);
}
