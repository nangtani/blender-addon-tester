import sys
import blender_addon_tester as BAT

if __name__ == "__main__":
    addon = "fake_addon"
    if len(sys.argv) > 1:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"
    
    BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev)
