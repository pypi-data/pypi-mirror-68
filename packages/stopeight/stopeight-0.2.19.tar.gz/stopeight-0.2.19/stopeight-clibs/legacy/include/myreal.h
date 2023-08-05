// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef MYREAL_H
#define MYREAL_H

//#include <QtCore/QString>
#include <QtCore/qglobal.h>
#include <string>
#include <limits>
#include <cmath>

class MyReal
{
public:
    MyReal(qreal number);
    std::string strValue(){
        if (value != value){
            return std::string("NaN");
        } else if (value > std::numeric_limits<qreal>::max()){
            return std::string("+Inf");
        } else if (value < -std::numeric_limits<qreal>::max()){
            return std::string("-Inf");
        } else {
            return std::string("");
        }
    }
    bool checkIfValid(){
        std::string val = strValue();
        if ( val==std::string("NaN") || val==std::string("+Inf") || val==std::string("-Inf") ){
            return false;
        } else {
            return true;
        }
    }
    bool isInt(){
        if (fmod(value,1) == 0){
            return true;
        }
        return false;
    }
private:
    qreal value;
};

#endif // MYREAL_H
