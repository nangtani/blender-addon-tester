ADDON = "fake_addon"

import os
import sys

try:
    import pytest
except Exception as e:
    print(e)
    sys.exit(1)

try:
    sys.path.append(os.environ["LOCAL_PYTHONPATH"])
    from addon_helper import zip_module, import_module_into_blender, cleanup
except Exception as e:
    print(e)
    sys.exit(1)


class SetupPlugin:
    def __init__(self, addon):
        self.addon = addon
        self.addon_dir = "local_addon"

    def pytest_configure(self, config):
        (self.bpy_module, self.zfile) = zip_module(self.addon, self.addon_dir)
        import_module_into_blender(self.bpy_module, self.zfile, self.addon_dir)
        config.cache.set("bpy_module", self.bpy_module)

    def pytest_unconfigure(self):
#         cmd = "coverage xml"
#         os.system(cmd)
        cleanup(self.addon, self.bpy_module, self.addon_dir)
        print("*** test run reporting finished")


try:
    exit_val = pytest.main(["tests", "-v", "-x", "--cov", "--cov-report", "term-missing", "--cov-report", "xml",], plugins=[SetupPlugin(ADDON)])
except Exception as e:
    print(e)
    exit_val = 1
sys.exit(exit_val)
