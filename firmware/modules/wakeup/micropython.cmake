add_library(usermod_wakeup INTERFACE)

target_sources(usermod_wakeup INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/wakeup.c
    ${CMAKE_CURRENT_LIST_DIR}/wakeup.cpp
)

target_include_directories(usermod_wakeup INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(usermod_wakeup INTERFACE
    -DMODULE_WAKEUP_ENABLED=1
)

target_link_libraries(usermod INTERFACE usermod_wakeup)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/wakeup.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers"
)
