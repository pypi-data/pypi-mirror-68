import glob
import logging
import os.path
import re

import numpy as np
import pandas as pd
import pytest
from click.testing import CliRunner
from pymagicc.io import MAGICCData
from scmdata import ScmDataFrame

from netcdf_scm.cli import stitch_netcdf_scm_ncs
from netcdf_scm.io import load_scmdataframe
from netcdf_scm.stitching import get_branch_time, get_reference_values


def _do_generic_stitched_data_tests(stiched_scmdf, cmip5=False):
    assert stiched_scmdf["scenario"].nunique() == 1
    if cmip5:
        assert "(child) branch_time" in stiched_scmdf.metadata
        assert "(parent) tracking_id" in stiched_scmdf.metadata

    else:
        assert "(child) branch_time_in_parent" in stiched_scmdf.metadata
        assert "(parent) source_id" in stiched_scmdf.metadata

    assert "(child) parent_experiment_id" in stiched_scmdf.metadata
    assert "(parent) experiment_id" in stiched_scmdf.metadata


def _do_generic_normalised_data_tests(normalised_scmdf, cmip5=False):
    assert normalised_scmdf["scenario"].nunique() == 1
    if cmip5:
        assert "(child) branch_time" in normalised_scmdf.metadata
        assert "(normalisation) tracking_id" in normalised_scmdf.metadata

    else:
        assert "(child) branch_time_in_parent" in normalised_scmdf.metadata
        assert "(normalisation) source_id" in normalised_scmdf.metadata

    assert "(child) parent_experiment_id" in normalised_scmdf.metadata
    assert "normalisation method" in normalised_scmdf.metadata
    assert "(normalisation) experiment_id" in normalised_scmdf.metadata


def _get_ref_values(
    res, normalisation, parent, normalisation_path, normalisation_method
):
    helper = res.timeseries()
    helper = pd.concat([helper.iloc[:, 0]] * res["time"].shape[0], axis=1)
    helper.columns = res["time"]

    norm_helper = normalisation.timeseries()

    useful_idx = set(norm_helper.index.names).intersection(set(helper.index.names))
    helper.index = helper.index.droplevel(
        list(set(helper.index.names) - set(useful_idx))
    )
    norm_helper.index = norm_helper.index.droplevel(
        list(set(norm_helper.index.names) - set(useful_idx))
    )

    helper = ScmDataFrame(helper)
    norm_helper = ScmDataFrame(norm_helper)
    norm_helper.metadata = normalisation.metadata

    ref_values = get_reference_values(
        helper,
        norm_helper,
        get_branch_time(parent, parent_path=normalisation_path),
        normalisation_method,
    )

    return ref_values


def _check_expected_values(
    res, other, years, regions=None, ref_values=None, operation=None
):
    if regions is None:
        regions = res.get_unique_meta("region")

    for region in regions:
        res_vals = res.filter(region=region, year=years).values
        assert not any([s == 0 for s in res_vals.shape])

        other_ts = other.filter(region=region, year=years).timeseries()
        other_vals = other_ts.values
        assert not any([s == 0 for s in other_vals.shape])

        if ref_values is not None:
            rvs = ref_values.loc[ref_values.index.get_level_values("region") == region]
            # precision of times in a `.MAG` file is only year-month so update before
            # retrieving values of interest
            rvs.columns = rvs.columns.map(
                lambda x: "{:04d}{:02d}".format(x.year, x.month)
            )
            other_ts_year_month_cols = other_ts.columns.map(
                lambda x: "{:04d}{:02d}".format(x.year, x.month)
            )

            other_vals = other_vals - rvs[other_ts_year_month_cols].values

        if operation is not None:
            if operation == "time_mean_ac":
                other_ts.iloc[:, :] = other_vals
                other_vals = ScmDataFrame(other_ts).time_mean("AC").timeseries().values

            else:
                raise NotImplementedError("operation: {}".format(operation))

        np.testing.assert_allclose(
            res_vals, other_vals, rtol=1e-5, atol=1e-6,
        )


