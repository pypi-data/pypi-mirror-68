// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "listrotator.h"

//#define debug() QNoDebug()

template<> ListRotator<dpoint>::ListRotator() : ListBase<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> ListRotator<dpoint>::ListRotator(F& list) : ListBase<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<ListRotator<dpoint>& >(c);
}

template ListRotator<dpoint>::ListRotator(QList<dpoint>& list);
#include "cliffsanalyzer.h"
template ListRotator<dpoint>::ListRotator(CliffsAnalyzer<dpoint>& list);
#include "areaanalyzer.h"
template ListRotator<dpoint>::ListRotator(AreaAnalyzer<dpoint>& list);
template ListRotator<dpoint>::ListRotator(ListBase<dpoint>& list);
template ListRotator<dpoint>::ListRotator(ListCopyable<dpoint>& list);
template ListRotator<dpoint>::ListRotator(TurnNormalizer<dpoint>& list);
template ListRotator<dpoint>::ListRotator(AreaCalculator<dpoint>& list);
template ListRotator<dpoint>::ListRotator(CornerNormalizer<dpoint>& list);
template ListRotator<dpoint>::ListRotator(Calculator<dpoint>& list);
template ListRotator<dpoint>::ListRotator(ListSwitchable<dpoint>& list);
template ListRotator<dpoint>::ListRotator(AreaNormalizer<dpoint>& list);
template ListRotator<dpoint>::ListRotator(CliffsNormalizer<dpoint>& list);
#include "corneranalyzer.h"
template ListRotator<dpoint>::ListRotator(CornerAnalyzer<dpoint>& list);
#include "turnanalyzer.h"
template ListRotator<dpoint>::ListRotator(TurnAnalyzer<dpoint>& list);


// Note: ALL datamembers of target class destroyed
template<>template<typename F> void ListRotator<dpoint>::operator=(F& list){
    this->swap(list);
}

template <> void ListRotator<dpoint>::moveRotToZero(){
    QTransform transMat;

    if (this->size()>0){
        dpoint first = this->first();

        // this translation is just making the numbers look nice
        transMat.reset();
        transMat.translate(-first.rot.x(), -first.rot.y());

        dpoint tmp;
        for (int i=0;i<this->size();i++){
            tmp=this->at(i);
            tmp.rot = tmp.rot*transMat;
            this->replace(i, tmp);
        }
    }
}

template <> void ListRotator<dpoint>::rotate(double deg){
    QTransform transMat;
    dpoint last = this->last();

    transMat.reset();
    //moves to the end point does the rotation and resets to initial position
    transMat.translate(-last.x(), -last.y());
    transMat.rotate(-deg);
    transMat.translate(last.x(), last.y());

    dpoint tmp;
    for (int i=0;i<this->size();i++){
        tmp = this->at(i);
        tmp.rot = tmp * transMat;
        this->replace(i, tmp);
    }

}

template <> void ListRotator<dpoint>::rotateSegmentToXAxis(){
    double rad, deg = 0;

    if (this->size()>1){
        dpoint first = this->first();
        dpoint last = this->last();

        QPointF d = last - first;

        rad = atan2( d.y(),d.x());
        deg = (rad * (180.0 / M_PIl));

//        debug()<<"rotateSegmentToXAxis: Rotating "<<-deg<<" degrees clockwise.";

        rotate(deg);
    }
    moveRotToZero();
}

/*template <> void ListRotator<dpoint>::rotateLastVectorToYAxis(){

    QTransform transMat;
    double rad, deg = 0;

    if (this->size()>2)
    {
        dpoint secondlast = this->at(this->size()-2);
        dpoint last = this->last();

        QPointF d = last - secondlast;

        rad = atan2( d.y(),d.x());
        deg = (rad * (180.0 / M_PIl));

        debug()<<"rotateLastVectorToYAxis: Rotating "<<-deg<<" degrees clockwise.";

        rotate(deg);

        // make correction if segment is upside/down now
        if (this->last().rot.x()<this->first().rot.x()){
            rotate(180);
        }
        moveRotToZero();

    } else {
        rotateSegmentToXAxis();
    }
}*/

/*// letzter - 2.letzter, letzter - erster
template <> double ListRotator<dpoint>::getQuadCheckRotation(QPointF first, QPointF second){
    QPointF d = first;
    QPointF e = second;
    const double little = 0.00000001;//result will defer on position of 1 see ouput below
    double addrot = 0;
    // check for clockwise
    // check for quadrant
    if ( (e.x()>0&&d.x()>0&&d.y()>0&&e.y()<0) ||
         (e.x()>0&&d.x()<0&&d.y()>0&&e.y()>0) ||
         (e.x()<0&&d.x()<0&&d.y()<0&&e.y()>0) ||
         (e.x()<0&&d.x()>0&&d.y()<0&&e.y()<0) ){
        addrot = -90 + little;
    }
    // check for anti-clockwise
    // check for quadrant
    if ( (e.x()<0&&d.x()>0&&d.y()>0&&e.y()>0) ||
         (e.x()<0&&d.x()<0&&d.y()>0&&e.y()<0) ||
         (e.x()>0&&d.x()<0&&d.y()<0&&e.y()<0) ||
         (e.x()>0&&d.x()>0&&d.y()<0&&e.y()>0) ){
        addrot = 90 - little;
    }
    // check for irregular
    if ( (e.x()>0&&d.x()>0&&d.y()<0&&e.y()<0) ||
         (e.x()>0&&d.x()>0&&d.y()>0&&e.y()>0) ||
         (e.x()<0&&d.x()<0&&d.y()>0&&e.y()>0) ||
         (e.x()<0&&d.x()<0&&d.y()<0&&e.y()<0) ){
        addrot = 0 - little;
    }
    if ( (e.x()<0&&d.x()>0&&d.y()<0&&e.y()>0) ||
         (e.x()<0&&d.x()>0&&d.y()>0&&e.y()<0) ||
         (e.x()>0&&d.x()<0&&d.y()>0&&e.y()<0) ||
         (e.x()>0&&d.x()<0&&d.y()<0&&e.y()>0) ){
        addrot = 180 + little;
    }
    return addrot;
}

// letzter - 2.letzter, letzter - erster
// if (this->size()>=2)
// rotateSegmentToSteepest(this->last()-this->at(this->size()-2) , this->last()-this->first() );
template <> void ListRotator<dpoint>::rotateSegmentToSteepest(QPointF lastVector, QPointF startToEndVector){
    QTransform transMat;
    double rad, deg = 0;

    rad = atan2( lastVector.y(), lastVector.x());

    deg = (rad * (180.0 / M_PI));
    deg = deg + getQuadCheckRotation(lastVector,startToEndVector);

    debug()<<"rotateSegmentToSteepest: "<<-deg<<" degrees clockwise";

    rotate(deg);
    moveRotToZero();
}*/

