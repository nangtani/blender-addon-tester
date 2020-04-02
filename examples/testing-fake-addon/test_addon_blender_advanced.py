import sys
import os
try:
    import blender_addon_tester as BAT
except Exception as e:
    print(e)
    sys.exit(1)

def main():    
    if len(sys.argv) > 1:
        addon = sys.argv[1]
    else:
        addon = "fake_addon"
    if len(sys.argv) > 2:
        blender_rev = sys.argv[2]
    else:
        blender_rev = "2.80"
    
    here = os.path.dirname(os.path.realpath(__file__))
    config = {"blender_load_tests_script": os.path.join(here, "blender_advanced_load_pytest.py"), "coverage": True, "tests": "advanced_tests/"}

    try:
        exit_val = BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev, config=config)
    except Exception as e:
        print(e)
        exit_val = 1
    sys.exit(exit_val)

main()
