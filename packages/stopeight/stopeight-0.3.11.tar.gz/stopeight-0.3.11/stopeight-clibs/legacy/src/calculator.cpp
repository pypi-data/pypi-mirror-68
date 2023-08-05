// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "calculator.h"

template<> Calculator<dpoint>::Calculator() : ListSwitchable<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> Calculator<dpoint>::Calculator(F& list) : ListSwitchable<dpoint>(){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<Calculator<dpoint>& >(c);
}

template Calculator<dpoint>::Calculator(Calculator<dpoint>& list);
#include "straightscalculator.h"
template Calculator<dpoint>::Calculator(StraightsCalculator<dpoint>& list);
#include "cornernormalizer.h"
template Calculator<dpoint>::Calculator(CornerNormalizer<dpoint>& list);
template Calculator<dpoint>::Calculator(ListBase<dpoint>& list);
#include "analyzer.h"
template Calculator<dpoint>::Calculator(Analyzer<dpoint>& list);
#include "listcopyable.h"
template Calculator<dpoint>::Calculator(ListCopyable<dpoint>& list);
template Calculator<dpoint>::Calculator(QList<dpoint>& list);

template <> qreal Calculator<dpoint>::lengthOf(QPointF difference){
    return sqrt(pow(difference.x(),2)+pow(difference.y(),2));
}

template <> qreal Calculator<dpoint>::lengthAt(int position){
    QListIterator<dpoint> i(*this);
    if (i.findNext(this->at(position))) {
        dpoint point1;
        if (i.hasPrevious()){
            point1 = i.previous();
            if (i.hasNext()){
                i.next();
                if (i.hasNext()){
                    dpoint point2 = i.next();
                    dpoint point = point2-point1;
                    return lengthOf(point);
                } else {
                    return 0;
                }
            } else {
                return 0;
            }

        } else {
            return 0;
        }

    } else {
        return 0;
    }
}

template <> void Calculator<dpoint>::reverse(){
    ListSwitchable<dpoint> reversed= ListSwitchable<dpoint>();
    for (int i=this->size()-1;i>=0;i--){
        reversed << this->at(i);
    }
    this->clear();
    this->append(reversed);
}
