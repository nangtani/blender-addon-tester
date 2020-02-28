rm -rf build/ dist/ *.egg-info
pip3 install -r requirements.txt
pip uninstall blender_addon_tester -y
python3 setup.py bdist_wheel
pip install dist/*.whl