def _do_filepath_time_consistency_check(res, filepath, annual=False):
    if annual:
        expected_end = "{:04d}-{:04d}.MAG".format(
            res["time"].min().year, res["time"].max().year,
        )
    else:
        expected_end = "{:04d}{:02d}-{:04d}{:02d}.MAG".format(
            res["time"].min().year,
            res["time"].min().month,
            res["time"].max().year,
            res["time"].max().month,
        )
    assert filepath.endswith(expected_end)


def test_stitching_default(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_default"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*EC-Earth3-Veg.*ssp585.*r1i1p1f1.*hfds.*",
            ],
        )

    assert result.exit_code == 0, result.stderr

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])
    _do_generic_stitched_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "ssp585" in child_path
    assert "r1i1p1f1" in child_path
    assert "EC-Earth3-Veg" in child_path
    assert "hfds" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    _check_expected_values(res, child, range(2015, 2017))

    parent_path = res.metadata["(parent) netcdf-scm crunched file"]
    assert "historical" in parent_path
    assert "r1i1p1f1" in parent_path
    assert "EC-Earth3-Veg" in parent_path
    assert "hfds" in parent_path

    parent = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", parent_path))[0]
    )

    _check_expected_values(res, parent, range(2013, 2015))


def test_stitching_two_levels(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_two_levels"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                "^(?!.*(NCAR)).*GeoMIP.*G6solar.*$",
            ],
        )

    assert result.exit_code == 0, result.stderr

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_stitched_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "G6solar" in child_path
    assert "r1i1p1f2" in child_path
    assert "UKESM1-0-LL" in child_path
    assert "v20191031" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    _check_expected_values(
        res,
        child,
        range(2020, 2100),
        regions=["World", "World|Northern Hemisphere", "World|Land"],
    )

    parent_path = res.metadata["(parent) netcdf-scm crunched file"]
    assert "ssp585" in parent_path
    assert "r1i1p1f2" in parent_path
    assert "UKESM1-0-LL" in parent_path
    assert "v20190726" in parent_path

    parent = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", parent_path))[0]
    )

    _check_expected_values(
        res,
        parent,
        range(2015, 2020),
        regions=["World", "World|Northern Hemisphere", "World|Land"],
    )

    grandparent_path = res.metadata["(grandparent) netcdf-scm crunched file"]
    assert "historical" in grandparent_path
    assert "r1i1p1f2" in grandparent_path
    assert "UKESM1-0-LL" in grandparent_path
    assert "v20190627" in grandparent_path

    grandparent = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", grandparent_path))[0]
    )

    _check_expected_values(
        res,
        grandparent,
        range(1880, 2014),
        regions=["World", "World|Northern Hemisphere", "World|Land"],
    )


def test_stitching_in_file_BCC_CSM2_MR(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_in_file_BCC_CSM2_MR"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*BCC-CSM2-MR.*ssp126.*r1i1p1f1.*tas.*",
                "--out-format",
                "mag-files-average-year-mid-year",
            ],
        )

    assert result.exit_code == 0, result.stderr

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_stitched_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0], annual=True)

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "ssp126" in child_path
    assert "r1i1p1f1" in child_path
    assert "BCC-CSM2-MR" in child_path
    assert "tas" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    _check_expected_values(res, child, range(2015, 2017), operation="time_mean_ac")

    parent_path = res.metadata["(parent) netcdf-scm crunched file"]
    assert "historical" in parent_path
    assert "r1i1p1f1" in parent_path
    assert "BCC-CSM2-MR" in parent_path
    assert "tas" in parent_path

    parent = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", parent_path))[0]
    )

    _check_expected_values(res, parent, range(2013, 2015), operation="time_mean_ac")

    warn_str = (
        "Assuming BCC metadata is wrong and branch time units are actually years, "
        "not days"
    )
    bcc_warning = [r for r in caplog.record_tuples if r[2] == warn_str]
    assert len(bcc_warning) == 1
    assert bcc_warning[0][1] == logging.WARNING


