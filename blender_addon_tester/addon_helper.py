import os
import sys
import re
import time
import zipfile
import shutil
import bpy

def clean_file(filename):
    """ Cleans up addons files so that any blender version code is strip to be compliant with addon guidelines
    :param filename     Path to addon file
    :return None
    """
    print('file:', filename)
    f = open(filename, "r")
    try:
        lines = f.readlines()
    except:
        lines = ""
        pass

    f.close()

    unique_blender = True
    fix_fstrings = False
    if bpy.app.version <= (2, 79, 0):
        fix_fstrings = True

    trim_code = False
    active_print0 = None
    f = open(filename, "w")
    for line in lines:
        if unique_blender:
            line2 = line
            if re.search("^\s+else", line) and re.search("else bpy.app.version", line):
                active_print0 = not (active_print0)
                line2 = "\n"

            if re.search("endif", line):
                active_print0 = None
                trim_code = False
                line2 = "\n"

            h = re.search("^\s+[el]?if \((\d+), (\d+), (\d+)\) < bpy.app.version", line)
            if h:
                current_blender_rev = (
                    int(h.group(1)),
                    int(h.group(2)),
                    int(h.group(3)),
                )
                trim_code = True
                active_print0 = current_blender_rev <= bpy.app.version
                line2 = "\n"

            if trim_code:
                line2 = re.sub("^    ", "", line2)
            if not active_print0 and not active_print0 == None:
                line2 = "\n"
            line = line2

        k = re.search('"blender":\s\(\d+, \d+, \d+\)', line)
        if k:
            line = '    "blender": {0},\n'.format(bpy.app.version)

        if re.search('print\(f"', line) and fix_fstrings:
            line = re.sub("print", "pass ; # print", line)
        f.write(line)
    f.close()

def zip_module(addon, addon_dir):
    """ Zips 'addon' dir or '.py' file to 'addon.zip' if not yet zipped, then moves the archive to 'addon_dir'.
    :param addon     Absolute or relative path to a directory to zip or a .zip file.
    :param addon_dir Path to Blender's addon directory to move the zipped archive to.
    :return (bpy_module, zip_file) Tuple of strings - an importable module name, an addon zip file path.
    """
    already_zipped = False

    addon_path = os.path.realpath(addon)
    addon_basename = os.path.basename(addon_path)

    if addon_basename.endswith(".zip"):
        already_zipped = True

    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)
    os.mkdir(addon_dir)

    print("Addon dir is - {0}".format(os.path.realpath(addon_dir)))
    if not already_zipped:
        bpy_module = re.sub(".py", "", addon_basename)
        zfile = os.path.realpath(bpy_module + ".zip")

        print("Future zip path is - {0}".format(zfile))

        print("Zipping addon - {0}".format(bpy_module))


        zf = zipfile.ZipFile(zfile, "w")
        if os.path.isdir(addon):
            cwd = os.getcwd()
            temp_dir = "tmp"
            if os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)
        
            shutil.copytree(addon, temp_dir + "/" + addon)
            os.chdir(temp_dir)
            if os.path.isdir("__pycache__"):
                shutil.rmtree("__pycache__")
            for dirname, subdirs, files in os.walk(addon):
                zf.write(dirname)
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    clean_file(filename)
                    zf.write(filename)
            os.chdir(cwd)
            shutil.rmtree(temp_dir)
        else:
            clean_file(addon)
            zf.write(addon)
        zf.close()
    else:
        zfile = addon_path
        print("Detected zip path is - {0}. No need to zip the addon beforehand.".format(zfile))

        bpy_module = addon_basename.split(".zip")[0]

    brev = "{0}.{1}".format(bpy.app.version[0], bpy.app.version[1])
    bfile = re.sub(".zip", "_{}.zip".format(brev), zfile)
    shutil.copy(zfile, bfile)
    return (bpy_module, bfile)


def import_module_into_blender(bpy_module, zfile, addon_dir, module_type="ADDON"):
    print("Change addon dir - {0}".format(addon_dir))

    if module_type == "ADDON":
        if (2, 80, 0) < bpy.app.version:
            # https://docs.blender.org/api/current/bpy.types.PreferencesFilePaths.html#bpy.types.PreferencesFilePaths.script_directory
            # requires restart
            bpy.context.preferences.filepaths.script_directory = addon_dir
            bpy.utils.refresh_script_paths()
            bpy.ops.preferences.addon_install(overwrite=True, filepath=zfile)
            bpy.ops.preferences.addon_enable(module=bpy_module)
        else:
            bpy.context.user_preferences.filepaths.script_directory = addon_dir
            bpy.utils.refresh_script_paths()
            bpy.ops.wm.addon_install(overwrite=True, filepath=zfile)
            bpy.ops.wm.addon_enable(module=bpy_module)
    elif module_type == "APP_TEMPLATE":
        bpy.ops.preferences.app_template_install(overwrite=True, filepath=zfile)


def cleanup(addon, bpy_module, addon_dir):
    print("Cleaning up - {}".format(bpy_module))
    if (2, 80, 0) < bpy.app.version:
        bpy.ops.preferences.addon_disable(module=bpy_module)
    else:
        bpy.ops.wm.addon_disable(module=bpy_module)
    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)


def get_version(bpy_module):
    mod = sys.modules[bpy_module]
    return mod.bl_info.get("version", (-1, -1, -1))


def get_bl_version():
    return bpy.app.version
