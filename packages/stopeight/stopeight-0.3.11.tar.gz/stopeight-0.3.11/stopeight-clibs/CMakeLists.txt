cmake_minimum_required (VERSION 3.2)

set(CMAKE_CXX_STANDARD 17)

project(stopeight-clibs)
add_library(${PROJECT_NAME} INTERFACE)
target_include_directories(${PROJECT_NAME} INTERFACE ${PROJECT_SOURCE_DIR}/include/)
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/ DESTINATION include)

#############
# Variables needed in wrappers and modules
#############
set(${PROJECT_NAME}_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/include
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)

#############
# Variables needed in modules, auto-generated git.h file needed in wrappers
#############
set(PRE_CONFIGURE_FILE "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/git.cc.in")
set(POST_CONFIGURE_FILE "${CMAKE_CURRENT_BINARY_DIR}/git.cpp")
file(APPEND "${CMAKE_CURRENT_BINARY_DIR}/git.cpp" "")
include(${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/git_watcher.cmake)
# Danger injection from submodule?
set(GIT_HEADER_DIR "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/")

add_subdirectory(matrix)
add_subdirectory(grapher)
add_subdirectory(analyzer)
add_subdirectory(legacy)
