// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "straightsnormalizer.h"

template<> StraightsNormalizer<dpoint>::StraightsNormalizer() : StraightsCalculator<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> StraightsNormalizer<dpoint>::StraightsNormalizer(F& list) : StraightsCalculator<dpoint>(list){
    ListSwitchable<dpoint> c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<StraightsNormalizer<dpoint>& >(c);
}

#include "areanormalizer.h"
template StraightsNormalizer<dpoint>::StraightsNormalizer(AreaNormalizer<dpoint>& list);
template StraightsNormalizer<dpoint>::StraightsNormalizer(CornerNormalizer<dpoint>& list);
