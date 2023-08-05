// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listcopyable.h"

//#define debug() QNoDebug()

template<> ListCopyable<dpoint>::ListCopyable() : ListBase<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> ListCopyable<dpoint>::ListCopyable(F& list): ListBase<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this = static_cast<ListCopyable<dpoint>& >(c);
}

// Note: We only make a copy if it's been casted
template<>template<> ListCopyable<dpoint>::ListCopyable(ListCopyable<dpoint>& list) :ListBase<dpoint>(list){
//    debug()<<"ListCopyable::ListCopyable assignment"<<list.size();

    *this = list;
}

//template ListCopyable<dpoint>::ListCopyable(ListCopyable<dpoint>& list);
template ListCopyable<dpoint>::ListCopyable(ListBase<dpoint>& list);
#include "areaanalyzer.h"
template ListCopyable<dpoint>::ListCopyable(AreaAnalyzer<dpoint>& list);
#include "spirals.h"
template ListCopyable<dpoint>::ListCopyable(Spirals<dpoint>& list);
#include "analyzer.h"
template ListCopyable<dpoint>::ListCopyable(Analyzer<dpoint>& list);
template ListCopyable<dpoint>::ListCopyable(AreaCalculator<dpoint>& list);
template ListCopyable<dpoint>::ListCopyable(CliffsAnalyzer<dpoint>& list);
#include "cliffs.h"
template ListCopyable<dpoint>::ListCopyable(Cliffs<dpoint>& list);
#include "straightsanalyzer.h"
template ListCopyable<dpoint>::ListCopyable(StraightsAnalyzer<dpoint>& list);
template ListCopyable<dpoint>::ListCopyable(TurnNormalizer<dpoint>& list);
template ListCopyable<dpoint>::ListCopyable(QList<dpoint>& list);
#include "turnanalyzer.h"
template ListCopyable<dpoint>::ListCopyable(TurnAnalyzer<dpoint>& list);

/*template<> ListCopyable<dpoint> ListCopyable<dpoint>::chopCopy(int startPosition, int endPosition){
    ListCopyable<dpoint> filet = ListCopyable<dpoint>();
    for (int i=0;i<this->size();i++){
        if ((this->at(i).position >= startPosition &&
             this->at(i).position <= endPosition) ||
            // this is for reversed pieces, should work...?
            (this->at(i).position <= startPosition &&
             this->at(i).position >= endPosition)
            ){
            filet << this->at(i);
        }
    }
    return filet;
}*/

template <> ArrayOfTwoQListDpointIterators ListCopyable<dpoint>::position_to_iterator(int startPosition,int endPosition){
    auto start = size_t(startPosition);
    auto end = size_t(endPosition);
    if (start > end)
        throw std::out_of_range("Trying to chop from reverse.");
    auto first = std::begin(*this)+(start-size_t(std::begin(*this)->position));
    auto last = std::begin(*this)+(end-size_t(std::begin(*this)->position));
    auto chop_length = std::distance(first,last);
    if ((end-start)!= chop_length){
        throw std::length_error("ListCopyable is missing elements. Use full copy instead.");
    } else {
        return ArrayOfTwoQListDpointIterators{first,last};
    }
}
template ArrayOfTwoQListDpointIterators ListCopyable<dpoint>::position_to_iterator(int startPosition, int endPosition);


/*template <> void ListCopyable<dpoint>::reverse(){
    ListCopyable<dpoint> reversed= ListCopyable<dpoint>();
    for (int i=this->size()-1;i>=0;i--){
        reversed << this->at(i);
    }
    this->clear();
    this->append(reversed);
}*/

template <> void ListCopyable<dpoint>::removeIllegalPoints(){
//    debug() << "Before removeIllegalPoints: " <<this->size();
    CliffsAnalyzer<dpoint> cliff = CliffsAnalyzer<dpoint>(*this);
    while (cliff.hasIllegalSegment()!=-1){
        for (int i=0;i<cliff.size();i++){
            if (cliff.at(i).position == cliff.hasIllegalSegment()){
                //debug() << "removeIllegalPoints: "<<"Removed point "<<this->at(i)<<".";
                cliff.removeAt(i);
                break;
            }
        }
    }
//    debug() << "After removeIllegalPoints: " <<this->size();
}
