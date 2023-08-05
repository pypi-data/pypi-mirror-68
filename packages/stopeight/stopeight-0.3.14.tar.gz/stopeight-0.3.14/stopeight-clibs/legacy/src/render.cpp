// Copyright (C) 2009-2015 Specific Purpose Software GmbH

#include "render.h"

//#define debug() QDebug::QDebug(QtDebugMsg)
#define debug() QNoDebug()

#if defined(DEBUG) || defined(_DEBUG)

/* Old version using height */
QPointF render::heightedControlFromCorner(QPointF point1, QPointF point2, QPointF point3){
    QLineF one_three,normal,vector;
    QPointF* intersection = new QPointF();
    one_three = QLineF(point1,point3);
    normal = one_three.normalVector();
    normal.translate(point2-point1);
    normal.intersect(one_three, intersection);
    vector = QLineF(*intersection,point2);
    vector.setLength(vector.length()*2);
    return vector.p2();
}

/* new version using middle */
QPointF render::controlFromCorner(QPointF point1, QPointF point2, QPointF point3){
QLineF sidehalf=render::getSeitenhalbierende(point1,point2,point3);
sidehalf.setLength(sidehalf.length()*-1);
return sidehalf.p2();
}

QList<QPointF> render::constructCubicControlPointsFromControlPoint(QPointF point1, QPointF point2, QPointF point3){
QPointF corner = render::cornerFromControl(point1,point2,point3);
return render::constructCubicControlPointsFromCorner(point1,corner,point3);
}

#endif

/* starting with point in triangle! */
//QLineF render::getSeitenhalbierende(QPointF point1, QPointF point2, QPointF point3){
//    QLineF one_three,vector;
//    one_three = QLineF(point1,point3);
//    one_three.setLength(one_three.length()/2);
//    vector = QLineF(point2,one_three.p2());
//    return vector;
//}

/* Old version using Winkelhalbierende */
QLineF render::getSeitenhalbierende(QPointF point1, QPointF point2, QPointF point3){
    QLineF line1,line2,one_three,vector;
    one_three = QLineF(point1,point3);
    //one_three.setLength(one_three.length()/2);
    line1 = QLineF(point2,point1);
    line2 = QLineF(point2,point3);
    qreal angle = line1.angleTo(line2);
    line1.setAngle(line1.angle()+angle/2);
    QPointF* intersection = new QPointF();
    line1.intersect(one_three,intersection);
    vector = QLineF(point2,*intersection);
    return vector;
}

qreal render::getAngleOfPoint2(QPointF point1, QPointF point2, QPointF point3){
    QLineF line1,line2;
    line1 = QLine(point2.toPoint(),point1.toPoint());
    line2 = QLine(point2.toPoint(),point3.toPoint());
    qreal angle = line1.angleTo(line2);
    return angle;
}

QPointF render::dividedBase(QPointF point1, QPointF point2, QPointF point3){
    QLineF base,normal;
    base = QLine(point1.toPoint(),point3.toPoint());
    normal = base.normalVector();
    normal.translate(point2-point1);
    QPointF* intersection = new QPointF();
    base.intersect(normal,intersection);
    return *intersection;
}

QList<QPointF> render::quadraticbeziers(QPointF turn1, QPointF corner, QPointF turn2)
{
    QList<QPointF> controlPoints = render::constructCubicControlPointsFromCorner(turn1, corner, turn2);
    QPointF leftCorner = render::cornerFromControl(turn1, controlPoints[0], corner);
    QPointF rightCorner = render::cornerFromControl(corner, controlPoints[1], turn2);

    QList<QPointF> leftControls = render::constructCubicControlPointsFromCorner(turn1, leftCorner, corner);

    QList<QPointF> rightControls = render::constructCubicControlPointsFromCorner(corner, rightCorner, turn2);

	QList<QPointF> arc = QList<QPointF>();
	arc << turn1 << leftControls[0] << leftCorner << leftControls[1] << corner << rightControls[0] << rightCorner << rightControls[1] << turn2;
	return arc;
}

