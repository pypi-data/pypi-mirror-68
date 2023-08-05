cmake_minimum_required(VERSION 3.2)

set(CMAKE_CXX_STANDARD 17)

project(stopeight)

add_subdirectory(pybind11)

#add_subdirectory(stopeight-clibs)

add_subdirectory(stopeight-clibs/matrix-wrappers)
add_subdirectory(stopeight-clibs/grapher-wrappers)
add_subdirectory(stopeight-clibs/analyzer-wrappers)
add_subdirectory(stopeight-clibs/legacy-wrappers)
