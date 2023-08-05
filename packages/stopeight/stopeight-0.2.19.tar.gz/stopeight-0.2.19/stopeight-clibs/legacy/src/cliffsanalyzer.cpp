// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "cliffsanalyzer.h"

template<> CliffsAnalyzer<dpoint>::CliffsAnalyzer() : CliffsNormalizer<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> CliffsAnalyzer<dpoint>::CliffsAnalyzer(F& list) : CliffsNormalizer<dpoint>(list){
    // should be listswitchable
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<CliffsAnalyzer<dpoint>& >(c);
}

#include "areaanalyzer.h"
//area to cliff ok
template CliffsAnalyzer<dpoint>::CliffsAnalyzer(AreaAnalyzer<dpoint>& list);
template CliffsAnalyzer<dpoint>::CliffsAnalyzer(ListCopyable<dpoint>& list);

template <> int CliffsAnalyzer<dpoint>::hasIllegalSegment(){
    ListRotator<dpoint> rotator = ListRotator<dpoint>(*this);
    // has to change to steepest possible?
    rotator.rotateSegmentToXAxis();
    //rotateLastVectorToYAxis();

    for (int i=0;i<rotator.size()-1;i++){
        if ((rotator.at(i+1).rot.x()<=rotator.at(i).rot.x())
                //&&(rotator.at(i+1).rot.y()<HIGHPASS_LOW_LIMIT)
                )
        {
            //debug() << "Illegal Segment found at " << rotator.at(i+1);
            return rotator.at(i+1).position;
        }
    }
    return -1;
}

template<> ListCopyable<dpoint> CliffsAnalyzer<dpoint>::getFirstLegalSegment(){
    CliffsAnalyzer<dpoint> result = CliffsAnalyzer<dpoint>();
    if (this->size()>1){

        bool foundOne=false;
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
            if (result.hasIllegalSegment()!=-1){
                foundOne=true;
                break;
            }
        }
        if (foundOne){
            result.removeLast();
        }
    } else {
        //throw "ListAnalyzer::getFirstLegalSegment: segment size is below 2";
        for (int i=0;i<this->size();i++){
            result<<this->at(i);
        }
    }
    for (int i=0;i<result.size();i++){
        this->removeFirst();
    }

    result.rotateSegmentToXAxis();

    return result;
}

//NEVER USED
//editorcliffs implementation is using getFirstLegalSegment
//FOR REFERENCE
template<> ListCopyable<dpoint> CliffsAnalyzer<dpoint>::getFirstCliff(qreal limit){
    //specialised internally!
    dpoint result = dpoint();

    // from AreaAnalyzer::getFirstArea
    // needs to be and is a COPY
    ListCopyable<dpoint> copy = ListCopyable<dpoint>(*this);
    CliffsAnalyzer<dpoint> calculator = CliffsAnalyzer<dpoint>(copy);

    bool foundOne = false;

    // Spirals getFirstArea implementation was here, now areaanalyzer

    // directional cliffs implementation?
    // first Operation without preceding triangles and areas
    while (calculator.size()>1){
        ListCopyable<dpoint> legalSegment = calculator.getFirstLegalSegment();//cliffs
        //if (count!=0 && legalSegment.size()>0){
        //    legalSegment.removeFirst();
        //}

        if (calculator.size()>1){
            // + tiny bit in between
            calculator.prepend(legalSegment.last());

            AreaAnalyzer<dpoint> dxAreas = AreaAnalyzer<dpoint>(legalSegment);
            // changed to new format limit, start, limit preceding DOES NOT WORK WITH NEW ALGO
            ListCopyable<dpoint> area = dxAreas.getArea(limit,dxAreas.first());//area
            calculator = CliffsAnalyzer<dpoint>(dxAreas);
            //if (count!=0 && legalSegment.size()>0){
            //    area.removeFirst();
            //}
            if (this->last().position!=area.last().position){
                // + tiny bit in between
                calculator.prepend(area.last());
                foundOne = true;
                result=area.last();
            } else {
                //// BUG:
                ////return this->chopCopy(area.last().position, this->last().position);
                //result = this->last();
                //return result;

                //infinite loop break
                break;
            }
        }
    }
    // BUG: catch for calculator.size above
    result=this->last();

    // SHARED by spirals implementation and directional cliffs implementation
    ListCopyable<dpoint> area = ListCopyable<dpoint>();
    if (foundOne){
        ListCopyable<dpoint> util = ListCopyable<dpoint>(*this);
        //area = util.chopCopy(util.first().position,result.position);
        area.clear();
        auto it = util.position_to_iterator(util.first().position,result.position);
        std::copy(it[0],it[1],std::back_inserter(area));
        //area = ListBase<dpoint>(util.chopCopy(util.first().position,result.position));
        //debug()<<"Area has "<<illegalSegmentCounter<<" legal segments.";
    } else {
        area = *this;
    }
    // removing
    for (int i=0;i<area.size();i++){
        this->removeFirst();
    }
    return area;

    // TCT implementation was here, now getFirstCliffTCT

}

