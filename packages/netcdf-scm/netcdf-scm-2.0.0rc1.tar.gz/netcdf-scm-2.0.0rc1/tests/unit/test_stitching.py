import datetime as dt
import re
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from scmdata import ScmDataFrame

from netcdf_scm.stitching import (
    get_branch_time,
    get_parent_replacements,
    get_reference_values,
    normalise_against_picontrol,
    step_up_family_tree,
)


@pytest.fixture(scope="function")
def junk_data():
    out = ScmDataFrame(
        np.arange(100),
        index=np.arange(1850, 1950),
        columns={
            "scenario": ["rcp26"],
            "experiment_id": ["rcp26"],
            "model": ["model1"],
            "climate_model": ["climate_model1"],
            "mip_era": ["CMIP6"],
            "region": ["World"],
            "variable": ["tas"],
            "unit": ["K"],
        },
    )

    out.metadata = {
        "branch_time_in_parent": 0.0,
        "parent_time_units": "days since 1850-01-01",
        "calendar": "365_day",
        "source_id": "UoM mocked data",
        "experiment_id": "rcp26",
        "netcdf-scm crunched file": "/path/to/mocked/rcp26/data_rcp26.nc",
    }

    return out


@pytest.fixture
def junk_data_picontrol(junk_data):
    out = junk_data.copy()
    out.set_meta("piControl", "scenario")
    out.set_meta("piControl", "experiment_id")
    out.metadata = {
        "other": "metadata",
        "goes": "here",
        "branch_time_in_parent": -1001.1,
        "parent_time_units": "days since 1850-01-01",
        "calendar": "365_day",
        "source_id": "UoM mocked data",
        "experiment_id": "piControl",
        "netcdf-scm crunched file": "/path/to/mocked/piControl/data_piControl.nc",
    }

    return out


def test_get_branch_time_cmip5_not_parent_error(junk_data):
    junk_data.set_meta("CMIP5", "mip_era")

    error_msg = re.escape(
        "CMIP5 data does not contain information about the branch time "
        "in the child's time axis"
    )
    with pytest.raises(ValueError, match=error_msg):
        get_branch_time(junk_data, parent=False)


def test_get_branch_time_cmip5_no_parent_path_error(junk_data):
    junk_data.set_meta("CMIP5", "mip_era")

    error_msg = re.escape("If using cmip5 data, you must provide `parent_path`")
    with pytest.raises(ValueError, match=error_msg):
        get_branch_time(junk_data)


def test_get_reference_values_unrecognised_method(junk_data):
    picontrol_branch_time = get_branch_time(junk_data)

    error_msg = re.escape("Unrecognised normalisation method: humpty dumpty")

    with pytest.raises(NotImplementedError, match=error_msg):
        get_reference_values(
            junk_data, junk_data, picontrol_branch_time, "humpty dumpty"
        )


def test_get_reference_values_no_branch_time_data(junk_data, junk_data_picontrol):
    picontrol_branch_time = get_branch_time(junk_data)
    pi_data_to_use = junk_data_picontrol.filter(
        year=picontrol_branch_time.year, keep=False
    )

    error_msg = re.compile(
        ".*Branching time `185001` not available in piControl data in "
        "{}".format(pi_data_to_use.metadata["netcdf-scm crunched file"])
    )

    with pytest.raises(ValueError, match=error_msg):
        get_reference_values(
            junk_data, pi_data_to_use, picontrol_branch_time, "not reached"
        )


