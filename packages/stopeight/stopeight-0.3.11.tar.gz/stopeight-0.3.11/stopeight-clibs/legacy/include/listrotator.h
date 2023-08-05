// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LISTROTATOR_H
#define LISTROTATOR_H

// not available on windows:
#ifndef M_PIl
#define M_PIl		3.1415926535897932384626433832795029L  /* pi */
#endif //M_PIl
#ifndef M_El
# define M_El		2.7182818284590452353602874713526625L  /* e */
#endif //M_El
#ifndef M_LOG10El
# define M_LOG10El	0.4342944819032518276511289189166051L  /* log base 10 of e */
#endif //M_LOG10El

//#include <QMatrix>
#include <QtGui/QTransform>

#include "listbase.h"

template<typename T> class ListRotator : public ListBase<T>
{
public:
    ListRotator<T>();
    template<typename F> ListRotator<T>(F& list);
    template<typename F> void operator=(F& list);

    void rotateSegmentToXAxis();
    //void rotateLastVectorToYAxis();
    //void rotateSegmentToSteepest(QPointF lastVector, QPointF startToEndVector);
private:
    void moveRotToZero();
    void rotate(double deg);
    //double getQuadCheckRotation(QPointF first, QPointF second);
};

#endif // LISTROTATOR_H
