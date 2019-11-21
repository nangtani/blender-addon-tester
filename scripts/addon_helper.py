import os
import sys
import re
import time
import zipfile
import shutil
import bpy


def zip_addon(addon, addon_dir):
    bpy_module = re.sub(".py", "", os.path.basename(os.path.realpath(addon)))

    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)

    zfile = os.path.realpath(bpy_module + ".zip")

    print("Zipping addon - {0}".format(bpy_module))

    zf = zipfile.ZipFile(zfile, "w")
    if os.path.isdir(addon):
        for dirname, subdirs, files in os.walk(addon):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
    else:
        zf.write(addon)
    zf.close()
    return (bpy_module, zfile)


def change_addon_dir(bpy_module, zfile, addon_dir):
    print("Change addon dir - {0}".format(addon_dir))


    if (2, 80, 0) < bpy.app.version:
        bpy.context.preferences.filepaths.script_directory = addon_dir
        bpy.utils.refresh_script_paths()
        bpy.ops.preferences.addon_install(overwrite=True, filepath=zfile)
        bpy.ops.preferences.addon_enable(module=bpy_module)
    else:
        bpy.context.user_preferences.filepaths.script_directory = addon_dir
        bpy.utils.refresh_script_paths()
        bpy.ops.wm.addon_install(overwrite=True, filepath=zfile)
        bpy.ops.wm.addon_enable(module=bpy_module)


def cleanup(addon, bpy_module, addon_dir):
    print("Cleaning up - {}".format(bpy_module))
    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)


def get_version(bpy_module):
    mod = sys.modules[bpy_module]
    return mod.bl_info.get("version", (-1, -1, -1))
