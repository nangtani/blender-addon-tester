import pytest
from addon_helper import get_version, get_bl_version


@pytest.fixture
def bpy_module(cache):
    return cache.get("bpy_module", None)


def test_versionID_pass(bpy_module):
    print(get_bl_version)
    if (2, 90, 0) == get_bl_version:
        expect_version = (3, 3, 0)
    else:
        expect_version = (3, 3, 0)
    return_version = get_version(bpy_module)
    assert expect_version == return_version


def test_versionID_fail(bpy_module):
    expect_version = (0, 1, 1)
    return_version = get_version(bpy_module)
    assert not expect_version == return_version
