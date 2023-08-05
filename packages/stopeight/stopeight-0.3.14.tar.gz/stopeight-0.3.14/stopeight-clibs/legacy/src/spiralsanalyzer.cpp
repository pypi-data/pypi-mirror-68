// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "spiralsanalyzer.h"

//#define debug() QNoDebug()

template<> SpiralsAnalyzer<dpoint>::SpiralsAnalyzer() : SpiralsCalculator<dpoint>() {}

// Note: ALL datamembers of target class destroyed
template<>template<typename F> SpiralsAnalyzer<dpoint>::SpiralsAnalyzer(F& list) : SpiralsCalculator<dpoint>(list){
    *this = static_cast<SpiralsAnalyzer<dpoint>& >(list);
}

template<> bool SpiralsAnalyzer<dpoint>::consistencyCheck(QList<dpoint> cliffs){
    //debug()<<"We have "<< cliffs.size() << " cliffs in input.";
	//if (cliffs.size()!=0 && fmod(cliffs.size(),2) == 0){
    if (cliffs.size()!=0 && (cliffs.size()%2) == 0){
        //debug()<< "ShapeMatcher::verify: ";
        throw legacy::alg_logic_error("Inconsistency: even number of cliffs not allowed",__FILE__,"");
               //C++11
        //throw legacy::alg_logic_error("Inconsistency: even number of cliffs not allowed",__FILE__,__func__);
    } else {
        return true;
    }
    return false;
}




