// Copyright (C) 2009-2015 Specific Purpose Software GmbH

#ifndef RENDER_H
#define RENDER_H

//#include <QDebug>

//used for vector math
#include <QtGui/QVector2D>
#include <QtCore/QLineF>

#include "dpoint.h"

struct render
{
public:

#if defined(DEBUG) || defined(_DEBUG)
    static QPointF controlFromCorner(QPointF point1, QPointF point2, QPointF point3);
    static QPointF heightedControlFromCorner(QPointF point1, QPointF point2, QPointF point3);
#endif

	static QList<QPointF> quadraticbeziers(QPointF turn1, QPointF corner, QPointF turn2);

    static QList<QList<QPointF> > TCTPath(QList<QPointF> se_stroke_path);

private:
#if defined(DEBUG) || defined(_DEBUG)
	static QList<QPointF> constructCubicControlPointsFromControlPoint(QPointF point1, QPointF point2, QPointF point3);
#endif

	static QList<QPointF> constructCubicControlPointsFromCorner(QPointF point1, QPointF point2, QPointF point3);

	static QPointF cornerFromControl(QPointF point1, QPointF point2, QPointF point3);

	static QPointF dividedBase(QPointF point1, QPointF point2, QPointF point3);

    static qreal getAngleOfPoint2(QPointF point1, QPointF point2, QPointF point3);

    static QLineF getSeitenhalbierende(QPointF point1, QPointF point2, QPointF point3);

	//	static bool goneCubic(QPointF point1, QPointF point2, QPointF point3);

	//	static bool isHyperbolic(QPointF point1, QPointF point2, QPointF point3);
};

#endif // RENDER_H
