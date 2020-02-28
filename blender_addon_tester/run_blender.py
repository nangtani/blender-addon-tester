import os
import sys
import subprocess
import re
from glob import glob


def checkPath(path):
    if "cygwin" == sys.platform:
        cmd = "cygpath -wa {0}".format(path)
        path = subprocess.check_output(cmd.split()).decode("ascii").rstrip()
    return path


def run_blender_with_python_script(blender, test_file):
    test_file = checkPath(test_file)
    local_python = checkPath(os.getcwd())
    os.environ["LOCAL_PYTHONPATH"] = local_python

    cmd = f'{blender} -b --python "{test_file}"'
    result = int(os.system(cmd))
    if 0 == result:
        return 0
    else:
        return 1

def run_blender_version_with_pytest_suite(blender_rev):
    if "win32" == sys.platform or "win64" == sys.platform or "cygwin" == sys.platform:
        ext = ".exe"
    else:
        ext = ""

    files = glob(f"../blender-{blender_rev}*/blender{ext}")
    if not 1 == len(files):
        raise Exception(f"Too many blenders returned: {files}")
    
    blender = os.path.realpath(files[0])

    test_file = "load_pytest.py"

    return run_blender_with_python_script(blender, test_file)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"

    sys.exit(run_blender_version_with_pytest_suite(blender_rev))
