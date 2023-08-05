// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turnanalyzer.h"

#define SUMLENGTH_FACTOR_SUBDIVISION 1

//#define debug() QNoDebug()

template<> TurnAnalyzer<dpoint>::TurnAnalyzer() : TurnNormalizer<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> TurnAnalyzer<dpoint>::TurnAnalyzer(F& list) : TurnNormalizer<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<TurnAnalyzer<dpoint>& >(c);
}

#include "areanormalizer.h"
template TurnAnalyzer<dpoint>::TurnAnalyzer(AreaNormalizer<dpoint>& list);
template TurnAnalyzer<dpoint>::TurnAnalyzer(CornerNormalizer<dpoint>& list);
template TurnAnalyzer<dpoint>::TurnAnalyzer(ListCopyable<dpoint>& list);
#include "listswitchable.h"
template TurnAnalyzer<dpoint>::TurnAnalyzer(ListSwitchable<dpoint>& list);

template <> ListCopyable<dpoint> TurnAnalyzer<dpoint>::getFirstTriplet(){
    StraightsAnalyzer<dpoint> result = StraightsAnalyzer<dpoint>();
    if (this->size()>1){
        bool foundOne=false;
        qreal sum=0;
        int j = 0;
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
            result.rotateSegmentToXAxis();
            qreal newsum = result.sumRotYFrom(j);
            if ((newsum<0&&newsum>sum) ||
                (newsum>0&&newsum<sum)){
                // check if straight line -> hop over crests!
                // this is allergic to jitter!
                if (result.checkIfSectionIsStraightLine(SUMLENGTH_FACTOR_SUBDIVISION)){
                    // if yes, reset sum? or start over?
                    //reset sum
                    sum = 0;
                    //set j
                    j = i;
                    //not necessary: set result
                } else {
                    foundOne=true;
                    break;
                }
            }
            sum = newsum;
        }
        if (foundOne){
            result.removeLast();
        }
    } else {
        throw "ListAnalyzer::getFirstTriplet: triplet too short for detection";
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
        }
    }
    // removing
    for (int i=0;i<result.size();i++){
        this->removeFirst();
    }

    return result;
}

/*
 Problem: if crest detection not applied, second corner can't be found
 getting the first corner
 get the first triplet from first corner
 get the second triplet from first triplet
 reverse segment of second triplet to first corner
 find first Corner in reversed segment = second corner
 integrate segment of secondCorner and firstCorner to get 1st turn'
 get point in the middle of first triplet and 1st turn'
*/
template <> ListCopyable<dpoint> TurnAnalyzer<dpoint>::getFirstTurnByTriplets(){

    TurnAnalyzer<dpoint> result = TurnAnalyzer<dpoint>();
    ListCopyable<dpoint> origin = ListCopyable<dpoint>(*this);
    ListCopyable<dpoint> copy1 = ListCopyable<dpoint>(*this);
    ListCopyable<dpoint> copy2 = ListCopyable<dpoint>(*this);

    CornerAnalyzer<dpoint> cornerCalculator = CornerAnalyzer<dpoint>(copy1);
    //findTurn: doCorner, findTriplet
    // this has never been rotated, first time in cornerFilters
    cornerCalculator.cornerFilters();
    ListCopyable<dpoint> firstCorner = cornerCalculator.getFirstCorner();
    // we might lose 1 point here: the corner. Prepend 1 point?
    //debug()<<"fresh 1";

    //calculator.freshDataSetFrom(origin);
    TurnAnalyzer<dpoint> calculator = TurnAnalyzer<dpoint>(copy2);


    //debug()<<"Size after: "<<calculator.size();
    if (calculator.size()>4){
        calculator.tripletFilters();
        ListCopyable<dpoint> firstTriplet = calculator.getFirstTriplet();

        if (calculator.size()>2){
            ListCopyable<dpoint> secondTriplet = calculator.getFirstTriplet();
            if (secondTriplet.size()>2) {
                auto it = origin.position_to_iterator(firstCorner.last().position,secondTriplet.last().position);
                auto reverse = ListCopyable<dpoint>();
                std::copy(it[0],it[1],std::front_inserter(reverse));
                // this has to be in triplet detection!
                //if (reverse.checkIfSectionIsStraightLine()){
                // start over!
                //} else {
                //reverse.reverse();
                // get First Corner
                CornerAnalyzer<dpoint> twoTriplets = CornerAnalyzer<dpoint>(reverse);
                twoTriplets.cornerFilters();
                ListCopyable<dpoint> secondCorner = twoTriplets.getFirstCorner();
                it = origin.position_to_iterator(firstCorner.last().position,secondCorner.last().position);
                auto cornerToCorner = ListCopyable<dpoint>();
                std::copy(it[0],it[1],std::front_inserter(cornerToCorner));
                //cornerToCorner.reverse();
                // this check is asymetric, improve!
                if (cornerToCorner.size()>0 && firstTriplet.size()>0){
                    TurnAnalyzer<dpoint> normalized = TurnAnalyzer<dpoint>(cornerToCorner);
                    normalized.tripletFilters();
                    // triplet lost! inline specialization!
                    dpoint turnTwo = normalized.getFirstTriplet().last();
                    dpoint turnOne = firstTriplet.last();
                    ListCopyable<dpoint> container = ListCopyable<dpoint>();
                    // eventually turnLine will have length 1
                    // this belongs into chopcopy
                    //if (turnTwo.position>=turnOne.position){
                    //    container = origin.chopCopy(turnOne.position,turnTwo.position);
                    //inversion
                    //} else if (turnTwo.position<turnOne.position) {
                    //    container = origin.chopCopy(turnTwo.position,turnOne.position);
                    //} else {
                    it = origin.position_to_iterator(turnOne.position,turnTwo.position);
                    container.clear();
                    std::copy(it[0],it[1],std::begin(container));
                    //}
                    CornerNormalizer<dpoint> turnLine = CornerNormalizer<dpoint>(container);
                    for (int i=0;this->at(i).position<=turnLine.getPointInTheMiddle().position;i++){
                        result<<this->at(i);
                    }
                } else {
                    throw "ListAnalyzer::getFirstTurnByTriplets: Reverse triplet too short.";
                    for (int i=0;i<this->size();i++){
                        result<<this->at(i);
                    }
                }
                //}
            } else {
                throw "ListAnalyzer::getFirstTurnByTriplets: Second triplet too short.";
                for (int i=0;i<this->size();i++){
                    result<<this->at(i);
                }
            }
        } else {
            //throw "ListAnalyzer::getFirstTurnByTriplets: Could not find more than 1 triplet.";
            for (int i=0;i<this->size();i++){
                result<<this->at(i);
            }
        }
    } else {
        //throw "ListAnalyzer::getFirstTurnByTriplets: Segment is below 5. too short for detection";
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
        }
    }

    // removing
    for (int i=0;i<result.size();i++){
        this->removeFirst();
    }

    return result;
}
