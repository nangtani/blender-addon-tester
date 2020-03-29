# Set a BLENDER_CACHE if not set yet
export BLENDER_CACHE=${BLENDER_CACHE:-"~/.blender_cache"}
rm -rf build/ dist/ *.egg-info
pip install -r requirements.txt
pip uninstall blender_addon_tester -y
python setup.py bdist_wheel
pip install dist/*.whl
