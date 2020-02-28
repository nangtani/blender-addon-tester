rm -rf build/ dist/ *.egg-info
pip3 install -r requirements.txt
python3 setup.py bdist_wheel
pip install dist/*.whl
