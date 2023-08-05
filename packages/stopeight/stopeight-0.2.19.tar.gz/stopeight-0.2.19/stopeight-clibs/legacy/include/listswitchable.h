// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LISTSWITCHABLE_H
#define LISTSWITCHABLE_H

#define HIGHPASS_LOW_LIMIT 0.0001

#include "listrotator.h"
//#include <limits>

template<typename T> class ListSwitchable : public ListRotator<dpoint>
{
public:
    ListSwitchable();
    template<typename F> ListSwitchable<T>(F& list);
    //THIS THING AND ALL INHERITING CAN NOT BE COPIED
    template<typename F> void operator=(F& list);
    template<typename F> void operator=(const F& list);


    void removeAt(int i);

};





#endif // LISTSWITCHABLE_H
