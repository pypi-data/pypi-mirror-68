// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef EditorBase_H
#define EditorBase_H

// Will move into implementations when all are completed, or make interface configuration call?
#define MAX_POINTS 5
//#define LIMIT_TEST M_El
//#define LIMIT_TEST M_PIl
#define LIMIT_ITERATION_STEP 0.1

#include "editorinterface.h"
#include "listbase.h"
#include "listcopyable.h"
//#include "myreal.h"

template<typename T> struct ListStorage{
    ListStorage<T>() : input(T()), output(T()){}

    // input is always the raw data either from file or pen/mouse stroke
    T input;
    // output is initially input but gets reduced to T-C-T... in automatic
    T output;
};


template<typename T> class EditorBase : public EditorInterface<T>
{
public:
    EditorBase<T>();
    //~EditorBase();

    void resetLists();
    void addPoint(QPointF p);
    //dont make getOutput const, see reversal in spiral process
    T& getOutput();
	QList<QPointF> getConvertedOutput();
    void flushOutput();

    void automatic();
	void automatic(QList<QPointF> list);

protected:

    void setOutput(T list);

    void mainIterator(const QList<dpoint>& constCliffs,QList<QList<dpoint> >& slicesRef);

private:
    //should ONLY be accessed for implementation instantiation
    ListStorage<T > data;


};

#endif // EditorBase_H
