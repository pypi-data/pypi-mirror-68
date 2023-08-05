// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "editorcliffs.h"

#define debug() QNoDebug()

EditorCliffs::EditorCliffs() : EditorBase<ListBase<dpoint> >()
{
}

//EditorCliffs::~EditorCliffs(){
//    EditorBase::~EditorBase();
//}

//toBeProcessed is modifying data.output
void EditorCliffs::process(ListBase<dpoint> &toBeProcessed){
    if (this->getOutput().size()>0) {
        /* SHARED CLIFFS&SPIRALS */
        Cliffs<dpoint> data = Cliffs<dpoint>(toBeProcessed);

        QList<dpoint> cliffs= Cliffs<dpoint>::findCliffs(data);

        /* SHARED After this cliffs is const */
        const QList<dpoint> constCliffs = cliffs;

        /* SHARED CLIFFS&SPIRALS, But replace cornerMeasuring?? */
        QList<QList<dpoint> > slices= QList<QList<dpoint> >();
        QList<QList<dpoint> >& slicesRef(slices);

        mainIterator(constCliffs,slicesRef);
        const QList<QList<dpoint> > constSlices= slices;

        ListBase<dpoint> result = ListBase<dpoint>();

        /* SPIRALS&CLIFFS check */
        SpiralsAnalyzer<dpoint>::consistencyCheck(constCliffs);

        /* SHARED */
        result = Analyzer<dpoint>::populateTurns(this->getOutput(),constSlices);

        this->setOutput(result);
    } else {
        throw "EditorCliffs::process called without any data";
    }
}

// this is a drop-in replacement for processSegment used for clarifying math
QList<dpoint> EditorCliffs::processSegment(QList<dpoint>::iterator start,QList<dpoint>::iterator end){
    auto list = QList<dpoint>();
    std::copy(start,end,std::back_inserter(list));
    ListRotator<dpoint> cliff = ListRotator<dpoint>(list);
    QList<dpoint> path_section = QList<dpoint>();
    if (cliff.size()>1){
        cliff.rotateSegmentToXAxis();
        //debug()<<"removing illegal points because of illegal segments for debug calc.";
        //cliff.removeIllegalPoints();
        //debug()<<"Points "<<cliff.first().position<<" - "<<cliff.last().position;
        //debug()<<"Number of points in Segment: "<<cliff.length();
        //debug()<<"Length of Curve is: "<<cliff.sumLength();
        //cliff.requireMinimumLength(1);
        //debug()<<"Area of Curve is: "<<cliff.sumOfDxAreasRotY();
        //debug()<<"Spiral-Area of Curve is:"<<cliff.measureSpiral();
        //qreal d = cliff.sumOfDx();
        //qreal d = cliff.lengthFromStartToEnd();
        ////debug()<<"Radius is: "<<d/2<<"; Segment-Radius-Area is: "<<(pow(d/2,2)*(double)M_PIl)/2;
        //debug()<<"Radius is: "<<d/2<<"; Segment-Radius-Area is: "<<ListAnalyzer<dpoint>::area(d,MyLimit);

        ////debug()<<"Diameter is: "<<d<<"; Segment-Diameter-Circumference is: "<<(d*(double)M_PIl);
        //debug()<<"Diameter is: "<<d<<"; Segment-Diameter-Circumference is: "<<ListAnalyzer<dpoint>::circumference(d,MyLimit);

        path_section << cliff.first();
        path_section << cliff.last();
        return path_section;
    } else {
        //throw "EditorCliffs::cornerMeasuring: this is a humongously small cliff.";
        return path_section;
    }
}

// This would be original but it never worked after switching from TCT implementation
/*QList<dpoint> EditorCliffs::processSegment(QList<dpoint> cliff){
    if (cliff.size()>2){
        QList<dpoint> path_section = QList<dpoint>();
        path_section << cliff.first();
        QList<dpoint> turns = Turns<dpoint>::findTurns(cliff);
        //debug()<< "Found "<<turns.size()<<" turns in cliff";
        //for (int i=0;i<turns.size();i++){
        //    debug()<< turns[i];
        //}
        path_section << turns;
        path_section << cliff.last();
        return path_section;
    } else {
        throw "EditorCliffs::processSegment: segment size is below 3.";
    }
}*/

// Not USED
// TCT Implementation
// FOR REFERENCE ONLY
/*const void ShapeMatcher::cliffIterator(const QList<dpoint> constCliffs,ListCalculator<dpoint>& resultRef){
    //for (int i=0;i<constCliffs.size()+1;i++){
    // section commented old_implementation

    // WHEREFROM:
    ListAnalyzer<dpoint> cliff;

        //maemo works: check cliff size
        if (cliff.size()>1){
            //only needed for debugging; crest works with scalar
            ListAnalyzer<dpoint> bugger = cliff;
            bugger.rotateSegmentToXAxis();
            //debug()<<bugger;
            QList<dpoint> crests = ListAnalyzer<dpoint>();
            crests << cliff.first() << cliff.last();

            if (crests.size()>1){
                for (int k=0;k<crests.size()-1;k++){
                    ListAnalyzer<dpoint> crest;
                    //if (k != (crests.size()-2) ) {
                    //    crest = output.chopCopy(crests[k].position,crests[k+1].position-1);
                    //} else {
                    crest = this->data.output.chopCopy(crests[k].position,crests[k+1].position);
                    //}
                    if (crest.size()>1){


                        // don't turn on first corner

                        // WHEREFROM:
                        if (crestCorners.size()>1){
                            // don't turn on last corner
                            for (int j=0;j<crestCorners.size()-1;j++){
                                // don't turn on first corner
                                ListAnalyzer<dpoint> corner;

                                //maemo works: check cliff size
                                if (corner.size()>1){

                                    //debug() << "Before filter turn: ";
                                    corner.normalizeCorners();
                                    corner.normalizeTurns();
                                    //debug() << "After filter turn: ";

                                    dpoint turn = doTurn(corner);
                                    // WHEREFROM:
                                    turns << turn;
                                    resultRef << turn;
                                    // beziers start with cliffs/crests
                                    if (j!=crestCorners.size()-1){
                                        resultRef << crestCorners[j+1];
                                    }
                                }
                            }
                        }

                        // don't do this if it's the last crest: it is done once by the cliff!
                        if (k != crests.size()-2){
                            resultRef << crests[k+1];
                        }
                    }
                }
            }
        }
        //maemo works: check cliff size
        //resultRef << constCliffs[i+1];
    //}

}*/