def test_stitching_no_parent(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_no_parent"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CNRM-ESM2-1.*r2i1p1f2.*/cSoil/.*",
            ],
        )

    assert result.exit_code != 0

    error_msg = re.compile(
        ".*No parent data \\(ssp585\\) available for "
        ".*CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-ESM2-1/ssp534-over/r2i1p1f2/Emon/cSoil/gr/v20190410/netcdf-scm_cSoil_Emon_CNRM-ESM2-1_ssp534-over_r2i1p1f2_gr_201501-210012.nc"
        ", we looked in "
        ".*CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-ESM2-1/ssp585/r2i1p1f2/Emon/cSoil/gr/\\*/netcdf-scm_cSoil_Emon_CNRM-ESM2-1_ssp585_r2i1p1f2_gr_\\*.nc"
    )
    no_parent_error = [r for r in caplog.record_tuples if error_msg.match(r[2])]
    assert len(no_parent_error) == 1
    assert no_parent_error[0][1] == logging.ERROR


def test_stitching_historical_only(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_historical_only"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*GFDL-CM4.*1pctCO2.*r1i1p1f1.*",
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    # should just be same as wrangle if like this
    assert not any(["(child)" in k for k in res.metadata])
    error_msg = re.compile(
        ".*No normalisation is being done and the parent of 1pctCO2 is piControl for "
        "infile: "
        ".*CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/1pctCO2/r1i1p1f1/Amon/tas/gr1/v20180701/netcdf-scm_tas_Amon_GFDL-CM4_1pctCO2_r1i1p1f1_gr1_000101-015012.nc"
    )
    no_operation_info = [r for r in caplog.record_tuples if error_msg.match(r[2])]
    assert len(no_operation_info) == 1
    assert no_operation_info[0][1] == logging.INFO


def test_stitching_esm_hist_only(tmpdir, caplog, test_cmip6_crunch_output):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_esm_hist_only"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CanESM5.*esm-hist.*r1i1p1f1.*fgco2.*",
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    # should just be same as wrangle if like this
    assert not any(["(child)" in k for k in res.metadata])
    error_msg = re.compile(
        "No normalisation is being done and the parent of esm-hist is esm-piControl "
        "for infile: "
        ".*CMIP6/CMIP/CCCma/CanESM5/esm-hist/r1i1p1f1/Omon/fgco2/gn/v20190429/netcdf-scm_fgco2_Omon_CanESM5_esm-hist_r1i1p1f1_gn_185001-201412.nc"
    )
    no_operation_info = [r for r in caplog.record_tuples if error_msg.match(r[2])]
    assert len(no_operation_info) == 1
    assert no_operation_info[0][1] == logging.INFO


def test_stitching_with_normalisation(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    if normalisation_method == "21-yr-running-mean":
        pytest.xfail("Not enough data to take running mean")

    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CESM2.*r10i1p1f1.*tas.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_normalised_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "historical" in child_path
    assert "r10i1p1f1" in child_path
    assert "CESM2" in child_path
    assert "tas" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "piControl" in normalisation_path
    assert "r1i1p1f1" in normalisation_path
    assert "CESM2" in normalisation_path
    assert "tas" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_cmip6_crunch_output, "*", normalisation_path)
    )[0]
    normalisation = load_scmdataframe(normalisation_path)

    assert child.metadata["branch_time_in_parent"] == 306600.0
    assert child.metadata["parent_time_units"] == "days since 0001-01-01 00:00:00"

    ref_values = _get_ref_values(
        res, normalisation, child, normalisation_path, normalisation_method
    )

    _check_expected_values(res, child, range(1850, 2015), ref_values=ref_values)


