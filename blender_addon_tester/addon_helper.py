import os
import sys
import re
import tempfile
import time
import zipfile
import shutil
import subprocess
from pathlib import Path

def clean_file(filename):
    """ Cleans up addons files so that any blender version code is strip to be compliant with addon guidelines
    :param filename     Path to addon file
    :return None
    """
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

def zip_module(blender_exec_path, module, temp_dir, dir_to_ignore=set()):
    """ Zips 'addon' dir or '.py' file to 'addon.zip' if not yet zipped, then moves the archive to 'temp_dir'.
    :param addon     Absolute or relative path to a directory to zip or a .zip file.
    :param temp_dir Path to Blender's addon directory to move the zipped archive to.
    :return (bpy_module, zip_file) Tuple of strings - an importable module name, an addon zip file path.
    """
    already_zipped = False

    module_path = os.path.realpath(module)
    module_basename = os.path.basename(module_path)

    if module_basename.endswith(".zip"):
        already_zipped = True

    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    print("Addon dir is - {0}".format(os.path.realpath(temp_dir)))
    if not already_zipped:
        bpy_module = re.sub(".py", "", module_basename)
        zfile = os.path.realpath(bpy_module + ".zip")
        zfile = Path(tempfile.gettempdir(), f"{bpy_module}.zip")

        print("Future zip path is - {0}".format(zfile))

        print("Zipping addon - {0}".format(bpy_module))


        zf = zipfile.ZipFile(zfile, "w")
        if os.path.isdir(module):
            cwd = os.getcwd()
            temp_dir = "tmp"
            if os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)
        
            shutil.copytree(module, temp_dir + "/" + module, ignore=shutil.ignore_patterns(*dir_to_ignore))
            os.chdir(temp_dir)
            if os.path.isdir("__pycache__"):
                shutil.rmtree("__pycache__")
            for dirname, subdirs, files in os.walk(module, topdown=True):
                # Exclude unwanted directories
                subdirs[:] = [d for d in subdirs if d not in dir_to_ignore]

                # Write the directory and its contents in the archive
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    # clean_file(filename) # TODO seems to mess up with binary files
                    zf.write(filename, arcname=os.path.relpath(filename, Path(module_path).parent))
            os.chdir(cwd)
            shutil.rmtree(temp_dir)
        else:
            clean_file(module)
            zf.write(module)
        zf.close()
    else:
        zfile = module_path
        print("Detected zip path is - {0}. No need to zip the addon beforehand.".format(zfile))

        bpy_module = module_basename.split(".zip")[0]
    
    # Get blender version from command line
    output = subprocess.run([blender_exec_path, "-v"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    blender_version = re.search('Blender (.*)\n', output).group(1).split(".")

    brev = f"{blender_version[0]}.{blender_version[1]}"
    bfile = re.sub(".zip", "_{}.zip".format(brev), str(zfile))
    shutil.copy(zfile, bfile)
    return (bpy_module, bfile)


def import_module_into_blender(blender_exec_path, bpy_module, zfile, addon_dir, module_type="ADDON"):
    print("Change addon dir - {0}".format(addon_dir))

    if module_type == "ADDON":
        if (2, 80, 0) < bpy.app.version:
            # https://docs.blender.org/api/current/bpy.types.PreferencesFilePaths.html#bpy.types.PreferencesFilePaths.script_directory
            # requires restart
            python_command = f"import bpy; bpy.context.preferences.filepaths.script_directory = '{addon_dir}'; bpy.utils.refresh_script_paths(); bpy.ops.preferences.addon_install(overwrite=True, filepath='{zfile}'); bpy.ops.preferences.addon_enable(module='{bpy_module}')"
        else:
            python_command = f"import bpy; bpy.context.user_preferences.filepaths.script_directory = '{addon_dir}'; bpy.utils.refresh_script_paths(); bpy.ops.wm.addon_install(overwrite=True, filepath='{zfile}'); bpy.ops.wm.addon_enable(module='{bpy_module}')"
            
    elif module_type == "APP_TEMPLATE":
        # Install the app template into Blender
        python_command = f"import bpy; bpy.ops.preferences.app_template_install(overwrite=True, filepath='{zfile}')"
    
    # Run the installation command
    subprocess.call([blender_exec_path, "-b", '--python-expr', python_command])


def cleanup(bpy_module, addon_dir, module_type="ADDON"):
    import bpy

    print("Cleaning up - {}".format(bpy_module))
    if (2, 80, 0) < bpy.app.version:
        if module_type == "ADDON":
            bpy.ops.preferences.addon_disable(module=bpy_module)
        elif module_type == "APP_TEMPLATE":
            # TODO make it delete the app template
            print(bpy_module, addon_dir)
            pass
    else:
        if module_type == "ADDON":
            bpy.ops.wm.addon_disable(module=bpy_module)
        elif module_type == "APP_TEMPLATE":
            pass
    if os.path.isdir(addon_dir):
        shutil.rmtree(addon_dir)


def get_version(bpy_module):
    mod = sys.modules[bpy_module]
    return mod.bl_info.get("version", (-1, -1, -1))


def get_bl_version():
    return bpy.app.version
