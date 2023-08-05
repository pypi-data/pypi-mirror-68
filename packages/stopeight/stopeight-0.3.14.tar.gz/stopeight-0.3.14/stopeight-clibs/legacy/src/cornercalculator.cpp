// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cornercalculator.h"

template<> CornerCalculator<dpoint>::CornerCalculator() : ListSwitchable<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> CornerCalculator<dpoint>::CornerCalculator(F& list) : ListSwitchable<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<CornerCalculator<dpoint>& >(c);
}

#include "turnnormalizer.h"
template CornerCalculator<dpoint>::CornerCalculator(TurnNormalizer<dpoint>& list);
#include "calculator.h"
template CornerCalculator<dpoint>::CornerCalculator(Calculator<dpoint>& list);
template CornerCalculator<dpoint>::CornerCalculator(ListBase<dpoint>& list);
#include "cliffsnormalizer.h"
template CornerCalculator<dpoint>::CornerCalculator(CliffsNormalizer<dpoint>& list);
#include "listcopyable.h"
template CornerCalculator<dpoint>::CornerCalculator(ListCopyable<dpoint>& list);
#include "areanormalizer.h"
template CornerCalculator<dpoint>::CornerCalculator(AreaNormalizer<dpoint>& list);
template CornerCalculator<dpoint>::CornerCalculator(CornerNormalizer<dpoint>& list);
