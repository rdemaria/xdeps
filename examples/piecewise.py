# copyright ############################### #
# This file is part of the Xdeps Package.   #
# Copyright (c) CERN, 2026.                 #
# ######################################### #

import json

import xdeps as xd


values = {"x": -2.0}
manager = xd.Manager()
ref = manager.ref(values, "values")
x = ref["x"]

# Conditions are checked in order. Only the selected value is evaluated.
ref["y"] = xd.piecewise(
    (x < 0, -x),
    (x < 10, x**2),
    otherwise=100.0,
)

# ``where`` is a compact two-branch piecewise expression.
ref["sign"] = xd.where(x >= 0, 1, -1)

print(values)  # {'x': -2.0, 'y': 2.0, 'sign': -1}

ref["x"] = 3.0
print(values)  # {'x': 3.0, 'y': 9.0, 'sign': 1}

# The expression definitions contain only JSON-serializable strings.
print(json.dumps(manager.dump(), indent=2))
