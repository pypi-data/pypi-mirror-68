// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef AREAANALYZER_H
#define AREAANALYZER_H

#include "areanormalizer.h"
#include "cliffsanalyzer.h"
#include "listcopyable.h"

template<typename T> class AreaAnalyzer : public AreaNormalizer<T>
{
public:
    AreaAnalyzer<T>();
    template<typename F> AreaAnalyzer<T>(F& list);

    ListBase<dpoint> getFirstArea(qreal limit);

    // new Area function
    ListCopyable<dpoint> getArea(qreal limit,QPointF START,qreal preceding=0);
protected:

    // Segment-Radius-Area; should be non-static with diameter=lengthStartToEnd from instance
    static qreal area(qreal diameter, qreal base);


};

#endif // AREAANALYZER_H
