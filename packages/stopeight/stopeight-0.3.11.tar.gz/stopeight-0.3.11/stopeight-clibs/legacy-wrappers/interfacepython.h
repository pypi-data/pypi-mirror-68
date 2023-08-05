#ifndef INTERFACEPYTHON_H
#define INTERFACEPYTHON_H


#include <QtCore/QList>
#include <QtCore/QPointF>

#ifdef _WINDOWS
#ifdef _DEBUG
#undef _DEBUG
#define DEBUG_BYPASS 1
#endif
#endif

#include <Python.h>
#include "error.h"


namespace legacy_wrappers{
//private
static PyObject* LegacyError;
static PyObject* error(const char* message);
static PyObject* error(legacy::alg_logic_error err);
static PyObject* convert(QList<QPointF> list);
static QList<QPointF> parse_list(PyObject *self, PyObject *args);
//public
static PyObject* parse_file(PyObject* self, PyObject* args);
static PyObject* TCT_to_bezier(PyObject* self, PyObject* args);
static PyObject* stroke_parallel(PyObject* self, PyObject* args);
static PyObject* stroke_sequential(PyObject* self, PyObject* args);
}

static PyMethodDef legacyMethods[] = {
    {"parse_file",  legacy_wrappers::parse_file, METH_VARARGS,
     "parse proprietary legacy qt file format for input points of recorded pen-stroke."},
	 { "TCT_to_bezier",  legacy_wrappers::TCT_to_bezier, METH_VARARGS,
	 "Convert stopeight TCT path to quadratic bezier segments suitable for rendering in most graphics APIs" },
    {"stroke_parallel",  legacy_wrappers::stroke_parallel, METH_VARARGS,
     "This is the parallel version of the stroke analyzer. It can look ahead, detect and center multiple immediately repeating features, when the number of features is prime. It will theoretically run out of memory if the number of immediately repeating features is too high."},
    {"stroke_sequential",  legacy_wrappers::stroke_sequential, METH_VARARGS,
     "This is the sequential version of the stroke analyzer. It will subdivide pairs (cliffs) and triplets (turns) of immediately repeating features without further lookahead and center them."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

#if __GNUC__ >= 4
    #define VIS __attribute__((visibility("default")))
#else
    #define VIS
#endif

#ifdef PY_MAJOR_VERSION
#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef legacymodule = {
	PyModuleDef_HEAD_INIT,
    "legacy",   /* name of module */
	NULL, /* module documentation, may be NULL */
	-1,       /* size of per-interpreter state of the module,
			  or -1 if the module keeps state in global variables. */
    legacyMethods
};

PyMODINIT_FUNC PyInit_legacy(void) VIS;

#else // PY_MAJOR_VERSION >= 3

PyMODINIT_FUNC initlegacy(void) VIS;

#endif // PY_MAJOR_VERSION >= 3
#endif // PY_MAJOR_VERSION

#ifdef DEBUG_BYPASS
#undef DEBUG_BYPASS
#define _DEBUG 1
#endif // DEBUG_BYPASS

#endif // INTERFACEPYTHON_H
