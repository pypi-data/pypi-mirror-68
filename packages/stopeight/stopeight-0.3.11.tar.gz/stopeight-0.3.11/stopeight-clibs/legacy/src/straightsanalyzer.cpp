// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "straightsanalyzer.h"

#define debug() QNoDebug()

template<> StraightsAnalyzer<dpoint>::StraightsAnalyzer() : StraightsCalculator<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> StraightsAnalyzer<dpoint>::StraightsAnalyzer(F& list) : StraightsCalculator<dpoint>(list){
    ListBase<dpoint> c = static_cast<ListBase<dpoint>& >(list);
    *this= static_cast<StraightsAnalyzer<dpoint>& >(c);
}

#include "areanormalizer.h"
template StraightsAnalyzer<dpoint>::StraightsAnalyzer(AreaNormalizer<dpoint>& list);
template StraightsAnalyzer<dpoint>::StraightsAnalyzer(CornerNormalizer<dpoint>& list);

template<> bool StraightsAnalyzer<dpoint>::checkIfSectionIsStraightLine(qreal sumLengthFactor){
    ListCopyable<dpoint> section;
    for (int i=0;i<this->size();i++){
        section << this->at(i);
    }
    // maybe we should remove values that could jeoparize integration
    // This is a hack!
    section.removeIllegalPoints();

    // Check if segment is a line
    StraightsCalculator<dpoint> line = StraightsCalculator<dpoint>(section);
    //if ( sumLength/(1+1/3)>sumRotY ) {
    if ( line.sumLength()*sumLengthFactor>line.sumOfLinesRotY() ) {
        // It is a straight line!
        return true;
    } else {
        return false;
    }
}
