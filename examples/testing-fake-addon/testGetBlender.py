import sys

try:
    from blender_addon_tester import get_blender
except Exception as e:
    print(e)
    sys.exit(1)

platform_list = [
    "win64",
    "linux",
    "darwin",
]
version_list = [
    "3.3",
    "3.2",
    "3.1",
    "3.0",
    "2.93",
    "2.92",
    "2.91",
    "2.90",
    "2.83",
    "2.82",
    "2.81",
    "2.80",
]

# platform = "linux"
#
# blender_version = "2.81"
# blender_zippath, nightly = get_blender.getSuffix(blender_version, platform)
# print(blender_zippath)

for platform in platform_list:
    for version in version_list:
        blender_zippath, nightly = get_blender.getSuffix(version, platform)
        print(blender_zippath)
