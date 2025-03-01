import os
from pathlib import Path
import sys

try:
    import blender_addon_tester as BAT
except Exception as e:
    print(e)
    sys.exit(1)


def main():
    here = Path(__file__).parent
    if len(sys.argv) > 1:
        addon = sys.argv[1]
    else:
        addon = here.joinpath("fake_addon").as_posix()
    if len(sys.argv) > 2:
        blender_rev = sys.argv[2]
    else:
        blender_rev = "2.80"

    config = {
        "blender_load_tests_script": here.joinpath(
            "blender_advanced_load_pytest.py"
        ).as_posix(),
        "coverage": True,
        "tests": here.joinpath("advanced_tests").as_posix(),
    }

    try:
        exit_val = BAT.test_blender_addon(
            addon_path=addon, blender_revision=blender_rev, config=config
        )
    except Exception as e:
        print(e)
        exit_val = 1
    sys.exit(exit_val)


main()
