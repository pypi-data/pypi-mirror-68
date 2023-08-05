import datetime as dt
import logging
import os.path
import re
from unittest.mock import patch

import netCDF4
import pandas as pd
import pytest
import scipy.interpolate

from netcdf_scm.io import load_scmdataframe
from netcdf_scm.stitching import (
    get_branch_time,
    get_reference_values,
    normalise_against_picontrol,
)

# TODO: some of these are definitely not unit tests...


@pytest.fixture(scope="module")
def picontrol_data(test_cmip6_crunch_output):
    test_file = os.path.join(
        test_cmip6_crunch_output,
        "Amon",
        "CMIP6",
        "CMIP",
        "NCAR",
        "CESM2",
        "piControl",
        "r1i1p1f1",
        "Amon",
        "tas",
        "gn",
        "v20190320",
        "netcdf-scm_tas_Amon_CESM2_piControl_r1i1p1f1_gn_080001-099912.nc",
    )

    loaded = load_scmdataframe(test_file)
    loaded.metadata["netcdf-scm crunched file"] = test_file

    return loaded


@pytest.fixture(scope="module")
def historical_data(test_cmip6_crunch_output):
    test_file = os.path.join(
        test_cmip6_crunch_output,
        "Amon",
        "CMIP6",
        "CMIP",
        "NCAR",
        "CESM2",
        "historical",
        "r10i1p1f1",
        "Amon",
        "tas",
        "gn",
        "v20190313",
        "netcdf-scm_tas_Amon_CESM2_historical_r10i1p1f1_gn_185001-201412.nc",
    )

    loaded = load_scmdataframe(test_file)
    loaded.metadata["netcdf-scm crunched file"] = test_file

    return loaded


@pytest.fixture
def junk_data(picontrol_data):
    return picontrol_data.copy()


@pytest.mark.parametrize("expected_time,parent", ((306600.0, True), (674885.0, False),))
def test_get_branch_time_cmip6(historical_data, expected_time, parent):
    raw = netCDF4.num2date(expected_time, "days since 0001-01-01 00:00:00", "365_day",)
    expected = dt.datetime(raw.year, raw.month, raw.day)

    res = get_branch_time(historical_data, parent)

    assert res == expected


def test_get_branch_time_bcc_warning(caplog, test_cmip6_crunch_output):
    bcc_dat = load_scmdataframe(
        os.path.join(
            test_cmip6_crunch_output,
            "Amon",
            "CMIP6",
            "CMIP",
            "BCC",
            "BCC-CSM2-MR",
            "historical",
            "r1i1p1f1",
            "Amon",
            "tas",
            "gn",
            "v20181126",
            "netcdf-scm_tas_Amon_BCC-CSM2-MR_historical_r1i1p1f1_gn_185001-201412.nc",
        )
    )
    expected = dt.datetime(int(bcc_dat.metadata["branch_time_in_parent"]), 1, 1)

    with caplog.at_level(logging.WARNING):
        res = get_branch_time(bcc_dat)

    assert res == expected
    warn_str = (
        "Assuming BCC metadata is wrong and branch time units are actually years, "
        "not days"
    )
    bcc_warning = [r for r in caplog.record_tuples if r[2] == warn_str]
    assert len(bcc_warning) == 1
    assert bcc_warning[0][1] == logging.WARNING


def test_get_branch_time_cmip5(test_marble_cmip5_crunch_output):
    cmip5_dat = load_scmdataframe(
        os.path.join(
            test_marble_cmip5_crunch_output,
            "Amon",
            "cmip5",
            "historical",
            "Amon",
            "tas",
            "NorESM1-M",
            "r1i1p1",
            "netcdf-scm_tas_Amon_NorESM1-M_historical_r1i1p1_185001-200512.nc",
        )
    )

    parent_path = os.path.join(
        test_marble_cmip5_crunch_output,
        "Amon",
        "cmip5",
        "piControl",
        "Amon",
        "tas",
        "NorESM1-M",
        "r1i1p1",
        "netcdf-scm_tas_Amon_NorESM1-M_piControl_r1i1p1_070001-120012.nc",
    )

    raw = netCDF4.num2date(255135.0, "days since 1-01-01 00:00:00", "365_day",)
    expected = dt.datetime(raw.year, raw.month, raw.day)

    res = get_branch_time(cmip5_dat, parent_path=parent_path)

    assert res == expected


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


