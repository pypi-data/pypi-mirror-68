cmake_minimum_required (VERSION 3.4.3)

project(stopeight-clibs-grapher)

aux_source_directory(. SRC_LIST)
#file(GLOB SOURCES "*.cpp")
set(${PROJECT_NAME}_sources
    containers.cpp
    algo.cpp
    grapher.cpp
    mean.cpp
    main.cpp
    ${POST_CONFIGURE_FILE}
)

#add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_sources})
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_sources})

#include_directories(${stopeight-clibs_INCLUDE_DIRS})
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${stopeight-clibs_INCLUDE_DIRS}
    ${GIT_HEADER_DIR}
)
add_dependencies(${PROJECT_NAME} check_git)
install(TARGETS ${PROJECT_NAME} DESTINATION lib)
