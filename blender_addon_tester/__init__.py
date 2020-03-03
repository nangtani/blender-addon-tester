import os

from .get_blender import get_blender_from_suffix
from .run_blender import run_blender_version_with_pytest_suite


def test_blender_addon(addon_path, blender_rev="2.80", custom_test_file=None):
    print("testing ", addon_path, "under", blender_rev, "with custom_test_file", custom_test_file)
    get_blender_from_suffix(blender_rev)
    run_blender_version_with_pytest_suite(blender_rev, addon_path, custom_test_file)
