import os
import sys
import subprocess
from glob import glob

CURRENT_MODULE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


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


def run_blender_version_with_pytest_suite(blender_revision, addon, override_test_file=None):
    """
    Run tests for "blender_revision" x "addon" using the builtin "blender_load_pytest.py" script or "override_test_file"

    :param blender_revision: Version of Blender3d. Eg. "2.80"
    :param addon: Addon path (or name if in current directory) to test.
    :param override_test_file: Any path to a script runnable in Blender, replacing the default blender_load_pytest.py
    :return:
    """
    if "win32" == sys.platform or "win64" == sys.platform or "cygwin" == sys.platform:
        ext = ".exe"
    else:
        ext = ""

    files = glob(f"../blender-{blender_revision}*/blender{ext}")
    if not 1 == len(files):
        raise Exception(f"Too many blenders returned: {files}")
    
    blender = os.path.realpath(files[0])

    os.environ["BLENDER_ADDON_TO_TEST"] = addon

    if not override_test_file:
        test_file = os.path.join(CURRENT_MODULE_DIRECTORY, "blender_load_pytest.py")
    else:
        test_file = override_test_file

    return _run_blender_with_python_script(blender, test_file)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        blender_rev = sys.argv[1]
        addon = sys.argv[2]
        sys.exit(run_blender_version_with_pytest_suite(blender_rev, addon))
    else:
        print("Usage:", sys.argv[0], "blender_rev addon")
        sys.exit(1)