//NEVER USED
//editorcliffs implementation is using getFirstLegalSegment
//FOR REFERENCE
/*template<> ListCopyable<dpoint> CliffsAnalyzer<dpoint>::getFirstCliffTCT(qreal limit){
    ListCopyable<dpoint> copy = ListCopyable<dpoint>(*this);
    ListCopyable<dpoint> calculator = ListCopyable(*this);
    // TCT implementation?

    // first Operation without preceding triangles and areas
    while (calculator.size()>1){
        ListCopyable<dpoint> legalSegment = calculator.getFirstLegalSegment();
        //if (count!=0 && legalSegment.size()>0){
        //    legalSegment.removeFirst();
        //}

        if (calculator.size()>1){
            // + tiny bit in between
            calculator.prepend(legalSegment.last());
            ListAnalyzer<dpoint> area = calculator.getArea(limit,legalSegment.sumOfDxAreasRotY(),legalSegment.first());//this->first());
            //if (count!=0 && legalSegment.size()>0){
            //    area.removeFirst();
            //}
            if (this->last().position!=area.last().position){
                // + tiny bit in between
                calculator.prepend(area.last());

                result<<area.last();
            } else {
                // BUG:
                //return this->chopCopy(area.last().position, this->last().position);
                result << this->last();
                return result;
            }
        }
    }
    result<<this->last();
    //return result;
    //------------------------------- Old_implementation --------------------------------------
    // Second Operation with preceding triangle and preceding Area
    if (calculator.size()>1){
      ListAnalyzer<dpoint> legalSegment = calculator.getFirstLegalSegment();
    if (legalSegment.size()>1){
            int pos = legalSegment.last().position;

            // +tiny little triangle between precedent and current
            //precedent
            precedent.removeLast();//tiny little triangle duplicate

            // preceding Area
            preceding += precedent.sumOfDxAreasRotY();

            precedent = legalSegment.getArea(limit,preceding);
            if (pos==precedent.last().position){
                // + tiny bit in between
                calculator.prepend(precedent.last());
            } else {
                return copy.chopCopy(precedent.last().position, this->last().position);
            }
        }
    result<<legalSegment.last();
    }
    // Third Operation with preceding Area(s) plus one preceding triangle
    while (calculator.size()>1){
        ListAnalyzer<dpoint> legalSegment = calculator.getFirstLegalSegment();
        if (legalSegment.size()>1){
            int pos = legalSegment.last().position;

            // +tiny little triangle between precedent and current
            //precedent
            precedent.removeLast();//tiny little triangle duplicate

            // preceding Area
            preceding += precedent.sumOfDxAreasRotY();

            // calculating fixed triangle of preceding operation: only on third operation!
            //precedent.first to precedent.last
            //qreal triangle

            ListAnalyzer<dpoint> precedent = legalSegment.getArea(limit,preceding);
            if (pos==precedent.last().position){
                // + tiny bit in between
                calculator.prepend(precedent.last());
            } else {
                return copy.chopCopy(precedent.last().position, this->last().position);
            }
        }
        result<<legalSegment.last();
    }
    return result;
}*/