def test_stitching_with_normalisation_esm_hist(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    if normalisation_method == "21-yr-running-mean":
        pytest.xfail("Not enough data to take running mean")

    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_esm_hist"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CanESM5.*esm-hist.*r1i1p1f1.*fgco2.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_normalised_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "esm-hist" in child_path
    assert "r1i1p1f1" in child_path
    assert "CanESM5" in child_path
    assert "fgco2" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "esm-piControl" in normalisation_path
    assert "r1i1p1f1" in normalisation_path
    assert "CanESM5" in normalisation_path
    assert "fgco2" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_cmip6_crunch_output, "*", normalisation_path)
    )[0]
    normalisation = load_scmdataframe(normalisation_path)

    assert child.metadata["branch_time_in_parent"] == 1277865.0
    assert child.metadata["parent_time_units"] == "days since 1850-01-01 0:0:0.0"

    ref_values = _get_ref_values(
        res, normalisation, child, normalisation_path, normalisation_method
    )

    _check_expected_values(res, child, range(1850, 2015), ref_values=ref_values)


def test_stitching_with_normalisation_year_zero(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    if normalisation_method == "21-yr-running-mean":
        pytest.xfail("Not enough data to take running mean")

    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_year_zero"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CESM2.*abrupt-4xCO2.*r1i1p1f1.*fgco2.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_normalised_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "abrupt-4xCO2" in child_path
    assert "r1i1p1f1" in child_path
    assert "CESM2" in child_path
    assert "fgco2" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "piControl" in normalisation_path
    assert "r1i1p1f1" in normalisation_path
    assert "CESM2" in normalisation_path
    assert "fgco2" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_cmip6_crunch_output, "*", normalisation_path)
    )[0]
    normalisation = load_scmdataframe(normalisation_path)

    assert child.metadata["branch_time_in_parent"] == 182865.0
    assert child.metadata["parent_time_units"] == "days since 0001-01-01 00:00:00"

    ref_values = _get_ref_values(
        res, normalisation, child, normalisation_path, normalisation_method
    )

    _check_expected_values(res, child, range(1, 1000), ref_values=ref_values)


def test_stitching_with_normalisation_two_levels(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    if normalisation_method == "21-yr-running-mean":
        pytest.xfail("Not enough data to take running mean")

    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_two_levels"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*BCC-CSM2-MR.*ssp126.*tas.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    warn_str = (
        "Assuming BCC metadata is wrong and branch time units are actually years, "
        "not days"
    )
    bcc_warning = [r for r in caplog.record_tuples if r[2] == warn_str]
    assert len(bcc_warning) == 2
    assert bcc_warning[0][1] == logging.WARNING

    res = MAGICCData(out_files[0])

    _do_generic_stitched_data_tests(res)
    _do_generic_normalised_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "ssp126" in child_path
    assert "r1i1p1f1" in child_path
    assert "BCC-CSM2-MR" in child_path
    assert "tas" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    parent_path = res.metadata["(parent) netcdf-scm crunched file"]
    assert "historical" in parent_path
    assert "r1i1p1f1" in child_path
    assert "BCC-CSM2-MR" in child_path
    assert "tas" in child_path

    parent = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", parent_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "piControl" in normalisation_path
    assert "r1i1p1f1" in normalisation_path
    assert "BCC-CSM2-MR" in normalisation_path
    assert "tas" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_cmip6_crunch_output, "*", normalisation_path)
    )[0]
    normalisation = load_scmdataframe(normalisation_path)

    assert parent.metadata["branch_time_in_parent"] == 2289.0
    assert parent.metadata["parent_time_units"] == "days since 1850-01-01"

    ref_values = _get_ref_values(
        res, normalisation, parent, normalisation_path, normalisation_method
    )

    _check_expected_values(res, child, range(2015, 2101), ref_values=ref_values)

    _check_expected_values(res, parent, range(1850, 2015), ref_values=ref_values)


