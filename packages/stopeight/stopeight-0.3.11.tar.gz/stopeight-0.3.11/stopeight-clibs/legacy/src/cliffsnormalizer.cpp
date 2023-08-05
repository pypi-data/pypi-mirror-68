// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffsnormalizer.h"

template<> CliffsNormalizer<dpoint>::CliffsNormalizer() : AreaCalculator<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> CliffsNormalizer<dpoint>::CliffsNormalizer(F& list) : AreaCalculator<dpoint>() {
	ListBase<dpoint> c = static_cast<ListBase<dpoint>&>(list);
	*this = static_cast<CliffsNormalizer<dpoint>&>(c);
}

#include "listcopyable.h"
template CliffsNormalizer<dpoint>::CliffsNormalizer(ListCopyable<dpoint>& list);
#include "areaanalyzer.h"
template CliffsNormalizer<dpoint>::CliffsNormalizer(AreaAnalyzer<dpoint>& list);

template <> void CliffsNormalizer<dpoint>::cliffFilters() {
	if (this->checkPrecision()) {
		CornerNormalizer<dpoint> b = CornerNormalizer<dpoint>(*this);
		b.requireMinimumLength(1);
		TurnNormalizer<dpoint> c = TurnNormalizer<dpoint>(b);
		// enabling this is good for circles, bad for certain spirals, sinus and strokes without enough input data
		c.risingJitter(0);
		//
		c.smoothingJitter(0);
		c.risingJitter(0);
	}
	else {
		CornerNormalizer<dpoint> b = CornerNormalizer<dpoint>(*this);
		b.requireMinimumLength(2);
		//// enabling this is good for circles, bad for certain spirals, sinus and strokes without enough input data
		////toBeProcessed.risingJitter(0);
		TurnNormalizer<dpoint> c = TurnNormalizer<dpoint>(b);
		c.smoothingJitter(0);
		//c.risingJitter(0);
	}
}
