from get_blender import get_blender_from_suffix

def test_blender_addon(blender_version="2.80", addon_name="fake_addon", pytests_path="tests/"):
    print("testing ", addon_name, "under", blender_version, "with tests at:", pytests_path)
    get_blender_from_suffix(blender_version)
    # TODO more steps: run pytests, ensure coverage is OK
