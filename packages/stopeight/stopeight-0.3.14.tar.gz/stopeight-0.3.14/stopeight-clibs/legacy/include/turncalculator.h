// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef TURNCALCULATOR_H
#define TURNCALCULATOR_H

#include "listswitchable.h"

#define REGH1 true
#define REGH2 false

template<typename T> class TurnCalculator : public ListSwitchable<T>
{
public:
    TurnCalculator<T>();
    template<typename F> TurnCalculator<T>(F& list);

    bool isRegLineThroughAt(int i);

private:
    qreal regH1At(int i);
    qreal regH2At(int i);
    // has performance issues and is being used by regH1At and regH2At above
    qreal getRegressionValueFor2Points(int pos, bool value);

};

#endif // TURNCALCULATOR_H
