![Github Actions pypi.org nightly tests](https://github.com/nangtani/blender-addon-tester/workflows/test-fake-addon-example-from-github-pip-nightly/badge.svg)
![Github Actions local Python wheel tests](https://github.com/nangtani/blender-addon-tester/workflows/test-fake-addon-example-from-local-wheel/badge.svg)
[![codecov](https://codecov.io/gh/nangtani/blender-addon-tester/branch/master/graph/badge.svg)](https://codecov.io/gh/nangtani/blender-addon-tester)

# blender-addon-tester

## Background

[Blender](https://blender.org) can be extended with python addons. 

When an addonsreleased, it's developped to work with the current version of Blender.  
But over time as Blender releases new versions, the Blender API changes, leading to the addon to eventually breaking and stop working.

Currently there's no native testing environment that:  
* Allows an addon to be tested against multiple versions of blender and multiple OSs (ubuntu, windows and macosx)
* Used an industry standard of testing, i.e. `pytest`
* Plugs into a continuous integration tool, i.e. Github Actions, Travis CI
* Ability to test a passing addon against the nightly builds, to catch API breaks as close to when they happen
* Code coverage of the addon. Used to assess comprehensivness of the tests.

## What does blender-addon-tester do

This python module allows command line `pytest`ing to be performed on different versions of blender. It will:
- download and maintain different versions of blender locally.    
- install the addon under test into a location accessible by the respective version of blender.   
- execute a series of tests, by default, located in the `tests` directory. These tests are written in the `pytest` format.  

Once the addon has been completed and the tests have been written, they are checked in to github.   
They can be run against a continous integration tool.   
There's currently support for both Github Actions and Travis CI.    

## Usage

It can be confusing with blender as it has an internal version of python that is different from the system python.   
`blender-addon-tester` is install to the system python and is used to call different versions of blender.   
It is inside this instance of blender that the addon under test gets installed.

`blender-addon-tester` can be install from pypi:  
```batch
pip install blender-addon-tester
```

Then it can be called from any script:  
```
    import blender_addon_tester as BAT
    BAT.test_blender_addon(addon_path=addon, blender_revision=blender_rev)
```

Once called, it will  
* Check to see if the version of blender is presnet in the cache location, if not it will download that version of blender and install it to the cache location, installing all the extra python modules required to enable pytest-ing and coverage.
* It will install the addon to the version of blender
* It will run all the tests, default `tests` directory, but this can be explictly set. \it will report a pass or failure.  This result is written to be capturable by CI tools.
* It will also report to coverage of the test.  This coverage can be almalgamated across all versions to get a full idea of testing.

Online continuous integration and code coverage need to be setup explictly. 

## pytest

Example output of a successful `pytest`.

```
============================= test session starts =============================
platform win32 -- Python 3.7.4, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- C:\blender\blender-2.93\blender.exe
cachedir: .pytest_cache
rootdir: C:\blender\blender-fake-addon
plugins: cov-2.8.1
collected 2 items

tests/test_version.py::test_versionID_pass PASSED                         [ 50%]
tests/test_version.py::test_versionID_fail PASSED                         [100%]

========================== 2 passed in 0.20 seconds ===========================
```

Example of a failing `pytest`.

```
_____________________________ test_versionID_pass ______________________________
bpy_module = 'fake_addon'
    def test_versionID_pass(bpy_module):
        expect_version = (1, 0, 1)
        return_version = get_version(bpy_module)
>       assert  expect_version == return_version
E       assert (1, 0, 1) == (0, 0, 1)
E         At index 0 diff: 1 != 0
E         Use -v to get the full diff
tests/test_pytest.py:11: AssertionError
====================== 1 failed, 1 passed in 0.08 seconds ======================
```

## Operational

To see a working addon environment checkout this repo.  In the sub directory `examples\testing-fake-addon`, it contains a dummy addon that that can be sued to verify that the whole enviroment is setup correctly.
```
cd examples\testing-fake-addon
test_addon_blender.py fake_addon 3.2
```
However it is better to use this modile with an addon in a different repo.  Check out this repo for that example, [fake_addon](https://github.com/nangtani/blender-fake-addon)

## Projects using `blender-addon-tester`
- [fake_addon](https://github.com/nangtani/blender-fake-addon)
- [blender-import-lwo](https://github.com/nangtani/blender-import-lwo)
- [ba_io_scene_obj](https://github.com/nangtani/ba_io_scene_obj)
- [gmic-blender](https://github.com/myselfhimself/gmic-blender)

## Releases
### v0.10
- Add support for 3.4
- Add support for 3.5
- Bumped all the guthub actions revs
- Added support for github actions release

### v0.9
- Add support for 3.1
- Add support for 3.2
- Add support for 3.3
- Move to python3.10 on CI

### v0.8
- Needed to updated how the blender packages got fetch from the server (again)
- Fixed the non-default addon directory option, #26
- Break out the addon directory setup from the addon install
- Deprecated 2.79, which removes any dependency on python3.5
- Deprecated 2.80

### v0.7
- Re-do how the most recent version of Blender is fetched as the format used on the server has changed.
- Deprecated 2.78.

### v0.6
- Added PYTEST_ARGS on the config option
- Need a separate PYTHONPATH for the scripts directory that the addon uses for helper scripts:  
`addon_helper = os.environ.get("ADDON_TEST_HELPER", None)`

### v0.5
- Fix Blender rev edit bug

### v0.4
- Introduce per Blender rev addons support

### v0.3
- New release required due to repo migration

### v0.2
- Added default cache location if not specified
- Deleted built-in addon from reference Blender if testing a new version of the addon
- Updated setup.py to remove unnecessary modules needed for blender-addon-tester to work.
- Updated documentation

### v0.1
- Initial check-in to PyPI
- Working against GitHub Actions
- Working against Travis CI


