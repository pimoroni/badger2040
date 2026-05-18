#!/usr/bin/env bash
# Build Badger 2040 firmware inside the Docker container.
# Usage: docker compose run --rm build
#        docker compose run --rm -e BOARD=PIMORONI_BADGER2040W build
set -euo pipefail

WORKSPACE=/workspace
BADGER_DIR="${WORKSPACE}/badger2040"
MICROPYTHON_DIR="${WORKSPACE}/micropython"
FIRMWARE_DIR="${BADGER_DIR}/firmware"
BADGER_OS_DIR="${BADGER_DIR}/badger_os"
DIST_DIR="${BADGER_DIR}/dist"

# ── Patch helpers ─────────────────────────────────────────────────────────────

apply_patch() {
    local patch_file="$1"
    local target_dir="$2"
    local name
    name="$(basename "$patch_file")"
    echo ":: patch: ${name}"
    pushd "$target_dir" > /dev/null
    if git apply --check "$patch_file" 2>/dev/null; then
        git apply "$patch_file"
        echo "   applied."
    elif git apply --check --reverse "$patch_file" 2>/dev/null; then
        echo "   already applied, skipping."
    else
        echo "   WARNING: patch does not apply cleanly, attempting anyway..." >&2
        git apply --reject "$patch_file" || true
    fi
    popd > /dev/null
}

apply_patch "${FIRMWARE_DIR}/startup_overclock.patch" "${MICROPYTHON_DIR}/lib/pico-sdk"
# pins.csv fix (932f76c) is already merged in MicroPython v1.24+ — skip

# ── Board builds ──────────────────────────────────────────────────────────────

mkdir -p "${DIST_DIR}"

# Default: build both boards. Override with BOARD env var.
BOARDS="${BOARD:-PIMORONI_BADGER2040W PIMORONI_BADGER2040}"

for BUILD_BOARD in ${BOARDS}; do
    case "${BUILD_BOARD}" in
        PIMORONI_BADGER2040W) SHORTNAME="badger2040w" ;;
        PIMORONI_BADGER2040)  SHORTNAME="badger2040" ;;
        *)                     SHORTNAME="${BUILD_BOARD,,}" ;;
    esac

    BOARD_DIR="${FIRMWARE_DIR}/${BUILD_BOARD}"
    BUILD_DIR="${MICROPYTHON_DIR}/ports/rp2/build-${SHORTNAME}"
    RELEASE_FILE="${DIST_DIR}/${SHORTNAME}-micropython.uf2"
    RELEASE_FILE_WITH_OS="${DIST_DIR}/${SHORTNAME}-micropython-with-badger-os.uf2"

    echo ""
    echo "════════════════════════════════════════"
    echo " ${BUILD_BOARD}"
    echo "════════════════════════════════════════"

    ccache --zero-stats 2>/dev/null || true

    cmake \
        -S "${MICROPYTHON_DIR}/ports/rp2" \
        -B "${BUILD_DIR}" \
        -DPICO_BUILD_DOCS=0 \
        -DUSER_C_MODULES="${BOARD_DIR}/micropython.cmake" \
        -DMICROPY_BOARD_DIR="${BOARD_DIR}" \
        -DMICROPY_BOARD="${BUILD_BOARD}" \
        -DCMAKE_C_COMPILER_LAUNCHER=ccache \
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache

    cmake --build "${BUILD_DIR}" -j"$(nproc)"

    ccache --show-stats 2>/dev/null || true

    cp "${BUILD_DIR}/firmware.uf2" "${RELEASE_FILE}"

    echo "── verifying UF2 ──"
    python3 "${WORKSPACE}/py_decl/py_decl.py" --to-json --verify "${RELEASE_FILE}"

    echo "── appending Badger OS filesystem ──"
    # dir2uf2 writes output relative to cwd; cd into dist so files land there
    pushd "${DIST_DIR}" > /dev/null
    "${WORKSPACE}/dir2uf2/dir2uf2" \
        --fs-compact \
        --append-to "${RELEASE_FILE}" \
        --manifest "${BOARD_DIR}/uf2-manifest.txt" \
        --filename "with-badger-os.uf2" \
        "${BADGER_OS_DIR}/"
    popd > /dev/null

    echo ""
    echo "Output:"
    echo "  ${RELEASE_FILE}"
    echo "  ${RELEASE_FILE_WITH_OS}"
done

echo ""
echo "All done. UF2 files are in dist/"
