// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turns.h"

//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

template<> Turns<dpoint>::Turns() : ListSwitchable<dpoint>() {}

// Note: typename F can be any implementation of ListBase WITHOUT data members
template<>template<typename F> Turns<dpoint>::Turns(F& list) : ListSwitchable<dpoint>(){
    ListSwitchable<dpoint>& c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<Turns<dpoint>& >(c);
}

template Turns<dpoint>::Turns(ListBase<dpoint>& list);

//ShapeMatcher::findTurns
template<> QList<dpoint> Turns<dpoint>::findTurns(ListCopyable<dpoint> toBeProcessed){
    //debug()<<"Turns::findTurns started with "<<toBeProcessed.size()<<" input points";
    QList<dpoint> result = QList<dpoint>();
    TurnAnalyzer<dpoint> crest = TurnAnalyzer<dpoint>(toBeProcessed);
    // TODO bool foundOne = false;
    while (crest.size()>4){
        ListCopyable<dpoint> triplet = crest.getFirstTurnByTriplets();
        result<<triplet.last();
    }
    // The last one is the end of the crest
    //if (result.size()>1){
    result.removeLast();
    //}
    return result;
}
