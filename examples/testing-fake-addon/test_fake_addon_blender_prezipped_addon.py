import sys
import os
import zipfile
import blender_addon_tester as BAT

def zipdir(path, ziph):
    # Per https://www.tutorialspoint.com/How-to-zip-a-folder-recursively-using-Python
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == "__main__":
    zipf = zipfile.ZipFile('fake_addon.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('./fake_addon', zipf)
    zipf.close()
    addon = "fake_addon.zip"

    if len(sys.argv) > 1:
        blender_rev = sys.argv[1]
    else:
        blender_rev = "2.80"
    
    here = os.path.dirname(os.path.realpath(__file__))
    config = {"coverage": True, "tests": "advanced_tests/"}

    print("WILL TEST WITH BLENDER_REVISION=", blender_rev)
    BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev, config=config)
