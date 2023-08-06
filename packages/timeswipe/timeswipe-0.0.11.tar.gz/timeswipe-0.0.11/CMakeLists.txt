cmake_minimum_required(VERSION 3.9)

SET(CMAKE_C_FLAGS "-lpthread -O3")
SET(CMAKE_CXX_FLAGS "-fpermissive -lpthread -O3 -std=gnu++17")

project(timeswipe_py DESCRIPTION "timeswipe driver python binding")

SET(SRC src/timeswipe_py.cpp)

add_library(timeswipe_py SHARED ${SRC})
set_target_properties(timeswipe_py PROPERTIES PREFIX "")
set_target_properties(timeswipe_py PROPERTIES OUTPUT_NAME "timeswipe")
set_target_properties(timeswipe_py PROPERTIES SOVERSION 1)

# rasbian has python3 while arch has python
find_package(Boost COMPONENTS python3)
If (Boost_FOUND)
else ()
find_package(Boost COMPONENTS python)
endif ()

find_package(PkgConfig REQUIRED)
pkg_search_module(PYTHON3 python3)

if (NOT "$ENV{OVERRIDE_INCLUDES}" STREQUAL "")
set(INCLUDE_LIST "$ENV{OVERRIDE_INCLUDES}")
string(REPLACE " " ";" INCLUDE_LIST ${INCLUDE_LIST})
else ()
set(INCLUDE_LIST ${PYTHON3_INCLUDE_DIRS})
endif()

if (NOT "$ENV{OVERRIDE_LIBS}" STREQUAL "")
set(LIB_LIST "$ENV{OVERRIDE_LIBS}")
string(REPLACE " " ";" LIB_LIST ${LIB_LIST})
else ()
set(LIB_LIST timeswipe ${Boost_LIBRARIES})
endif()

target_include_directories(timeswipe_py PRIVATE src ${INCLUDE_LIST})

target_link_libraries(timeswipe_py ${LIB_LIST} )

