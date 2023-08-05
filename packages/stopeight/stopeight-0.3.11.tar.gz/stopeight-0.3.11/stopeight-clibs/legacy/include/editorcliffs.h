// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef EDITORCLIFFS_H
#define EDITORCLIFFS_H

#include "editorbase.h"
#include "cliffs.h"
#include "spiralsanalyzer.h"

class EditorCliffs : public EditorBase<ListBase<dpoint> >
{
    friend class EditorSpirals;
public:
    EditorCliffs();
    //~EditorCliffs();


protected:
    void process(ListBase<dpoint>& toBeProcessed);

private:
    QList<dpoint> processSegment(QList<dpoint>::iterator start,QList<dpoint>::iterator end);

};

#endif // EDITORCLIFFS_H