QList<QList<QPointF> > render::TCTPath(QList<QPointF> se_stroke_path) {
	QList<QList<QPointF> > arcs = QList<QList<QPointF> >();
	if (se_stroke_path.size() > 0) {
		for (int i = 0; i < se_stroke_path.size() - 2; i = i + 2) {

			QPointF point1, point2, point3;
			point1 = se_stroke_path.at(i).toPoint();
			point2 = se_stroke_path.at(i + 1).toPoint();
			point3 = se_stroke_path.at(i + 2).toPoint();

			QList<QPointF> arc = render::quadraticbeziers(point1, point2, point3);

			arcs.append(arc);

		}
	}
	return arcs;
}

/* Old version using two thirds */
QList<QPointF> render::constructCubicControlPointsFromCorner(QPointF point1, QPointF point2, QPointF point3){
    qreal rotation = render::getAngleOfPoint2(point1,point2,point3)/2;
    QLineF line1,line2,line3;
    line1 = QLine(point2.toPoint(),point1.toPoint());
    line2 = QLine(point2.toPoint(),point3.toPoint());
    //line3 = QLine(point1.toPoint(),point3.toPoint());
    line1.setAngle(line1.angle()+rotation-90);
    line2.setAngle(line2.angle()-rotation+90);
    QPointF base = render::dividedBase(point1,point2,point3);
    qreal length1,length2;
    length1=QLineF(base,point1.toPoint()).length();
    length2=QLineF(base,point3.toPoint()).length();
    //qreal factor1,factor2;
    //factor1 = (length1/line3.length());
    //factor2= (length2/line3.length());
    line1.setLength(length1*2/3);
    line2.setLength(length2*2/3);
    //QPointF base = render::dividedBase(point1,point2,point3);
    //debug() << "Length " << QLineF(point1.toPoint(),point3.toPoint()).length() << " equals" << baselengths[0] << " + " << baselengths[1];
    QList<QPointF> result;
    result.append(line1.p2());
    result.append(line2.p2());
    return result;
}

QPointF render::cornerFromControl(QPointF point1, QPointF point2, QPointF point3){
    QLineF section = render::getSeitenhalbierende(point1,point2,point3);
    section.setLength(section.length()/2);
    return section.p2();
}

/* New version using Menelaos */
/*QList<QPointF> render::constructCubicControlPointsFromCorner(QPointF point1, QPointF point2, QPointF point3){
    QLineF midSection = render::getSeitenhalbierende(point1,point2,point3);
    QLineF normal = midSection.normalVector();
    QPointF quadControl = render::controlFromCorner(point1,point2,point3);
    QLineF line1 = QLine(quadControl.toPoint(),point1.toPoint());
    QLineF line2 = QLine(quadControl.toPoint(),point3.toPoint());
    QPointF *intersection1 = new QPointF();
    line1.intersect(normal,intersection1);
    QPointF *intersection2 = new QPointF();
    line2.intersect(normal,intersection2);
    QList<QPointF> result;
    result.append(*intersection1);
    result.append(*intersection2);
    return result;
}*/

/*bool render::isHyperbolic(QPointF point1, QPointF point2, QPointF point3){
    QPointF sideHalf = render::getSeitenhalbierende(point1,point2,point3).p2();
    if ((render::getAngleOfPoint2(point1,point2,sideHalf)>90)||
        render::getAngleOfPoint2(sideHalf,point2,point3)>90){
        return true;
    } else {
        return false;
    }
}*/

/*bool render::goneCubic(QPointF point1, QPointF point2, QPointF point3){
    qreal angle = render::getAngleOfPoint2(point1,point2,point3);
    if (angle>180){
        angle=360 - angle;
    }
    debug() << "Angle: " << angle;
    if (angle>120||angle==0){//should be 135 or 120?
        return false;
    } else {
        return true;
    }
}*/
