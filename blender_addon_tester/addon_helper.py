import os
import re
import sys
import shutil
import time
import zipfile
from pathlib import Path
from tempfile import gettempdir

import bpy

def clean_file(filename):
    """ Cleans up addons files so that any blender version code is strip to be compliant with addon guidelines
    :param filename     Path to addon file
    :return None
    """
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    unique_blender = True

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
            line = f'    "blender": {bpy.app.version},\n'

        f.write(line)
    f.close()

def zip_addon(addon: str, addon_dir: str):
    """ Zips 'addon' dir or '.py' file to 'addon.zip' if not yet zipped, then moves the archive to 'addon_dir'.

    :param addon: Absolute or relative path to a directory to zip or a .zip file.
    :param addon_dir: Path to Blender's addon directory to move the zipped archive to.
    :return (bpy_module, zip_file) Tuple of strings - an importable module name, an addon zip file path.
    """
    addon_path = Path(addon).resolve()
    addon_basename = addon_path.name

    # Check if addon is already zipped
    already_zipped = False
    if addon_basename.endswith(".zip"):
        already_zipped = True

    # Delete target addon dir if exists
    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)
    os.mkdir(addon_dir)

    print(f"Addon dir is - {os.path.realpath(addon_dir)}")
    if not already_zipped:  # Zip the addon
        # Get bpy python module from addon file name
        bpy_module = re.sub(".py", "", addon_basename)

        # Create zip archive using the module name
        zfile = Path(f"{bpy_module}.zip").resolve()

        print(f"Future zip path is - {zfile}")

        print(f"Zipping addon - {bpy_module}")

        # Zip addon content
        # -------------------
        zf = zipfile.ZipFile(zfile, "w")
        if addon_path.is_dir():  # Addon is a directory, zip hierarchy
            cwd = os.getcwd()
            temp_dir = Path(gettempdir(), "blender_addon_tester")

            # Clean temp dir if already exists
            if temp_dir.is_dir():
                shutil.rmtree(temp_dir)

            # Creating the addon under the temp dir with its hierarchy 
            temp_dir_dst = temp_dir.joinpath(addon_path.relative_to(addon_path.anchor))
            shutil.copytree(addon_path, temp_dir_dst)

            # Move to temp dir
            os.chdir(temp_dir_dst)


            # Write addon content into archive
            for dirname, subdirs, files in os.walk(temp_dir_dst):
                for filename in files:
                    # Ignore pycache files
                    if filename.endswith('.pyc'):
                        continue

                    filename = os.path.join(dirname, filename)

                    # Clean file
                    if filename.endswith('.py'):
                        clean_file(filename)

                    # Write file into zip under its hierarchy
                    zf.write(filename, arcname=os.path.relpath(filename, temp_dir_dst.parent))

            # Go back to start dir
            os.chdir(cwd)

            # Remove temp dir
            shutil.rmtree(temp_dir)
        else:  # Addon is a file, zip only the file
            # Clean file
            #y = addon_path.as_posix()
            y = addon_basename
            #print(y)
            if filename.endswith('.py'):
                clean_file(y)

            # Write single addon file into zip
            zf.write(y)

        # End zip building
        zf.close()
    else:  # Addon is already zipped, take it as it is
        zfile = addon_path
        print(f"Detected zip path is - {zfile}. No need to zip the addon beforehand.")

        # Get bpy python module from zip file name
        bpy_module = addon_basename.split(".zip")[0]

    # Copy zipped addon with name extended by blender revision number
    bl_revision = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
    bfile = f"{zfile.stem}_{bl_revision}.zip"
    shutil.copy(zfile, bfile)

    return bpy_module, bfile


def change_addon_dir(bpy_module: str, addon_dir: str):
    """Change Blender default addons (a.k.a user scripts) directory to the given one.
    :param bpy_module: Addon name used as bpy module name
    :param addon_dir: Directory used by Blender to get addons (user scripts)
    """
    # Ensure paths
    addon_dir_abs = Path(addon_dir).resolve()

    # Create addon target dir if doesn't exist
    if not addon_dir_abs.is_dir():
        addon_dir_abs.mkdir(parents=True)

    print(f"Change addon dir - {addon_dir_abs}")

    # 3.6 introduced multiple addon directories
    if bpy.app.version < (3,6):
        bpy.context.preferences.filepaths.script_directory = addon_dir_abs.as_posix()
    else:
        directory = addon_dir_abs.as_posix()
        script_directories = bpy.context.preferences.filepaths.script_directories

        new_dir = script_directories.new()
        # Assign path selected via file browser.
        new_dir.directory = directory
        new_dir.name = addon_dir

    bpy.utils.refresh_script_paths()


def install_addon(bpy_module: str, zfile: str, addon_dir: str):
    """Install addon to the version of blender
    :param bpy_module: Addon name used as bpy module name
    :param zfile: Zipped addon to import
    """
    # Ensure paths
    zfile = Path(zfile).resolve()

    # 3.6 introduced multiple addon directories
    if bpy.app.version < (3,6):
        bpy.ops.preferences.addon_install(overwrite=True, target='PREFS', filepath=zfile.as_posix())
    else:
        bpy.ops.preferences.addon_install(overwrite=True, target=addon_dir, filepath=zfile.as_posix())

    bpy.ops.preferences.addon_enable(module=bpy_module)


def cleanup(addon, bpy_module, addon_dir):
    print(f"Cleaning up - {bpy_module}")
    bpy.ops.preferences.addon_disable(module=bpy_module)
    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)


def get_version(bpy_module):
    mod = sys.modules[bpy_module]
    return mod.bl_info.get("version", (-1, -1, -1))


def get_bl_version():
    return bpy.app.version
