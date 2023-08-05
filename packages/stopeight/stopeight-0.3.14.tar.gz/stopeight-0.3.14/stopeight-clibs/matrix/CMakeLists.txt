cmake_minimum_required (VERSION 3.4.3)

project(stopeight-clibs-matrix)

aux_source_directory(. SRC_LIST)
set(${PROJECT_NAME}_sources
    Matrix.cpp
    ${POST_CONFIGURE_FILE}
)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_sources})
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${stopeight-clibs_INCLUDE_DIRS}
    ${GIT_HEADER_DIR}
)
add_dependencies(${PROJECT_NAME} check_git)
install(TARGETS ${PROJECT_NAME} DESTINATION lib)
