add_library(usermod_system_speed INTERFACE)

target_sources(usermod_system_speed INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/system_speed.c
    ${CMAKE_CURRENT_LIST_DIR}/system_speed.cpp
)

target_include_directories(usermod_system_speed INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(usermod_system_speed INTERFACE
    -DMODULE_SYSTEM_SPEED_ENABLED=1
)

target_link_libraries(usermod INTERFACE usermod_system_speed
    hardware_vreg
    hardware_pll
    hardware_resets
)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/system_speed.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers"
)
