# Setting executables output
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

# Including directories
include_directories(${INCLUDE_DIRS})

# Adding executables
# For every main in the MAIN_FILES list, add an executable
foreach(main_file ${MAIN_FILES})
    get_filename_component(main_name ${main_file} NAME_WE)

	# Main compilation message
	message(STATUS "🛠 Compiling executable:  ${main_file}")

	# Adding executable	
    add_executable(${main_name} ${main_file})

    # Linking executables
    target_link_libraries(${main_name} ${LIBRARY_NAME})

    # Linking to OpenMPI if MPI option is enabled (no debug)
    if (MPI AND NOT DEBUG)
        target_link_libraries(${main_name} MPI::MPI_C)

        if(MPI_COMPILE_FLAGS)
          set_target_properties(${main_name} PROPERTIES
            COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
        endif()

        if(MPI_LINK_FLAGS)
          set_target_properties(${main_name} PROPERTIES
            LINK_FLAGS "${MPI_LINK_FLAGS}")
        endif()
    endif()

    # Linking to OpenMPI if MPI option is enabled (debug)
    if (MPI AND DEBUG)
        target_link_libraries(${main_name} MPI::MPI_C)

        if(MPI_COMPILE_FLAGS_DEBUG)
          set_target_properties(${main_name} PROPERTIES
            COMPILE_FLAGS_DEBUG "${MPI_COMPILE_FLAGS} -g -O0 -DDEBUG")
        endif()

        if(MPI_LINK_FLAGS_DEBUG)
          set_target_properties(${main_name} PROPERTIES
            LINK_FLAGS_DEBUG "${MPI_LINK_FLAGS}")
        endif()
    endif()
endforeach(main_file)