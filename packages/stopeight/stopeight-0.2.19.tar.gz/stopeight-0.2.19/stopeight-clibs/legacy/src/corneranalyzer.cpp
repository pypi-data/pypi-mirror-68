// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "corneranalyzer.h"

#define debug() QNoDebug()

template<> CornerAnalyzer<dpoint>::CornerAnalyzer() : CornerNormalizer<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> CornerAnalyzer<dpoint>::CornerAnalyzer(F& list) : CornerNormalizer<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<CornerAnalyzer<dpoint>& >(c);
}

#include "areanormalizer.h"
template CornerAnalyzer<dpoint>::CornerAnalyzer(AreaNormalizer<dpoint>& list);
template CornerAnalyzer<dpoint>::CornerAnalyzer(CornerNormalizer<dpoint>& list);
template CornerAnalyzer<dpoint>::CornerAnalyzer(ListCopyable<dpoint>& list);

template <> ListCopyable<dpoint> CornerAnalyzer<dpoint>::getFirstCorner(){
    Analyzer<dpoint> result = Analyzer<dpoint>();

    // used to be >1
    if (this->size()>3){
        //careful!
        result << this->at(0) << this->at(1) << this->at(2);

        // changed from this to calc
        CliffsCalculator<dpoint> calc = CliffsCalculator<dpoint>(*this);
        for (int i=3;i<calc.size();i++){
            if (calc.deriv1Crossed(i)){
                break;
            }
            result << calc.at(i);
        }

    } else {
        //throw "ListAnalyzer::getFirstCorner: Segment is below 4. too short for detecting corners.";
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
        }
    }

    // removing
    for (int i=0;i<result.size();i++){
        this->removeFirst();
    }

    // don't ever rotate in here!

    return result;
}
