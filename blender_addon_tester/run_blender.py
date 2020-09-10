import os
import sys
import subprocess
import re
import shutil
import zipfile
import tempfile
from pathlib import Path
from glob import glob
from .get_blender import get_blender_from_suffix
from .addon_helper import zip_module, import_module_into_blender, cleanup


CURRENT_MODULE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
BUILTIN_BLENDER_LOAD_TESTS_SCRIPT = os.path.join(CURRENT_MODULE_DIRECTORY, "blender_load_pytest.py")

def _run_blender_with_python_script(blender, blender_python_script, app_template_name=""):
    local_python = CURRENT_MODULE_DIRECTORY
    os.environ["LOCAL_PYTHONPATH"] = local_python
    
    # Set the application template call if specified
    app_template_command = f"--app-template {app_template_name}" if app_template_name else ""

    cmd = f'{blender} -b --python "{blender_python_script}" {app_template_command}'
    print(f"Will run the following command: {cmd}")

    # TODO Clean up Blender
    result = int(os.system(cmd))
    if 0 == result:
        return 0
    else:
        return 1

def test_existing_modules(blender_revision, addon_path, blender):
    addon = addon_path
    rev = re.sub("[a-z]$", "", blender_revision)
    if "darwin" == sys.platform:
        loc = os.path.realpath(f"{blender}/../../Resources/{rev}/scripts")
    else:
        loc = os.path.realpath(f"{blender}/../{rev}/scripts")

    loc = f"{loc}/*/{addon}"
    files = glob(loc)
    for addon in files:
        zfile = f"{addon}.zip"
        zf = zipfile.ZipFile(zfile, "w")
        if os.path.isdir(addon):
            for dirname, subdirs, files in os.walk(addon):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
        else:
            zf.write(addon)
        zf.close()
        
        if os.path.isdir(addon):
            shutil.rmtree(os.path.realpath(addon))
        else:
            os.unlink(os.path.realpath(addon))

def run_blender_version_for_addon_with_pytest_suite(addon_path="", app_template_path="", blender_exec_path="", blender_revision=None, config={}, dir_to_ignore=set()):
    """
    Run tests for "blender_revision" x "addon" using the builtin "blender_load_pytest.py" script or "custom_blender_load_tests_script"

    :param addon: Addon path to test, can be a path to a directory (will be zipped for you) or to a .zip file. The Python module name will be that of the (directory or) zip file without extension, try to make it as pythonic as possible for Blender's Python importer to work properly with it: letters, digits, underscores.
    :param blender_revision: Version of Blender3d. Default: "2.82"
    :param config: A options dictionary, its keys allow to override some defaults:
                    "blender_load_tests_script": str: absolute or CWD-relative path to the Blender Python scripts that loads and runs tests. Default: "blender_load_tests_script.py" (packaged with this module)
                    "coverage": bool: whether or not run coverage evaluation along tests; Default: False (no coverage evaluation) 
                    "tests": str: absolute or CWD-relative path to a directory of tests or test script that the blender_load_tests_script can use. Default: "tests/" (CWD-relative)
                    "blender_cache": str: absolute or CWD-relative path to a directory where to download and extract Blender3d releases.
    :param dir_to_ignore: Set of directories to ignore when zipping the addon.
    :return: None, will sys-exit with 1 on failure
    """
    if None == blender_revision:
        blender_revision = "2.82"
        print("No blender_revision given, defaulting to {blender_revision}.")

    print("testing addon_path:", addon_path, "under blender_revision:", blender_revision, "with config dict:", config)

    # Get Blender for the given version in a cached way
    if not blender_exec_path:
        downloaded_blender_dir = get_blender_from_suffix(blender_revision)
        print("Downloaded Blender is expected in this directory: ", downloaded_blender_dir)

        # Tune configuration
        DEFAULT_CONFIG = {"blender_load_tests_script": os.path.join(CURRENT_MODULE_DIRECTORY, "blender_load_pytest.py"), "coverage": False}
        # Let the provided config dict override the default one
        config = dict(DEFAULT_CONFIG, **config)

        if "win32" == sys.platform or "win64" == sys.platform or "cygwin" == sys.platform:
            ext = ".exe"
        else:
            ext = ""

        if "darwin" == sys.platform:
            blender_executable_root = f"{downloaded_blender_dir}/MacOS/*lender"
        else:
            blender_executable_root = f"{downloaded_blender_dir}/blender{ext}"

        files = glob(blender_executable_root)
        if not 1 == len(files):
            if len(files) == 0:
                raise Exception(f"No blenders found in directory {blender_executable_root}: {files}")
            else:
                raise Exception(f"Too many blenders found in directory {blender_executable_root}: {files}")
        
        blender = os.path.realpath(files[0])
    else:
        blender = blender_exec_path

    if config.get("blender_cache", None):
        os.environ["BLENDER_CACHE"] = config["blender_cache"]
#     else:
#         os.environ["BLENDER_CACHE"] = ".."
    config_keys = [
        "blender_load_tests_script",
        "coverage",
        "tests",
        "pytest_args",
    ]
    for c in config.keys():
        if not c in config_keys:
            raise Exception(f"Unknown key for config:\n\t{c}")

    # Set the test file
    test_file = config.get("blender_load_tests_script")

    if not config.get("coverage"):
        if os.environ.get("BLENDER_ADDON_COVERAGE_REPORTING"):
            del os.environ["BLENDER_ADDON_COVERAGE_REPORTING"]
    else:
        os.environ["BLENDER_ADDON_COVERAGE_REPORTING"] = "y"

    if not config.get("tests"):
        if os.environ.get("BLENDER_ADDON_TESTS_PATH"):
            del os.environ["BLENDER_ADDON_TESTS_PATH"]
    else:
        os.environ["BLENDER_ADDON_TESTS_PATH"] = config["tests"] 

    if not config.get("pytest_args"):
        if os.environ.get("BLENDER_PYTEST_ARGS"):
            del os.environ["BLENDER_PYTEST_ARGS"]
    else:
        os.environ["BLENDER_PYTEST_ARGS"] = config["pytest_args"] 

    test_existing_modules(blender_revision, addon_path, blender)

    # Import the module into Blender
    temp_dir = Path(tempfile.gettempdir()).joinpath("blender_python_test")
    bpy_module, zfile = zip_module(blender, app_template_path, temp_dir, dir_to_ignore=dir_to_ignore)
    import_module_into_blender(blender, bpy_module, zfile, temp_dir, module_type="APP_TEMPLATE")

    app_template_name = os.path.basename(app_template_path).split(".zip")[0]
    # Run tests with the proper Blender version and configured tests
    return _run_blender_with_python_script(blender, test_file, app_template_name)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        blender_rev = sys.argv[1]
        addon = sys.argv[2]
        sys.exit(run_blender_version_for_addon_with_pytest_suite(blender_revision=blender_rev, addon_path=addon))
    else:
        print("Usage:", sys.argv[0], "blender_rev addon")
        sys.exit(1)

