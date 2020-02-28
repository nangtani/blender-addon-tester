from . import get_blender
from . import run_blender

def test_blender_addon(blender_version="2.80", addon_name="fake_addon", pytests_path="tests/"):
    print("testing ", addon_name, "under", blender_version, "with tests at:", pytests_path)
    get_blender.get_blender_from_suffix(blender_version) # TODO exit code checking
    run_blender.run_blender_version_with_pytest_suite(blender_version)
    # TODO more steps: ensure coverage is OK
