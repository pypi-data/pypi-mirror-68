#include "interfacepython.h"
#include "render.h"
#include "editorspirals.h"
#include "editorcliffs.h"

#include <iostream>

PyObject* legacy_wrappers::error(const char* message) {
	PyErr_SetString(legacy_wrappers::LegacyError, message);
	return NULL;
}

PyObject* legacy_wrappers::error(legacy::alg_logic_error err) {
	std::string message = std::string();
	message += err.fi_name;
	message += "::";
	message += err.fu_name;
	message += ": ";
	message += err.what();
	return legacy_wrappers::error(message.c_str());
}

PyObject* legacy_wrappers::convert(QList<QPointF> list) {
	PyObject* parray = PyList_New(list.size());
	for (int i = 0; i < list.size(); i++) {
		QPointF qpoint = list.at(i);
		PyObject* ppoint = Py_BuildValue("ff", qpoint.x(), qpoint.y());
		PyList_SetItem(parray, i, ppoint);
	}
	return parray;
}

PyObject* legacy_wrappers::parse_file(PyObject *self, PyObject *args) {
	const char *pythonpath;
	if (!PyArg_ParseTuple(args, "s", &pythonpath)) {
		return legacy_wrappers::error("Filename is not a list");
	}
	QList<QPointF> myList = QList<QPointF>();
	try {
		myList = ListBase<dpoint>::open(pythonpath);
	}
	catch (legacy::alg_logic_error exc) {
		return legacy_wrappers::error(exc);
	}
	catch (const char* text) {
		return legacy_wrappers::error(text);
	}
	catch (...) {
		return legacy_wrappers::error("Undefined C-Style Wrapper Error");
	}
	return legacy_wrappers::convert(myList);
}

QList<QPointF> legacy_wrappers::parse_list(PyObject *self, PyObject *args) {
	PyObject* obj;
	QList<QPointF> list = QList<QPointF>();
	if (!PyArg_ParseTuple(args, "O", &obj)) {
        throw std::runtime_error("Argument is supposed to be a list of a pair of numbers");
	}
	PyObject* pyList = PySequence_Fast(obj, "Not a list");
	int length = PySequence_Size(obj);
	for (int i = 0; i < length; i++) {
		PyObject* item = PySequence_Fast_GET_ITEM(pyList, i);
		if (PySequence_Size(item) != 2) {
            throw std::runtime_error("Malformed point format");
		}
		float xValue;
		float yValue;
		if (PyArg_ParseTuple(item, "ff", &xValue, &yValue)) {
			list << QPointF(xValue, yValue);
		}
		else {
            throw std::runtime_error("Malformed number format");
		}
	}
	return list;
}

PyObject * legacy_wrappers::TCT_to_bezier(PyObject* self, PyObject * args)
{
	QList<QList<QPointF> > result = QList<QList<QPointF> >();
	try {
		QList<QPointF> list = legacy_wrappers::parse_list(self, args);		
		result = render::TCTPath(list);
	}
	catch (legacy::alg_logic_error exc) {
		return legacy_wrappers::error(exc);
	}
	catch (const char* text) {
		return legacy_wrappers::error(text);
	}
	catch (...) {
		return legacy_wrappers::error("undefined");
	}
	QList<QPointF> unpacked = QList<QPointF>();
	for (int i = 0; i < result.size(); i++) {
		if (i > 0) {
			result[i].removeFirst();
		}
		unpacked.append(result[i]);
	}
	return legacy_wrappers::convert(unpacked);
}

PyObject* legacy_wrappers::stroke_parallel(PyObject *self, PyObject *args) {
	EditorSpirals editor = EditorSpirals();

	try {
		editor.automatic(legacy_wrappers::parse_list(self, args));
	}
	catch (legacy::alg_logic_error exc) {
		return legacy_wrappers::error(exc);
	}
	catch (const char* text) {
		return legacy_wrappers::error(text);
	}
	catch (...) {
		return legacy_wrappers::error("undefined");
	}

	ListCopyable<dpoint> result = ListCopyable<dpoint>();
	result = editor.getOutput();
	return legacy_wrappers::convert(ListBase<dpoint>::convert(result));
}

PyObject* legacy_wrappers::stroke_sequential(PyObject *self, PyObject *args) {
	EditorCliffs editor = EditorCliffs();

	try {
		editor.automatic(legacy_wrappers::parse_list(self, args));
	}
	catch (legacy::alg_logic_error exc) {
		return legacy_wrappers::error(exc);
	}
	catch (const char* text) {
		return legacy_wrappers::error(text);
	}
	catch (...) {
		return legacy_wrappers::error("undefined");
	}

	ListCopyable<dpoint> result = ListCopyable<dpoint>();
	result = editor.getOutput();
	return legacy_wrappers::convert(ListBase<dpoint>::convert(result));
}

#ifdef PY_MAJOR_VERSION
#if PY_MAJOR_VERSION >= 3

PyMODINIT_FUNC PyInit_legacy(void)
{
	PyObject* my_mod = PyModule_Create(&legacymodule);
	if (my_mod == NULL)
		return NULL;

    legacy_wrappers::LegacyError = PyErr_NewException("legacy.error", NULL, NULL);
	Py_INCREF(legacy_wrappers::LegacyError);
	PyModule_AddObject(my_mod, "error", legacy_wrappers::LegacyError);
	return my_mod;
}

#else // #if PY_MAJOR_VERSION >= 3

PyMODINIT_FUNC initlegacy(void)
{
    PyObject* my_mod = Py_InitModule("legacy", legacyMethods);
	if (my_mod == NULL)
		return;

    legacy_wrappers::LegacyError = PyErr_NewException((char*)("legacy.error"), NULL, NULL);
	Py_INCREF(legacy_wrappers::LegacyError);
	PyModule_AddObject(my_mod, "error", legacy_wrappers::LegacyError);
}

#endif // #if PY_MAJOR_VERSION >= 3
#endif // PY_MAJOR_VERSION
