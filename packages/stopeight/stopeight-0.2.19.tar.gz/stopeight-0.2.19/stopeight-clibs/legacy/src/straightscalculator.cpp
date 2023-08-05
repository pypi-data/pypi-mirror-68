// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "straightscalculator.h"

template<> StraightsCalculator<dpoint>::StraightsCalculator() : ListSwitchable<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> StraightsCalculator<dpoint>::StraightsCalculator(F& list) : ListSwitchable<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<StraightsCalculator<dpoint>& >(c);
}

#include "cornernormalizer.h"
template StraightsCalculator<dpoint>::StraightsCalculator(CornerNormalizer<dpoint>& list);
#include "listcopyable.h"
template StraightsCalculator<dpoint>::StraightsCalculator(ListCopyable<dpoint>& list);
#include "areanormalizer.h"
template StraightsCalculator<dpoint>::StraightsCalculator(AreaNormalizer<dpoint>& list);

template <> qreal StraightsCalculator<dpoint>::sumLength(){
    qreal sumLength = 0;
    Calculator<dpoint> calc = Calculator<dpoint>(*this);
    for (int i=0;i<this->size()-1;i++) {
        sumLength += calc.lengthAt(i);
    }
    return sumLength;
}

// being used by triplets
template <> qreal StraightsCalculator<dpoint>::sumRotYFrom(int start){
    qreal sumRotY = 0;
    for (int i=start;i<this->size();i++) {
        sumRotY += this->at(i).rot.y();
    }
    return sumRotY;
}

// being used by checkIfSectionIsStraight
template <> qreal StraightsCalculator<dpoint>::sumOfLinesRotY(){
    qreal sumRotY = 0;
    for (int i=0;i<this->size();i++) {
        sumRotY += fabs(this->at(i).rot.y());
    }
    return sumRotY;
}
