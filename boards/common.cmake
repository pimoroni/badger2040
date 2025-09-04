# Make sure we get our VirtualEnv Python
set(Python_FIND_VIRTUALENV "FIRST")
set(Python_FIND_UNVERSIONED_NAMES "FIRST")
set(Python_FIND_STRATEGY "LOCATION")
find_package (Python COMPONENTS Interpreter Development)

message("dir2uf2/py_decl: Using Python ${Python_EXECUTABLE}")

# Convert supplies paths to absolute, for a quieter life
get_filename_component(PIMORONI_UF2_MANIFEST ${PIMORONI_UF2_MANIFEST} REALPATH)
get_filename_component(PIMORONI_UF2_DIR ${PIMORONI_UF2_DIR} REALPATH)

if (EXISTS "${PIMORONI_TOOLS_DIR}/py_decl/py_decl.py")
    add_custom_target("${MICROPY_TARGET}-verify" ALL
        COMMAND ${Python_EXECUTABLE} "${PIMORONI_TOOLS_DIR}/py_decl/py_decl.py" --to-json --verify "${CMAKE_CURRENT_BINARY_DIR}/${MICROPY_TARGET}.uf2"
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "pydecl: Verifying ${MICROPY_TARGET}.uf2"
        DEPENDS ${MICROPY_TARGET}
    )
endif()

if (EXISTS "${PIMORONI_TOOLS_DIR}/dir2uf2/dir2uf2" AND EXISTS "${PIMORONI_UF2_MANIFEST}" AND EXISTS "${PIMORONI_UF2_DIR}")
    MESSAGE("dir2uf2: Using manifest ${PIMORONI_UF2_MANIFEST}.")
    MESSAGE("dir2uf2: Using root ${PIMORONI_UF2_DIR}.")
    add_custom_target("${MICROPY_TARGET}-with-filesystem.uf2" ALL
        COMMAND ${Python_EXECUTABLE} "${PIMORONI_TOOLS_DIR}/dir2uf2/dir2uf2" --fs-compact --sparse --append-to "${MICROPY_TARGET}.uf2" --manifest "${PIMORONI_UF2_MANIFEST}" --filename with-filesystem.uf2 "${PIMORONI_UF2_DIR}"
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "dir2uf2: Appending filesystem to ${MICROPY_TARGET}.uf2."
        DEPENDS ${MICROPY_TARGET}
        DEPENDS "${MICROPY_TARGET}-verify"
    )
endif()