def test_stitching_with_normalisation_two_levels_cmip5(
    tmpdir, caplog, test_marble_cmip5_crunch_output, normalisation_method
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_two_levels_cmip5"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_marble_cmip5_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "MarbleCMIP5",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*rcp45.*tas.*NorESM1.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_stitched_data_tests(res, cmip5=True)
    _do_generic_normalised_data_tests(res, cmip5=True)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "rcp45" in child_path
    assert "r1i1p1" in child_path
    assert "NorESM1-M" in child_path
    assert "tas" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_marble_cmip5_crunch_output, "*", child_path))[0]
    )

    parent_path = res.metadata["(parent) netcdf-scm crunched file"]
    assert "historical" in parent_path
    assert "r1i1p1" in child_path
    assert "NorESM1-M" in child_path
    assert "tas" in child_path

    parent = load_scmdataframe(
        glob.glob(os.path.join(test_marble_cmip5_crunch_output, "*", parent_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "piControl" in normalisation_path
    assert "r1i1p1" in normalisation_path
    assert "NorESM1-M" in normalisation_path
    assert "tas" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_marble_cmip5_crunch_output, "*", normalisation_path)
    )[0]

    normalisation = load_scmdataframe(normalisation_path)

    assert parent.metadata["branch_time"] == 255135.0

    ref_values = _get_ref_values(
        res, normalisation, parent, normalisation_path, normalisation_method
    )

    _check_expected_values(res, child, range(2006, 2101), ref_values=ref_values)

    _check_expected_values(res, parent, range(1850, 2006), ref_values=ref_values)


def test_stitching_with_normalisation_in_file_BCC_CSM2_MR(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_in_file_BCC_CSM2_MR"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*BCC-CSM2-MR.*1pctCO2-bgc.*r1i1p1f1.*tas.*",
                "--out-format",
                "mag-files-average-year-mid-year",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_normalised_data_tests(res)
    assert res.metadata["normalisation method"] == normalisation_method

    child_path = res.metadata["(child) netcdf-scm crunched file"]
    assert "1pctCO2-bgc" in child_path
    assert "r1i1p1f1" in child_path
    assert "BCC-CSM2-MR" in child_path
    assert "tas" in child_path

    child = load_scmdataframe(
        glob.glob(os.path.join(test_cmip6_crunch_output, "*", child_path))[0]
    )

    normalisation_path = res.metadata["(normalisation) netcdf-scm crunched file"]
    assert "piControl" in normalisation_path
    assert "r1i1p1f1" in normalisation_path
    assert "BCC-CSM2-MR" in normalisation_path
    assert "tas" in normalisation_path

    normalisation_path = glob.glob(
        os.path.join(test_cmip6_crunch_output, "*", normalisation_path)
    )[0]
    normalisation = load_scmdataframe(normalisation_path)

    assert child.metadata["branch_time_in_parent"] == 0.0
    assert child.metadata["parent_time_units"] == "days since 1850-01-01"

    ref_values = _get_ref_values(
        child, normalisation, child, normalisation_path, normalisation_method
    )

    _check_expected_values(
        res, child, range(1850, 2015), ref_values=ref_values, operation="time_mean_ac"
    )

    warn_str = (
        "Assuming BCC metadata is wrong and branch time units are actually years, "
        "not days"
    )
    bcc_warning = [r for r in caplog.record_tuples if r[2] == warn_str]
    # this file has a branch time of zero so the warning shouldn't be zero
    assert not bcc_warning


def test_stitching_with_normalisation_no_picontrol(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_no_picontrol"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*GFDL-CM4.*1pctCO2.*r1i1p1f1.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code != 0
    error_msg = re.compile(
        ".*No parent data \\(piControl\\) available for "
        ".*CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/1pctCO2/r1i1p1f1/Amon/tas/gr1/v20180701/netcdf-scm_tas_Amon_GFDL-CM4_1pctCO2_r1i1p1f1_gr1_000101-015012.nc"
        ", we looked in "
        ".*CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/piControl/r1i1p1f1/Amon/tas/gr1/\\*/netcdf-scm_tas_Amon_GFDL-CM4_piControl_r1i1p1f1_gr1_\\*.nc"
    )
    no_parent_error = [r for r in caplog.record_tuples if error_msg.match(r[2])]
    assert len(no_parent_error) == 1
    assert no_parent_error[0][1] == logging.ERROR


def test_stitching_with_normalisation_no_branching_time(
    tmpdir, caplog, test_cmip6_crunch_output, normalisation_method
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_no_branching_time"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*CNRM-CM6-1.*hist-aer.*tas.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code != 0
    error_msg = re.compile(
        ".*Branching time `188301` not available in piControl data in "
        "CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/piControl/r1i1p1f2/Amon/tas/gr/v20180814/netcdf-scm_tas_Amon_CNRM-CM6-1_piControl_r1i1p1f2_gr_230001-231012.nc"
    )
    no_branch_time_error = [r for r in caplog.record_tuples if error_msg.match(r[2])]
    assert len(no_branch_time_error) == 1
    assert no_branch_time_error[0][1] == logging.ERROR


def test_stitching_with_normalisation_not_enough_branching_time(
    tmpdir, caplog, test_cmip6_crunch_output
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching_with_normalisation_not_enough_branching_time"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*MIROC6.*r1i1p1f1.*rlut.*",
                "--normalise",
                "31-yr-mean-after-branch-time",
            ],
        )

    assert result.exit_code != 0
    error_msg = re.compile(
        ".*Only `320001` to `320212` is available after the branching time `320001` in piControl "
        "data in "
        "CMIP6/CMIP/MIROC/MIROC6/piControl/r1i1p1f1/Amon/rlut/gn/v20181212/netcdf-scm_rlut_Amon_MIROC6_piControl_r1i1p1f1_gn_320001-320212.nc"
    )
    not_enough_norm_data_error = [
        r for r in caplog.record_tuples if error_msg.match(r[2])
    ]
    assert len(not_enough_norm_data_error) == 1
    assert not_enough_norm_data_error[0][1] == logging.ERROR


@pytest.mark.parametrize(
    "out_format",
    (
        "magicc-input-files",
        "magicc-input-files-average-year-start-year",
        "magicc-input-files-average-year-mid-year",
        "magicc-input-files-average-year-end-year",
        "magicc-input-files-point-start-year",
        "magicc-input-files-point-mid-year",
        "magicc-input-files-point-end-year",
        "mag-files",
        "mag-files-average-year-start-year",
        "mag-files-average-year-mid-year",
        "mag-files-average-year-end-year",
        "mag-files-point-start-year",
        "mag-files-point-mid-year",
        "mag-files-point-end-year",
    ),
)
def test_stitching_file_types(
    tmpdir, caplog, test_cmip6_crunch_output, out_format, normalisation_method
):
    if normalisation_method == "21-yr-running-mean":
        pytest.xfail("Not enough data to take running mean")

    output_dir = str(tmpdir)
    crunch_contact = "test_stitching"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "--out-format",
                out_format,
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*BCC-CSM2-MR.*(ssp126|historical).*tas.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(
        os.path.join(
            output_dir, "flat", "*.IN" if out_format.startswith("magicc") else "*.MAG"
        )
    )
    assert len(out_files) == 4 if out_format.startswith("magicc") else 2

    for p in out_files:
        res = MAGICCData(p)
        _do_generic_normalised_data_tests(res)

        if "ssp126" in p:
            _do_generic_stitched_data_tests(res)

        if p.endswith(".MAG"):
            _do_filepath_time_consistency_check(res, p, annual="year" in out_format)


@pytest.mark.parametrize(
    "out_format",
    (
        "magicc-input-files",
        "magicc-input-files-average-year-start-year",
        "magicc-input-files-average-year-mid-year",
        "magicc-input-files-average-year-end-year",
        "magicc-input-files-point-start-year",
        "magicc-input-files-point-mid-year",
        "magicc-input-files-point-end-year",
        "mag-files",
        "mag-files-average-year-start-year",
        "mag-files-average-year-mid-year",
        "mag-files-average-year-end-year",
        "mag-files-point-start-year",
        "mag-files-point-mid-year",
        "mag-files-point-end-year",
    ),
)
def test_stitching_file_types_cmip5(
    tmpdir, caplog, test_marble_cmip5_crunch_output, out_format, normalisation_method
):
    output_dir = str(tmpdir)
    crunch_contact = "test_stitching"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level("DEBUG"):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_marble_cmip5_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "MarbleCMIP5",
                "--out-format",
                out_format,
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*(hist|rcp45).*tas.*NorESM1.*",
                "--normalise",
                normalisation_method,
            ],
        )

    assert result.exit_code == 0

    out_files = glob.glob(
        os.path.join(
            output_dir, "flat", "*.IN" if out_format.startswith("magicc") else "*.MAG"
        )
    )
    assert len(out_files) == 4 if out_format.startswith("magicc") else 2

    for p in out_files:
        res = MAGICCData(p)
        _do_generic_normalised_data_tests(res, cmip5=True)

        if "rcp45" in p:
            _do_generic_stitched_data_tests(res, cmip5=True)

        if p.endswith(".MAG"):
            _do_filepath_time_consistency_check(res, p, annual="year" in out_format)


@pytest.mark.parametrize(
    "out_format",
    (
        "magicc-input-files",
        "magicc-input-files-average-year-start-year",
        "magicc-input-files-average-year-mid-year",
        "magicc-input-files-average-year-end-year",
        "magicc-input-files-point-start-year",
        "magicc-input-files-point-mid-year",
        "magicc-input-files-point-end-year",
        "mag-files",
        "mag-files-average-year-start-year",
        "mag-files-average-year-mid-year",
        "mag-files-average-year-end-year",
        "mag-files-point-start-year",
        "mag-files-point-mid-year",
        "mag-files-point-end-year",
    ),
)
def test_prefix(tmpdir, caplog, test_cmip6_crunch_output, out_format):
    output_dir = str(tmpdir)
    crunch_contact = "test_prefix"
    prefix = "NORMED"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*BCC-CSM2-MR.*ssp126.*tas.*",
                "--out-format",
                out_format,
                "--prefix",
                prefix,
            ],
        )

    assert result.exit_code == 0, result.stderr

    out_files = glob.glob(
        os.path.join(
            output_dir, "flat", "*.IN" if out_format.startswith("magicc") else "*.MAG"
        )
    )
    assert len(out_files) == 2 if out_format.startswith("magicc") else 1
    assert [os.path.basename(p).startswith("{}_".format(prefix)) for p in out_files]