def test_get_reference_values_unrecognised_method(historical_data, picontrol_data):
    picontrol_branch_time = get_branch_time(historical_data)

    error_msg = re.escape("Unrecognised normalisation method: humpty dumpty")

    with pytest.raises(NotImplementedError, match=error_msg):
        get_reference_values(
            historical_data, picontrol_data, picontrol_branch_time, "humpty dumpty"
        )


def test_get_reference_values_no_branch_time_data(historical_data, picontrol_data):
    picontrol_branch_time = get_branch_time(historical_data)
    pi_data_to_use = picontrol_data.filter(year=picontrol_branch_time.year, keep=False)

    error_msg = re.compile(
        ".*Branching time `084101` not available in piControl data in "
        "{}".format(pi_data_to_use.metadata["netcdf-scm crunched file"])
    )

    with pytest.raises(ValueError, match=error_msg):
        get_reference_values(
            historical_data, pi_data_to_use, picontrol_branch_time, "not reached"
        )


@pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
@pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
def test_get_reference_values_mean_31_yr_after_branch_time(
    historical_data, picontrol_data, member_id, activity_id
):
    picontrol_branch_time = get_branch_time(historical_data)

    ref_mean = (
        picontrol_data.filter(
            year=range(picontrol_branch_time.year, picontrol_branch_time.year + 31)
        )
        .timeseries()
        .mean(axis=1)
    )
    expected = pd.concat([ref_mean] * historical_data["time"].shape[0], axis=1)
    expected.columns = historical_data["time"]

    expected = expected.reset_index()
    idx = historical_data.meta.columns.tolist()
    for c in idx:
        if c in ["region", "variable", "unit"]:
            continue

        expected[c] = historical_data.get_unique_meta(c, no_duplicates=True)

    expected = expected.set_index(idx)

    picontrol_data_to_use = picontrol_data.copy()
    picontrol_data_to_use.set_meta(member_id, "member_id")
    picontrol_data_to_use.set_meta(activity_id, "activity_id")

    res = get_reference_values(
        historical_data,
        picontrol_data_to_use,
        picontrol_branch_time,
        "31-yr-mean-after-branch-time",
    )

    pd.testing.assert_frame_equal(res, expected, check_like=True)


def test_get_reference_values_mean_31_yr_after_branch_time_not_enough_data_error(
    historical_data, picontrol_data
):
    picontrol_branch_time = get_branch_time(historical_data)
    pi_data_to_use = picontrol_data.filter(
        year=range(picontrol_branch_time.year, picontrol_branch_time.year + 10)
    )

    error_msg = re.compile(
        ".*Only `084101` to `085012` is available after the branching time `084101` in piControl "
        "data in "
        "{}".format(pi_data_to_use.metadata["netcdf-scm crunched file"])
    )

    with pytest.raises(ValueError, match=error_msg):
        get_reference_values(
            historical_data,
            pi_data_to_use,
            picontrol_branch_time,
            "31-yr-mean-after-branch-time",
        )


@pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
@pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
def test_get_reference_values_mean_21_year_running_mean(
    historical_data, picontrol_data, member_id, activity_id
):
    # shorten the data so our picontrol data is long enough to be useable
    historical_data_to_use = historical_data.filter(year=range(1850, 1950)).copy()

    picontrol_branch_time = get_branch_time(historical_data_to_use)
    first_relevant_year = (
        picontrol_branch_time.year
        - 11  # 21-year running mean so go 11 years either side to ensure we have enough data
    )
    last_relevant_year = (
        picontrol_branch_time.year
        + historical_data_to_use["year"].max()
        - historical_data_to_use["year"].min()
        + 11  # 21-year running mean so go 11 years either side to ensure we have enough data
    )

    ref_ts = picontrol_data.filter(
        year=range(first_relevant_year, last_relevant_year + 1)
    ).timeseries()
    ref_values = ref_ts.rolling(window=21 * 12, center=True, axis="columns").mean()
    relevant_cols = ref_values.columns[
        ref_values.columns.map(
            lambda x: (x.year >= picontrol_branch_time.year)
            and (x.year <= last_relevant_year - 11)
        )
    ]
    expected = ref_values[relevant_cols]

    expected = expected.reset_index()
    idx = historical_data_to_use.meta.columns.tolist()
    for c in idx:
        if c in ["region", "variable", "unit"]:
            continue

        expected[c] = historical_data_to_use.get_unique_meta(c, no_duplicates=True)

    expected = expected.set_index(idx)
    expected.columns = historical_data_to_use["time"]

    picontrol_data_to_use = picontrol_data.copy()
    picontrol_data_to_use.set_meta(member_id, "member_id")
    picontrol_data_to_use.set_meta(activity_id, "activity_id")

    res = get_reference_values(
        historical_data_to_use,
        picontrol_data_to_use,
        picontrol_branch_time,
        "21-yr-running-mean",
    )

    pd.testing.assert_frame_equal(res, expected, check_like=True)


@pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
@pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
def test_get_reference_values_mean_21_year_running_mean_with_extension(
    historical_data, picontrol_data, member_id, activity_id, caplog
):
    # shorten the data so our picontrol data is long enough to be useable
    historical_data_to_use = historical_data.filter(year=range(1850, 2000)).copy()

    picontrol_branch_time = get_branch_time(historical_data_to_use)
    first_relevant_year = (
        picontrol_branch_time.year
        - 5  # don't give quite enough data so some has to be filled
    )
    last_relevant_year = (
        picontrol_branch_time.year
        + historical_data_to_use["year"].max()
        - historical_data_to_use["year"].min()
        + 11  # 21-year running mean so go 11 years either side to ensure we have enough data
    )

    picontrol_data_to_use = picontrol_data.filter(
        year=range(first_relevant_year, last_relevant_year + 1)
    ).copy()

    ref_ts = picontrol_data_to_use.timeseries()
    ref_values = ref_ts.rolling(window=21 * 12, center=True, axis="columns").mean()

    expected = ref_values.reset_index()
    idx = historical_data_to_use.meta.columns.tolist()
    for c in idx:
        if c in ["region", "variable", "unit"]:
            continue

        expected[c] = historical_data_to_use.get_unique_meta(c, no_duplicates=True)

    expected = expected.set_index(idx)

    relevant_cols = expected.columns[
        expected.columns.map(
            lambda x: (x.year >= picontrol_branch_time.year)
            and (x.year <= last_relevant_year - 11)
        )
    ]
    expected = expected[relevant_cols]

    interp_base = expected.dropna(axis=1)

    def _convert_to_s(x):
        return (x - dt.datetime(1970, 1, 1)).total_seconds()

    time_axis_base = interp_base.columns.map(_convert_to_s)
    interpolater = scipy.interpolate.interp1d(
        time_axis_base, interp_base.values, fill_value="extrapolate"
    )

    nan_cols = sorted(list(set(expected.columns) - set(interp_base.columns)))
    time_nan_cols = [_convert_to_s(x) for x in nan_cols]

    expected.loc[:, expected.isnull().any()] = interpolater(time_nan_cols)
    expected.columns = historical_data_to_use["time"]

    picontrol_data_to_use.set_meta(member_id, "member_id")
    picontrol_data_to_use.set_meta(activity_id, "activity_id")

    with caplog.at_level(logging.INFO):
        res = get_reference_values(
            historical_data_to_use,
            picontrol_data_to_use,
            picontrol_branch_time,
            "21-yr-running-mean",
        )

    pd.testing.assert_frame_equal(res, expected, check_like=True)
    info_str = (
        "Filling gaps in running mean (where not enough values were available to create a full "
        "window) with linear interpolations and extrapolations."
    )
    fill_info = [r for r in caplog.record_tuples if r[2] == info_str]
    assert len(fill_info) == 1
    assert fill_info[0][1] == logging.INFO


