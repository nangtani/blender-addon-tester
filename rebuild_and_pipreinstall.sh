rm -rf build/ dist/ *.egg-info
python3 setup.py bdist_wheel
pip install dist/*.whl