def test_target_units(tmpdir, caplog, test_cmip6_crunch_output):
    target_unit = "J / yr / m^2"
    target_units = pd.DataFrame(
        [["fgco2", "g / m**2 / s"], ["hfds", target_unit]], columns=["variable", "unit"]
    )
    target_units_csv = os.path.join(tmpdir, "target_units.csv")
    target_units.to_csv(target_units_csv, index=False)

    output_dir = str(tmpdir)
    crunch_contact = "test_target_units"

    runner = CliRunner(mix_stderr=False)
    with caplog.at_level(logging.WARNING):
        result = runner.invoke(
            stitch_netcdf_scm_ncs,
            [
                test_cmip6_crunch_output,
                output_dir,
                crunch_contact,
                "--drs",
                "CMIP6Output",
                "-f",
                "--number-workers",
                1,
                "--regexp",
                ".*EC-Earth3-Veg.*ssp585.*r1i1p1f1.*hfds.*",
                "--target-units-specs",
                target_units_csv,
            ],
        )

    assert result.exit_code == 0, result.stderr

    out_files = glob.glob(os.path.join(output_dir, "flat", "*.MAG"))
    assert len(out_files) == 1

    res = MAGICCData(out_files[0])

    _do_generic_stitched_data_tests(res)
    _do_filepath_time_consistency_check(res, out_files[0])
    assert res["unit"].unique().tolist() == ["Jperyrpermsuper2"]
    assert "Converting units" in result.stderr
