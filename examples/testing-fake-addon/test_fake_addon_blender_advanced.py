import sys
import os
import blender_addon_tester as BAT

if __name__ == "__main__":
    addon = "fake_addon"
    print("SYS.ARGV IS:", sys.argv)
    if len(sys.argv) > 1:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"
    
    here = os.path.dirname(os.path.realpath(__file__))
    config = {"blender_load_tests_script": os.path.join(here, "blender_advanced_load_pytest.py"), "coverage": True, "tests": "advanced_tests/"}

    BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev, config=config)
