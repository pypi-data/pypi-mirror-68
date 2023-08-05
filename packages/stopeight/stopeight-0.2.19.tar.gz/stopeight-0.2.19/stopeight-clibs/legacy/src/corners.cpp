// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "corners.h"

#define debug() QNoDebug()

template<> Corners<dpoint>::Corners() : ListSwitchable<dpoint>() {}

// Note: typename F can be any implementation of ListBase WITHOUT data members
template<>template<typename F> Corners<dpoint>::Corners(F& list) : ListSwitchable<dpoint>(){
    ListSwitchable<dpoint>& c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<Corners<dpoint>& >(c);
}

template Corners<dpoint>::Corners(ListBase<dpoint>& list);

//ShapeMatcher::findCorners
template<> QList<dpoint> Corners<dpoint>::findCorners(ListCopyable<dpoint> toBeProcessed){
    QList<dpoint> result = QList<dpoint>();

    CornerAnalyzer<dpoint> crest = CornerAnalyzer<dpoint>(toBeProcessed);
    // do this once and don't do it anymore for the rest of the journey: rotation inside
    crest.cornerFilters();

    while (crest.size()>0){
        ListCopyable<dpoint> corner = crest.getFirstCorner();
        result<<corner.last();
    }
    // The last one is the end of the crest
    result.removeLast();
    //debug()<<"ShapeMatcher::findCorners: detected "<<result.size()<<" corners in algorithm.";
    return result;
}
