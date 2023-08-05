// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef CALCULATOR_H
#define CALCULATOR_H

#include "listswitchable.h"


template<typename T> class Calculator : public ListSwitchable<T>
{
public:
    Calculator<T>();
    template<typename F> Calculator<T>(F& list);

    qreal lengthAt(int i);

    // Note: this is simple reversal. it is not checking order. Should be static.
    void reverse();

    static qreal lengthOf(QPointF difference);


};

#endif // CALCULATOR_H
