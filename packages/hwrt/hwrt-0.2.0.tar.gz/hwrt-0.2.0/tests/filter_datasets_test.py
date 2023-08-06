#!/usr/bin/env python

# Core Library modules
import os

# Third party modules
import pkg_resources

# First party modules
import hwrt.filter_dataset as filter_dataset


# Tests
def test_main_execution():
    misc_path = pkg_resources.resource_filename("hwrt", "misc/")
    tests_path = os.path.join(os.path.dirname(__file__), "data/")
    symbol_yml_file = os.path.join(misc_path, "symbols.yml")
    raw_pickle_file = os.path.join(tests_path, "unittests-tiny-raw.pickle")
    pickle_dest_path = os.path.join(
        tests_path, "unittests-tiny-raw-filtered-tmp.pickle"
    )
    filter_dataset.main(symbol_yml_file, raw_pickle_file, pickle_dest_path)


def test_get_metadata():
    metadata = filter_dataset.get_metadata()
    assert len(metadata) == 3
