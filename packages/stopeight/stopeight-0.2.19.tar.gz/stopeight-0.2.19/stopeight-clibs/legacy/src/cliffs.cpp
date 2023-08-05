// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffs.h"

//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
#define debug() QNoDebug()

template<> Cliffs<dpoint>::Cliffs() : ListSwitchable<dpoint>() {}

// Note: typename F can be any implementation of ListBase WITHOUT data members
template<>template<typename F> Cliffs<dpoint>::Cliffs(F& list) : ListSwitchable<dpoint>(){
    ListSwitchable<dpoint>& c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<Cliffs<dpoint>& >(c);
}

template Cliffs<dpoint>::Cliffs(ListBase<dpoint>& list);

//ShapeMatcher::findCliffs
template<> QList<dpoint> Cliffs<dpoint>::findCliffs(ListCopyable<dpoint> toBeProcessed){
    //test for illegalPointRemoval
    QList<dpoint> result=QList<dpoint>();
    CliffsAnalyzer<dpoint> calculator = CliffsAnalyzer<dpoint>(toBeProcessed);
    while (calculator.size()>2) {
        calculator.cliffFilters();
        //older
        ListCopyable<dpoint> cliff = calculator.getFirstLegalSegment();
        //or newer impl?
        //ListCopyable<dpoint> cliff = calculator.getFirstCliff();
        result << cliff.last();
    }
    // The last one is the end of the stroke
    result.removeLast();
    return result;
}
