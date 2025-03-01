# This is a script that can you pipe to Blender directly. It populates and runs pytest tests.
# You may have your own version of this file, by copying it and piping its filename to
# run_blender_version_with_pytest_suite(override_test_file="my_load_test.py")

import os
from pathlib import Path
import sys
try:
    import pytest
except Exception as e:
    print(e)
    sys.exit(1)

# Make sure to have BLENDER_ADDON_TO_TEST set as an environment variable first
ADDON = os.environ.get("BLENDER_ADDON_TO_TEST", False)
if not ADDON:
    print("No addon to test was found in the 'BLENDER_ADDON_TO_TEST' environment variable. Exiting.")
    sys.exit(1)

# Set any value to the BLENDER_ADDON_COVERAGE_REPORTING environment variable to enable it
COVERAGE_REPORTING = os.environ.get("BLENDER_ADDON_COVERAGE_REPORTING", False)
# The Pytest tests/ path can be overriden through the BLENDER_ADDON_TESTS_PATH environment variable
default_tests_dir = Path(ADDON).parent.joinpath("tests")
TESTS_PATH = os.environ.get("BLENDER_ADDON_TESTS_PATH", default_tests_dir.as_posix())
# Add explict pytest commands, just in case fine control is required
PYTEST_ARGS = os.environ.get("BLENDER_PYTEST_ARGS", "")

try:
    sys.path.append(os.environ["LOCAL_PYTHONPATH"])
    from addon_helper import zip_addon, change_addon_dir, install_addon, cleanup
except Exception as e:
    print(e)
    sys.exit(1)

# This is needed for windows, doesn't seem to affect linux
addon_helper = os.environ.get("ADDON_TEST_HELPER", None)
if None == addon_helper:
    pass
elif os.path.isdir(addon_helper):
    sys.path.append(addon_helper)

class SetupPlugin:
    def __init__(self, addon):
        self.addon = addon
        self.addon_dir = "local_addon"
        self.bpy_module = None
        self.zfile = None

    def pytest_configure(self, config):
        (self.bpy_module, self.zfile) = zip_addon(self.addon, self.addon_dir)
        change_addon_dir(self.bpy_module, self.addon_dir)
        install_addon(self.bpy_module, self.zfile, self.addon_dir)
        config.cache.set("bpy_module", self.bpy_module)

    def pytest_unconfigure(self):
        cleanup(self.addon, self.bpy_module, self.addon_dir)
        print("*** test run reporting finished")


try:
    pytest_main_args = [TESTS_PATH, "-v", "-x"]
    if COVERAGE_REPORTING is not False:
        pytest_main_args += ["--cov", "--cov-report", "term", "--cov-report", "xml"]
        if not "" == PYTEST_ARGS:
            pytest_main_args += [PYTEST_ARGS]
    exit_val = pytest.main(pytest_main_args, plugins=[SetupPlugin(ADDON)])
except Exception as e:
    print(e)
    exit_val = 1
sys.exit(exit_val)
