cmake_minimum_required(VERSION 3.27)
project(neuralnet_evolution)

set(CMAKE_CXX_STANDARD 17)

set(SDL2_PATH "C:\\Users\\kely\\Downloads\\SDL2-2.30.1\\x86_64-w64-mingw32")
find_package(SDL2 REQUIRED)
include_directories( ${SDL2_INCLUDE_DIR} )

add_executable(
        neuralnet_evolution
        main.cpp
        Entity.h
        Environment.h
        Gene.h
        Organism.h
        MainWindow.h
)

target_link_libraries(untitled2 ${SDL2_LIBRARY} )