cmake_minimum_required (VERSION 3.2)

set(CMAKE_CXX_STANDARD 17)

project(stopeight-clibs)
include(${PROJECT_SOURCE_DIR}/Includes.cmake)
include(${PROJECT_SOURCE_DIR}/Versioning.cmake)

add_subdirectory(matrix)
add_subdirectory(grapher)
add_subdirectory(analyzer)
add_subdirectory(legacy)