@patch("netcdf_scm.stitching.get_reference_values")
def test_normalise_against_picontrol(
    mock_get_reference_values, junk_data, junk_data_picontrol
):
    mock_ref_values = junk_data.timeseries()
    mock_ref_values.iloc[:, :] = 1
    mock_get_reference_values.return_value = mock_ref_values
    picontrol_branch_time = dt.datetime(2, 2, 2)  # mocked so irrelevant
    method = "humpty dumpty"

    res = normalise_against_picontrol(
        junk_data, junk_data_picontrol, picontrol_branch_time, method
    )

    mock_get_reference_values.assert_called_with(
        junk_data, junk_data_picontrol, picontrol_branch_time, method,
    )

    expected_metadata = {
        **{"(child) {}".format(k): v for k, v in junk_data.metadata.items()},
        **{
            "(normalisation) {}".format(k): v
            for k, v in junk_data_picontrol.metadata.items()
        },
    }
    expected_metadata["normalisation method"] = method

    assert res.metadata == expected_metadata

    # thanks to mocking, everything simply shifted down by 1
    pd.testing.assert_frame_equal(res.timeseries(), junk_data.timeseries() - 1)


@pytest.mark.parametrize(
    "picontrol_expt_name,error", (("esm-piControl", False), ("piC", True),)
)
def test_normalise_against_picontrol_name_error(
    picontrol_expt_name, error, junk_data_picontrol, junk_data
):
    picontrol_branch_time = get_branch_time(junk_data)
    tweaked_picontrol = junk_data_picontrol.copy()
    tweaked_picontrol.metadata["experiment_id"] = picontrol_expt_name

    def call():
        normalise_against_picontrol(
            junk_data,
            tweaked_picontrol,
            picontrol_branch_time,
            "31-yr-mean-after-branch-time",
        )

    if error:
        error_msg = re.escape(
            "If you would like to normalise against an experiment other than piControl, please raise an "
            "issue at https://gitlab.com/znicholls/netcdf-scm/-/issues"
        )
        with pytest.raises(NotImplementedError, match=error_msg):
            call()

    else:
        # no error
        call()


@pytest.mark.parametrize(
    "start,expected",
    (
        ("(child)", "(parent)"),
        ("(parent)", "(grandparent)"),
        ("(grandparent)", "(greatgrandparent)"),
        ("(greatgrandparent)", "(greatgreatgrandparent)"),
        ("(greatgreatgreatgreatgrandparent)", "(greatgreatgreatgreatgreatgrandparent)"),
    ),
)
def test_step_up_family_tree(start, expected):
    assert step_up_family_tree(start) == expected


@pytest.mark.parametrize(
    "start,expected,cmip5",
    (
        (
            {
                "parent_activity_id": "CMIP",
                "parent_experiment_id": "historical",
                "parent_mip_era": "CMIP6",
                "parent_source_id": "UoM",
                "parent_variant_label": "r1i1p1f1",
                "other_meta": "something",
            },
            {
                "parent_activity_id": "CMIP",
                "parent_experiment_id": "historical",
                "parent_mip_era": "CMIP6",
                "parent_source_id": "UoM",
                "parent_member_id": "r1i1p1f1",
            },
            False,
        ),
        (
            {
                "parent_experiment": "piControl",
                "parent_experiment_id": "piControl",
                "parent_experiment_rip": "r1i1p1",
                "other_meta": "something",
            },
            {
                "parent_experiment": "piControl",
                "parent_experiment_id": "piControl",
                "parent_ensemble_member": "r1i1p1",
            },
            True,
        ),
    ),
)
def test_get_parent_replacements(junk_data, start, expected, cmip5):
    junk_data.metadata = start

    if cmip5:
        junk_data.set_meta("CMIP5", "mip_era")
    else:
        junk_data.set_meta("CMIP6", "mip_era")

    assert get_parent_replacements(junk_data) == expected


def test_get_parent_replacements_no_rip_error(junk_data):
    junk_data.set_meta("CMIP5", "mip_era")
    error_msg = re.escape("No `parent_experiment_rip` in metadata")
    with pytest.raises(KeyError, match=error_msg):
        get_parent_replacements(junk_data)


def test_get_parent_replacements_no_parent_variant_label_error(junk_data):
    junk_data.set_meta("CMIP6", "mip_era")
    error_msg = re.escape("No `parent_variant_label` in metadata")
    with pytest.raises(KeyError, match=error_msg):
        get_parent_replacements(junk_data)
