import sys
import blender_addon_tester as BAT

addon = "fake_addon"
if len(sys.argv) >= 2:
    blender_rev = sys.argv[1]
else:
    blender_rev = "2.80"

BAT.test_blender_addon(blender_rev, addon, "tests/")
