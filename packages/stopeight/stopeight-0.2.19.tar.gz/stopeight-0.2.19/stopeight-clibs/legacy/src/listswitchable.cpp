// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listswitchable.h"

//#define debug() QDebug::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

template<> ListSwitchable<dpoint>::ListSwitchable() : ListRotator<dpoint>(){
}


// Note: ALL datamembers of target class destroyed
template<>template<typename F> ListSwitchable<dpoint>::ListSwitchable(F& list) : ListRotator<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<ListSwitchable<dpoint>& >(c);
}

#include "listswitchable.h"
template ListSwitchable<dpoint>::ListSwitchable(ListSwitchable<dpoint>& list);
#include "cliffsanalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(CliffsAnalyzer<dpoint>& list);
#include "areacalculator.h"
template ListSwitchable<dpoint>::ListSwitchable(AreaCalculator<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(ListBase<dpoint>& list);
#include "cornernormalizer.h"
template ListSwitchable<dpoint>::ListSwitchable(CornerNormalizer<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(Calculator<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(ListCopyable<dpoint>& list);
#include "areaanalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(AreaAnalyzer<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(TurnNormalizer<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(AreaNormalizer<dpoint>& list);
template ListSwitchable<dpoint>::ListSwitchable(CliffsNormalizer<dpoint>& list);
#include "corneranalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(CornerAnalyzer<dpoint>& list);
#include "turnanalyzer.h"
template ListSwitchable<dpoint>::ListSwitchable(TurnAnalyzer<dpoint>& list);

// Note: ALL datamembers of target class destroyed
template<>template<typename F> void ListSwitchable<dpoint>::operator=(F& list){
    this->swap(list);
}

template<>template<typename F> void ListSwitchable<dpoint>::operator=(const F& list){
    //REQUIRES PHYSICAL COPY: ERROR MSVC
    //MEMORY LEAK
    ListBase<dpoint> copy = ListBase<dpoint>(list);
    *this = static_cast<ListSwitchable<dpoint> &>(copy);
    //throw std::runtime_error("ListSwitchable assigned with const");
}

#include "cliffscalculator.h"
template void ListSwitchable<dpoint>::operator=(CliffsCalculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const CliffsCalculator<dpoint>& list);
#include "areacalculator.h"
template void ListSwitchable<dpoint>::operator=(AreaCalculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const AreaCalculator<dpoint>& list);
#include "turncalculator.h"
template void ListSwitchable<dpoint>::operator=(TurnCalculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const TurnCalculator<dpoint>& list);
#include "cornercalculator.h"
template void ListSwitchable<dpoint>::operator=(CornerCalculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const CornerCalculator<dpoint>& list);
#include "calculator.h"
template void ListSwitchable<dpoint>::operator=(Calculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const Calculator<dpoint>& list);
#include "spirals.h"
template void ListSwitchable<dpoint>::operator=(Spirals<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const Spirals<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(StraightsCalculator<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const StraightsCalculator<dpoint>& list);
#include "cliffs.h"
template void ListSwitchable<dpoint>::operator=(Cliffs<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const Cliffs<dpoint>& list);
#include "corners.h"
template void ListSwitchable<dpoint>::operator=(Corners<dpoint>& list);
template void ListSwitchable<dpoint>::operator=(const Corners<dpoint>& list);

template <> void ListSwitchable<dpoint>::removeAt(int i) {
    if (i<0) {
        //debug()<<"Illegal position for point removal: "<<i;
        return;
    }
    if (i>this->size()-1) {
        //debug()<<"Illegal position for point removal: "<<i;
        return;
    }
    if ( (i==0 )|| (i==this->size()-1) ){
        //debug() << "WARNING: deleting first or last point in subsegment, pos: "<< this->at(i).position;
    }
    QList<dpoint>::removeAt(i);
    // watch out, this happens AFTER remove
    if ( (i==0 )|| (i==this->size()) ){
        //this has to change to steepest possible
        rotateSegmentToXAxis();
        //this->rotateLastVectorToYAxis();
    }
}
