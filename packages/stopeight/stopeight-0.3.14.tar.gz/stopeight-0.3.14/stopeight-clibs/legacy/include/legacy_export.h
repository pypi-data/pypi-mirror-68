#ifndef LEGACY_EXPORT_H
#define LEGACY_EXPORT_H

#include "listbase.h"
#include "editorspirals.h"
#include "editorcliffs.h"

namespace legacy{

static LEGACYSHARED_EXPORT QList<QPointF> loadSPFile(const QString& fileName){
    return ListBase<QPointF>::loadSPFile(fileName);
}

LEGACYSHARED_EXPORT class AlgorithmSpirals : public EditorSpirals {

};

LEGACYSHARED_EXPORT class AlgorithmCliffs : public EditorCliffs {

};

}
#endif // LEGACY_EXPORT_H