@pytest.mark.parametrize(
    "start_cut,end_cut,expected_error",
    (
        (10 ** 3, -30, True),
        (10 ** 3, -20, True),
        (10 ** 3, -10, True),
        (10 ** 3, -5, True),
        (10 ** 3, -1, True),
        (10 ** 3, 0, False),
        (0, 10 ** 3, False),
        (10 ** 3, 5, False),
        (5, 10 ** 3, False),
    ),
)
def test_get_reference_values_21_year_running_mean_not_enough_data_error(
    historical_data, picontrol_data, start_cut, end_cut, expected_error, caplog
):
    # shorten the data so our picontrol data is long enough to be useable
    historical_data_to_use = historical_data.filter(year=range(1850, 1950)).copy()

    picontrol_branch_time = get_branch_time(historical_data_to_use)
    pi_data_to_use = picontrol_data.filter(
        year=range(
            picontrol_branch_time.year - start_cut,
            picontrol_branch_time.year
            + historical_data_to_use["year"].max()
            - historical_data_to_use["year"].min()
            + end_cut
            + 1,
        )
    )

    error_msg = re.escape(
        "Only `{:04d}01` to `{:04d}12` is available in the piControl data. "
        "Given the branching time, `084101`, we need data from ~`0830` to `0951`. "
        "piControl data in "
        "{}".format(
            pi_data_to_use["year"].min(),
            pi_data_to_use["year"].max(),
            pi_data_to_use.metadata["netcdf-scm crunched file"],
        )
    )

    def call():
        get_reference_values(
            historical_data_to_use,
            pi_data_to_use,
            picontrol_branch_time,
            "21-yr-running-mean",
        )

    if expected_error:
        with pytest.raises(ValueError, match=error_msg):
            call()

    else:
        with caplog.at_level(logging.INFO):
            call()

        info_str = (
            "Filling gaps in running mean (where not enough values were available to create a full "
            "window) with linear interpolations and extrapolations."
        )
        info_msg = [r for r in caplog.record_tuples if r[2] == info_str]
        assert len(info_msg) == 1
        assert info_msg[0][1] == logging.INFO


@patch("netcdf_scm.stitching.get_reference_values")
def test_normalise_against_picontrol(
    mock_get_reference_values, historical_data, picontrol_data
):
    mock_ref_values = historical_data.timeseries()
    mock_ref_values.iloc[:, :] = 1
    mock_get_reference_values.return_value = mock_ref_values
    picontrol_branch_time = dt.datetime(2, 2, 2)  # mocked so irrelevant
    method = "humpty dumpty"

    res = normalise_against_picontrol(
        historical_data, picontrol_data, picontrol_branch_time, method
    )

    mock_get_reference_values.assert_called_with(
        historical_data, picontrol_data, picontrol_branch_time, method,
    )

    expected_metadata = {
        **{"(child) {}".format(k): v for k, v in historical_data.metadata.items()},
        **{
            "(normalisation) {}".format(k): v
            for k, v in picontrol_data.metadata.items()
        },
    }
    expected_metadata["normalisation method"] = method

    assert res.metadata == expected_metadata

    # thanks to mocking, everything simply shifted down by 1
    pd.testing.assert_frame_equal(res.timeseries(), historical_data.timeseries() - 1)


@pytest.mark.parametrize(
    "picontrol_expt_name,error", (("esm-piControl", False), ("piC", True),)
)
def test_normalise_against_picontrol_name_error(
    picontrol_expt_name, error, picontrol_data, historical_data
):
    picontrol_branch_time = get_branch_time(historical_data)
    tweaked_picontrol = picontrol_data.copy()
    tweaked_picontrol.metadata["experiment_id"] = picontrol_expt_name

    def call():
        normalise_against_picontrol(
            historical_data,
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
