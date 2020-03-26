import sys
try:
    import blender_addon_tester as BAT
except Exception as e:
    print(e)
    sys.exit(1)
    
if __name__ == "__main__":
    addon = "fake_addon"
    if len(sys.argv) > 1:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"
    
    try:
        exit_val = BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev)
    except Exception as e:
        print(e)
        exit_val = 1
    sys.exit(exit_val)
