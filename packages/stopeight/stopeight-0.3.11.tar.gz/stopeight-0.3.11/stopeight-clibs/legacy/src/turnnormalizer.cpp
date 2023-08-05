// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "turnnormalizer.h"

template<> TurnNormalizer<dpoint>::TurnNormalizer() : TurnCalculator<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> TurnNormalizer<dpoint>::TurnNormalizer(F& list) : TurnCalculator<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<TurnNormalizer<dpoint>& >(c);
}

#include "areanormalizer.h"
template TurnNormalizer<dpoint>::TurnNormalizer(AreaNormalizer<dpoint>& list);
template TurnNormalizer<dpoint>::TurnNormalizer(CornerNormalizer<dpoint>& list);
#include "listcopyable.h"
template TurnNormalizer<dpoint>::TurnNormalizer(ListCopyable<dpoint>& list);
#include "listswitchable.h"
template TurnNormalizer<dpoint>::TurnNormalizer(ListSwitchable<dpoint>& list);

template <> void TurnNormalizer<dpoint>::smoothingJitter(int pos){
    bool foundOne = false;
    for (int i=pos;i<this->size()-3;i++){
        //if ( (this->sumOfRegressionAt(i) <= 0.5) &&
        if (
             (!this->isRegLineThroughAt(i)) ){
        //if (this->isJitterAt(i) == true) {
            this->removeAt(i+1);
            // danger index change
            this->removeAt(i+1);
            foundOne=true;
            break;
        }
    }
    if (foundOne){
        smoothingJitter(pos+1);
    }
}

template <> void TurnNormalizer<dpoint>::risingJitter(int pos){
    bool foundOne = false;
    for (int i=pos;i<this->size()-3;i++){
        //if ( (this->sumOfRegressionAt(i) <= 0.5) &&
        if (
             (this->isRegLineThroughAt(i)) ){
        //if (this->isJitterAt(i) == true) {
            this->removeAt(i+1);
            // danger index change
            this->removeAt(i+1);
            //this->removeAt(i);
            foundOne=true;
            break;
        }
    }
    if (foundOne){
        risingJitter(pos+1);
    }
}

template <> void TurnNormalizer<dpoint>::tripletFilters(){
	// CHECKPRECISION?!
    TurnNormalizer<dpoint> b = TurnNormalizer<dpoint>(*this);
    //this->risingJitter(0);
    b.smoothingJitter(0);
    //only corners and turns need rotation: derivative
    // rotation is absolutely needed if using crossing 0. getFirstTurn contains rotation in point removal
    //remainingSlice.rotateSegmentToXAxis();
}
