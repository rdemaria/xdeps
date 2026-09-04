# copyright ############################### #
# This file is part of the Xdeps Package.   #
# Copyright (c) CERN, 2026.                 #
# ######################################### #

import json

import pytest

import xdeps as xd


def test_piecewise_and_where_are_reactive():
    values = {"x": -2.0}
    manager = xd.Manager()
    ref = manager.ref(values, "r")
    x = ref["x"]

    ref["y"] = xd.piecewise(
        (x < 0, -x),
        (x < 10, x**2),
        otherwise=100.0,
    )
    ref["sign"] = xd.where(x >= 0, 1, -1)

    assert values["y"] == 2.0
    assert values["sign"] == -1
    assert ref["y"].xdeps.expr_dependencies == {x}

    ref["x"] = 3.0
    assert values["y"] == 9.0
    assert values["sign"] == 1

    ref["x"] = 12.0
    assert values["y"] == 100.0
    assert values["sign"] == 1


def test_piecewise_dump_load_is_json_serializable():
    values = {"x": -2.0}
    manager = xd.Manager()
    ref = manager.ref(values, "r")
    x = ref["x"]

    ref["y"] = xd.piecewise(
        (x < 0, -x),
        (x < 10, x**2),
        otherwise=100.0,
    )
    ref["sign"] = xd.where(x >= 0, 1, -1)

    dumped = json.loads(json.dumps(manager.dump()))
    assert all("piecewise(" in expression for _, expression in dumped)

    loaded_values = {"x": 5.0}
    loaded_manager = xd.Manager()
    loaded_ref = loaded_manager.ref(loaded_values, "r")
    loaded_manager.load(dumped)
    loaded_manager.run_tasks()

    assert loaded_values["y"] == 25.0
    assert loaded_values["sign"] == 1

    loaded_ref["x"] = -3.0
    assert loaded_values["y"] == 3.0
    assert loaded_values["sign"] == -1


def test_where_only_evaluates_the_selected_value():
    values = {"x": 2.0}
    manager = xd.Manager()
    ref = manager.ref(values, "r")

    ref["y"] = xd.where(ref["x"] > 0, ref["x"], ref["missing"])

    assert values["y"] == 2.0


def test_piecewise_validates_cases():
    with pytest.raises(ValueError, match="at least one case"):
        xd.piecewise(otherwise=0)

    with pytest.raises(TypeError, match=r"\(condition, value\) pairs"):
        xd.piecewise((True, 1, 2), otherwise=0)
