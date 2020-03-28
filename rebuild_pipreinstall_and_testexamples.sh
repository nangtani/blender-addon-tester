# Set a BLENDER_CACHE if not set yet
export BLENDER_CACHE=${BLENDER_CACHE:-"~/.blender_cache"}
# Set a BLENDER_VERSION if not set yet
export BLENDER_VERSION=${BLENDER_VERSION:-"2.80"}
rm -rf build/ dist/ *.egg-info
pip install -r requirements.txt
pip uninstall blender_addon_tester -y
python setup.py bdist_wheel
pip install dist/*.whl
cd examples/testing-*/
pwd
for testable_file in $(ls test_addon*.py); do
  python "$testable_file" $BLENDER_VERSION fake_addon;
done
cd ../..
