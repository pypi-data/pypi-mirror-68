// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#include "editorspirals.h"

//#define debug() QDebug(QtDebugMsg)//::QDebug(QtDebugMsg)
//#define debug() QNoDebug()

EditorSpirals::EditorSpirals() : EditorCliffs()
{
}

//EditorSpirals::~EditorSpirals(){
//    EditorBase::~EditorBase();
//}

//toBeProcessed is modifying data.output
void EditorSpirals::process(ListBase<dpoint> &toBeProcessed){
    // use of output is a hack
    if (this->getOutput().size()>0) {
        /* SHARED CLIFFS&SPIRALS */
        QList<dpoint> cliffs;

        /* SPIRALS */
        Spirals<dpoint> spirals = Spirals<dpoint>(toBeProcessed);
        cliffs= Spirals<dpoint>::findSpiralCliffs(spirals);

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

        //hack
        this->setOutput(result);
    } else {
        throw "EditorSpirals::process called without any data";
    }
}

QList<dpoint> EditorSpirals::processSegment(QList<dpoint>::iterator start, QList<dpoint>::iterator end){
    return EditorCliffs::processSegment(start,end);
}
