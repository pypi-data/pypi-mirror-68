// Copyright (C) 2009-2015 Specific Purpose Software GmbH
// GNU Lesser General Public License, version 2.1

#ifndef LEGACY_GLOBAL_H
#define LEGACY_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(__linux__) || defined(UNIX) || defined(__unix__) || defined(LINUX)
	//  GCC
	#if defined(LEGACY_LIBRARY)
	#  define LEGACYSHARED_EXPORT Q_DECL_EXPORT
	#else
	#  define LEGACYSHARED_EXPORT Q_DECL_IMPORT
	#endif
//#elif defined(_WIN32) || defined(_WIN64) || defined(WIN32) || defined(WIN64)
    //  Microsoft
// disabled for static
//    #if defined(LEGACY_LIBRARY)
//	#define LEGACYSHARED_EXPORT __declspec(dllexport)
//	#else
//	#define LEGACYSHARED_EXPORT __declspec(dllimport)
//	#endif
#else
	//  do nothing and hope for the best?
	#define LEGACYSHARED_EXPORT
    #pragma WARNING Unknown dynamic link semantics.
#endif

#endif // LEGACY_GLOBAL_H
