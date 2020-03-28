import sys
import os
import zipfile
try:
    import blender_addon_tester as BAT
except Exception as e:
    print(e)
    sys.exit(1)

def zipdir(path, ziph):
    # Per https://www.tutorialspoint.com/How-to-zip-a-folder-recursively-using-Python
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def main():    
    if len(sys.argv) > 1:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"
    if len(sys.argv) > 2:
        addon = sys.argv[2]
    else:
        addon = "fake_addon"
    
    zipf = zipfile.ZipFile('fake_addon.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('./fake_addon', zipf)
    zipf.close()

    here = os.path.dirname(os.path.realpath(__file__))
    config = {"coverage": True, "tests": "advanced_tests/"}

    try:
        exit_val = BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev, config=config)
    except Exception as e:
        print(e)
        exit_val = 1
    sys.exit(exit_val)

main()