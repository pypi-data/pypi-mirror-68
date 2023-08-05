// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "analyzer.h"

#define debug() QNoDebug()

template<> Analyzer<dpoint>::Analyzer() : Calculator(){}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> Analyzer<dpoint>::Analyzer(F& list) : Calculator(list) {
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    // ListCopyable to Analyzer NOT ok
    *this= static_cast<Analyzer<dpoint>& >(c);
    //*this = static_cast<Analyzer<dpoint>& >(list);
}

template Analyzer<dpoint>::Analyzer(Analyzer<dpoint>& list);
template Analyzer<dpoint>::Analyzer(ListBase<dpoint>& list);
template Analyzer<dpoint>::Analyzer(ListCopyable<dpoint>& list);
template Analyzer<dpoint>::Analyzer(QList<dpoint>& list);

// Sould only be allowed in ListCopyable
// only call ONCE
template<> void Analyzer<dpoint>::reverseOrder(){
    ListSwitchable<dpoint> reversed= ListSwitchable<dpoint>();
    int pointer = 0;
    for (int i=this->size()-1;i>=0;i--){
        dpoint point = this->at(i);
        point.position=pointer;
        reversed << point;
        pointer++;
    }
    this->clear();
    this->append(reversed);
}

template<> Calculator<dpoint> Analyzer<dpoint>::populateTurns(ListBase<dpoint> &originalData, const QList<QList<dpoint> > slices){
    Calculator<dpoint> result;
    for (int k=0;k<slices.size();k++){
        for (int l=0;l<slices[k].size()-1;l++){
            result << slices[k][l];
            // this is for debugging turn detection
            ListCopyable<dpoint> iter = ListCopyable<dpoint>(originalData);
            //ListBase<dpoint> lst = iter.chopCopy(slices[k][l].position,slices[k][l+1].position);
            auto it = iter.position_to_iterator(slices[k][l].position,slices[k][l+1].position);
            auto lst = ListBase<dpoint>();
            std::copy(it[0],it[1],std::back_inserter(lst));
            CornerNormalizer<dpoint> mid = CornerNormalizer<dpoint>(lst);
            auto middle = mid.getPointInTheMiddle();
            middle.position = -1;
            result << middle;
            //result << mid.getPointInTheMiddle();
        }
        if ((k==slices.size()-1) && (slices[k].size()>0)){
            result << slices[k].last();
        }
    }
    return result;
}
