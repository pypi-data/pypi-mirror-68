#############
# Variables needed in modules, auto-generated git.h file needed in wrappers
#############
set(PRE_CONFIGURE_FILE "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/git.cc.in")
set(POST_CONFIGURE_FILE "${CMAKE_CURRENT_BINARY_DIR}/git.cpp")
file(APPEND "${CMAKE_CURRENT_BINARY_DIR}/git.cpp" "")
include(${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/git_watcher.cmake)
# Danger injection from submodule?
set(GIT_HEADER_DIR "${PROJECT_SOURCE_DIR}/cmake-git-version-tracking/better-example/")