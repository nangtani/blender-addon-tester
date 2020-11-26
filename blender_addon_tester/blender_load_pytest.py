# This is a script that can you pipe to Blender directly. It populates and runs pytest tests.
# You may have your own version of this file, by copying it and piping its filename to
# run_blender_version_with_pytest_suite(override_test_file="my_load_test.py")

import os
import sys
try:
    import pytest
except Exception as e:
    print(e)
    sys.exit(1)

# Make sure to have BLENDER_ADDON_TO_TEST set as an environment variable first
ADDON = os.environ.get("BLENDER_ADDON_TO_TEST", False)
APP_TEMPLATE = os.environ.get("BLENDER_APP_TEMPLATE_TO_TEST", False)
if not ADDON:
    print("No addon to test was found in the 'BLENDER_ADDON_TO_TEST' environment variable. Exiting.")
    # sys.exit(1)

# Set any value to the BLENDER_ADDON_COVERAGE_REPORTING environment variable to enable it
COVERAGE_REPORTING = os.environ.get("BLENDER_ADDON_COVERAGE_REPORTING", False)
# The Pytest tests/ path can be overriden through the BLENDER_ADDON_TESTS_PATH environment variable
TESTS_PATH = os.environ.get("BLENDER_ADDON_TESTS_PATH", "tests")

# Add explict pytest commands, just in case fine control is required
PYTEST_ARGS = os.environ.get("BLENDER_PYTEST_ARGS", "")

try:
    sys.path.append(os.environ["LOCAL_PYTHONPATH"])
    from addon_helper import zip_module, import_module_into_blender, cleanup
except Exception as e:
    print(e)
    sys.exit(1)

addon_helper = os.environ.get("ADDON_TEST_HELPER", None)
if not None == addon_helper:
    sys.path.append(addon_helper)

class SetupPlugin:
    def __init__(self, addon="", app_template=""):
        self.addon = addon
        self.app_template = app_template
        self.addon_dir = "local_addon"
        self.bpy_module = None
        self.zfile = None

    def pytest_configure(self, config):
        if self.addon:
            (self.bpy_module, self.zfile) = zip_module(self.addon, self.addon_dir)
            import_module_into_blender(self.bpy_module, self.zfile, self.addon_dir)
        if self.app_template:
            (self.bpy_module, self.zfile) = zip_module(self.app_template, self.addon_dir)
            import_module_into_blender(self.bpy_module, self.zfile, self.addon_dir, module_type="APP_TEMPLATE")

        config.cache.set("bpy_module", self.bpy_module)

    def pytest_unconfigure(self):
        cleanup(self.bpy_module, self.addon_dir, "APP_TEMPLATE")
        print("*** test run reporting finished")


try:
    pytest_main_args = ["/Users/felixdavid/Documents/Logiciels/Stax/stax/tests/", "-v", "-x"]
    if COVERAGE_REPORTING is not False:
        pytest_main_args += ["--cov", "--cov-report", "term", "--cov-report", "xml"]
        if not "" == PYTEST_ARGS:
            pytest_main_args += [PYTEST_ARGS]
    exit_val = pytest.main(pytest_main_args, plugins=[SetupPlugin(addon=ADDON, app_template=APP_TEMPLATE)])
except Exception as e:
    print(e)
    exit_val = 1
sys.exit(exit_val)
