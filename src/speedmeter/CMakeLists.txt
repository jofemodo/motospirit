cmake_minimum_required(VERSION 2.6)
project(speedmeter)

include(CheckIncludeFiles)
include(CheckLibraryExists)

link_directories(/usr/local/lib)

check_library_exists(wiringPi wiringPiSetup "" HAVE_WIRINGPI_LIB)

if(${HAVE_WIRINGPI_LIB})
	add_library(speedmeter SHARED speedmeter.h speedmeter.c)
	target_link_libraries(speedmeter wiringPi)
else()
	add_library(speedmeter SHARED speedmeter.h speedmeter.c wiringPiEmu.c)
	add_library(wiringPiEmu SHARED wiringPiEmu.h wiringPiEmu.c)
	target_link_libraries(speedmeter)
	install(TARGETS wiringPiEmu LIBRARY DESTINATION lib)
endif()

add_executable(speedmeter_test speedmeter_test.c)
target_link_libraries(speedmeter_test speedmeter)

install(TARGETS speedmeter LIBRARY DESTINATION lib)
#install(TARGETS speedmeter RUNTIME DESTINATION bin)
