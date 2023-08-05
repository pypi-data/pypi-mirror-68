// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

//#ifndef CORNERS_H
//#define CORNERS_H

#include "listswitchable.h"
#include "listcopyable.h"
#include "corneranalyzer.h"

template<typename T> class Corners : public ListSwitchable<T>
{
public:
    Corners<T>();
    template<typename F> Corners<T>(F& list);

    // Note: These only work as expected, if crests have been sliced. Otherwise: Only 1st result reliable
    static QList<dpoint> findCorners(ListCopyable<dpoint> toBeProcessed);

};

//#endif // CORNERS_H
