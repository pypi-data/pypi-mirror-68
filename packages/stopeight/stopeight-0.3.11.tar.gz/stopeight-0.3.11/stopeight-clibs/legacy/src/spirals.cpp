// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "spirals.h"

//#define debug() QNoDebug()

#define MAX_POINTS 5
//#define LIMIT_TEST M_El
//#define LIMIT_TEST M_PIl
#define LIMIT_ITERATION_STEP 0.1

template<> Spirals<dpoint>::Spirals() : ListSwitchable<dpoint>() {}

// Note: typename F can be any implementation of ListBase WITHOUT data members
template<>template<typename F> Spirals<dpoint>::Spirals(F& list) : ListSwitchable<dpoint>(){
    ListSwitchable<dpoint>& c = static_cast<ListSwitchable<dpoint>& >(list);
    *this= static_cast<Spirals<dpoint>& >(c);
}

template Spirals<dpoint>::Spirals(Spirals<dpoint>& list);
template Spirals<dpoint>::Spirals(ListBase<dpoint>& list);


template<> QList<dpoint> Spirals<dpoint>::findAreas(ListCopyable<dpoint> &stroke, qreal limit){
    AreaAnalyzer<dpoint> spiral = AreaAnalyzer<dpoint>(stroke);

    QList<dpoint> result=QList<dpoint>();

    while (spiral.size()>2){
        //if (stroke.size()>2){
        ListBase<dpoint> area = spiral.getFirstArea(limit);
        if (area.size()>0){
            //result << areas;
            result << area.last();
        }
    }
    //result<<stroke.last();

    // The very last one is the end of the stroke
    if (result.size()>0){
        result.removeLast();
    }
    return result;
}

// TODO use listcopyables
template<> qreal Spirals<dpoint>::findLimit(ListCopyable<dpoint> toBeProcessed){
    QList<dpoint> cliffs;
    qreal MyLimit;
    //Old working:
    //MyLimit = M_El;
    MyLimit = M_PIl;
    //MyLimit = (M_El+M_PIl)/2;
    //MyLimit = 3.135;
    //MyLimit=2*M_PIl/M_El;
    //MyLimit=M_PIl/2;

    // other block:
    //MyLimit=M_PIl/2;
    //MyLimit=0.66666666666666666666666666666666666666666666666666666666666666666666666666 * M_PIl;
    //MyLimit=2*M_PIl/M_El;
    //MyLimit = M_El;

    //throw "ShapeMatcher::process: invalid MyLimit";

    cliffs=findAreas(toBeProcessed,MyLimit);
    cliffs.size();
    if (cliffs.size()>0){
            //debug()<<"Found "<<cliffs.size()<<"cliffs, adjusting limit to current minimum";
            int selector=cliffs.size();
            QList<dpoint> backup;
            qreal backupLimit;
            while (cliffs.size()==(selector)){
                backupLimit = MyLimit;
                backup=cliffs;
                MyLimit -= LIMIT_ITERATION_STEP;
                cliffs=findAreas(toBeProcessed,MyLimit);
            }
            MyLimit=backupLimit;
            cliffs=backup;

    }
    //if ( (cliffs.size()!=0) && (fmod(cliffs.size(),2) == 0)){
    //    throw "ShapeMatcher::verify: Inconsistency: even number of cliffs not allowed";
    //}
    return MyLimit;
}

template<> QList<dpoint> Spirals<dpoint>::findSpiralCliffs(ListCopyable<dpoint> toBeProcessed){
    ListCopyable<dpoint> forward = ListCopyable<dpoint>(toBeProcessed);

    //qreal frontSpiral= toBeProcessed.measureSpiral();
    //debug()<<"Forward Spiral Size is: "<<frontSpiral;
    qreal limit = findLimit(toBeProcessed);
    //debug()<<"Limit from forward analysis is: "<<limit;

    // TODO
    //this should be a copy!
    Analyzer<dpoint> reversed = Analyzer<dpoint>(toBeProcessed);
    //reversed.tripletFilters();
    reversed.reverseOrder();
    //qreal backSpiral= reversed.measureSpiral();
    //debug()<<"Backward Spiral Size is: "<<backSpiral;
    ListCopyable<dpoint> backward = ListCopyable<dpoint>(reversed);
    qreal backLimit = findLimit(backward);
    //debug()<<"Limit from backward analysis is: "<<backLimit;
    //if (static_cast<int>(frontSpiral)!=static_cast<int>(backSpiral)){
        //throw "ShapeMatcher::process: spiral-size front/back not equal";
    //}

    // change: use reference?
    QList<dpoint>* cliffs = new QList<dpoint>;
    if (limit!=backLimit){
        //debug()<< "ShapeMatcher::process: different limits found, using larger";
        if (backLimit>limit){
            *cliffs = findAreas(backward,backLimit);
            //if (cliffs->size()>0){
            Calculator<dpoint> calc = Calculator<dpoint>(*cliffs);
            calc.reverse();
            *cliffs = calc;
            //}
        } else {
            *cliffs = findAreas(forward,limit);
        }
    } else {
        //debug()<<"******************* findAreas::Main **********************";
        *cliffs = findAreas(forward,limit);
    }
    return *cliffs;
}

