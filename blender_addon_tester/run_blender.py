import os
import sys
import subprocess
from glob import glob
from .get_blender import get_blender_from_suffix

CURRENT_MODULE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
BUILTIN_BLENDER_LOAD_TESTS_SCRIPT = os.path.join(CURRENT_MODULE_DIRECTORY, "blender_load_pytest.py")


def checkPath(path):
    if "cygwin" == sys.platform:
        cmd = "cygpath -wa {0}".format(path)
        path = subprocess.check_output(cmd.split()).decode("ascii").rstrip()
    return path


def _run_blender_with_python_script(blender, blender_python_script):
    blender_python_script = checkPath(blender_python_script)
    local_python = checkPath(CURRENT_MODULE_DIRECTORY)
    os.environ["LOCAL_PYTHONPATH"] = local_python

    cmd = f'{blender} -b --python "{blender_python_script}"'
    result = int(os.system(cmd))
    if 0 == result:
        return 0
    else:
        return 1


def run_blender_version_for_addon_with_pytest_suite(addon_path, blender_revision="2.80", config={}):
    """
    Run tests for "blender_revision" x "addon" using the builtin "blender_load_pytest.py" script or "custom_blender_load_tests_script"

    :param addon: Addon path (or name if in current directory) to test.
    :param blender_revision: Version of Blender3d. Eg. "2.80"
    :param config: A options dictionary, its keys allow to override some defaults:
                    "blender_load_tests_script": str: absolute or CWD-relative path to the Blender Python scripts that loads and runs tests. Default: "blender_load_tests_script.py" (packaged with this module)
                    "coverage": bool: whether or not run coverage evaluation along tests; Default: False (no coverage evaluation) 
                    "tests": str: absolute or CWD-relative path to a directory of tests or test script that the blender_load_tests_script can use. Default: "tests/" (CWD-relative)
    :return: None, will sys-exit with 1 on failure
    """
    print("testing ", addon_path, "under", blender_rev, "with config", config)

    # Get Blender for the given version in a cached way
    get_blender_from_suffix(blender_rev)

    # Tune configuration
    DEFAULT_CONFIG = {"blender_load_tests_script": BUILTIN_BLENDER_LOAD_TESTS_SCRIPT, "coverage": False}
    # Let the provided config dict override the default one
    config = dict(DEFAULT_CONFIG, **config)

    if "win32" == sys.platform or "win64" == sys.platform or "cygwin" == sys.platform:
        ext = ".exe"
    else:
        ext = ""

    files = glob(f"../blender-{blender_revision}*/blender{ext}")
    if not 1 == len(files):
        raise Exception(f"Too many blenders returned: {files}")
    
    blender = os.path.realpath(files[0])

    os.environ["BLENDER_ADDON_TO_TEST"] = addon_path

    if not config["blender_load_tests_script"]:
        test_file = BUILTIN_BLENDER_LOAD_TESTS_SCRIPT
    else:
        test_file = config["blender_load_tests_script"]

    if not config["coverage"]:
        del os.environ["BLENDER_ADDON_COVERAGE_REPORTING"]
    else:
        os.environ["BLENDER_ADDON_COVERAGE_REPORTING"] = "y"

    if not config["tests"]:
        del os.environ["BLENDER_ADDON_TESTS_PATH"]
    else:
        os.environ["BLENDER_ADDON_TESTS_PATH"] = config["tests"] 

    # Run tests with the proper Blender version and configured tests
    return _run_blender_with_python_script(blender, test_file)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        blender_rev = sys.argv[1]
        addon = sys.argv[2]
        sys.exit(run_blender_version_with_pytest_suite(blender_rev, addon))
    else:
        print("Usage:", sys.argv[0], "blender_rev addon")
        sys.exit(1)

