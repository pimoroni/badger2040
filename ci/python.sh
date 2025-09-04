# Include:
# F = Pyflakes
# Q = Quotes
# E/W = pycodestyle (Whitespace, Line lengths etc)
# B - flake8-bugbear = Unused loop variables, sloppy code
# COM - flake8-commas
# BLE - flake8-blind-except
# C4  - flake8-comprehensions
# ISC - flake8-implicit-str-concat = Implicit string concat, eg: `"hello" "world"` on one line
# ICN - flake8-import-conventions = Import conventions
# PIE - flake8-pie = Misc silliness, catches range with a 0 start argument
# RET - flake8-return = Enforces straight-forward code around return statements
# SLF - flake8-self
# ARG - flake8-unused-arguments

# Ignore:
# E501 - "line too long". How narrow is your screen!?
# E402 - "module level import not at top of file". Needs must!
# COM812 - "Add trailing comma". These are a little obnoxious and weird.
# ICN001 - "numpy should be imported as np". No. No it should not.

QA_INCLUDE="F,Q,W,E,B,COM,BLE,C4,ISC,ICN,PIE,RSE,RET,SLF,ARG"
QA_IGNORE="E501,E402,COM812,ICN001"

function qa_prepare_all {
    pip install ruff
}

function qa_check {
    ruff check --select "$QA_INCLUDE" --ignore "$QA_IGNORE" "$1"
}

function qa_fix {
    ruff check --select "$QA_INCLUDE" --ignore "$QA_IGNORE" --fix "$1"
}

function qa_examples_check {
    qa_check badger_os/
}

function qa_examples_fix {
    qa_fix badger_os/
}

function qa_modules_check {
    qa_check modules/badger2040
    qa_check modules/badger2040w
}

function qa_modules_fix {
    qa_fix modules/badger2040
    qa_fix modules/badger2040w
}