GIT_TAG?=0.10.0
VERSION_FILE?=`find . -name version.py`
release:
	echo "Release v${GIT_TAG}"
# 	@grep -Po '\d\.\d\.\d' cocotbext/jtag/version.py
	git tag v${GIT_TAG} || { echo "make release GIT_TAG=${GIT_TAG}"; git tag ; exit 1; }
	echo "__version__ = \"${GIT_TAG}\"" > ${VERSION_FILE}
	git add ${VERSION_FILE}
	git commit --allow-empty -m "Update to version ${GIT_TAG}"
	git tag -f v${GIT_TAG}
	git push && git push --tags

# default:
# 	@make dist
# 	#rm -rf build/ dist/ *.egg-info
# 	pip install -r requirements.txt
# 	pip uninstall blender_addon_tester -y
# 	pip install dist/*.whl
# 
# dist:
# 	rm -rf build/ dist/ *.egg-info
# 	python setup.py clean --all
# 	python setup.py bdist_wheel
# 
# 
# twine:        
# 	twine upload \
#     	    --verbose \
#     	    --repository-url https://upload.pypi.org/legacy/ dist/* \
#    	    -u __token__ \
#     	    -p $(PYPY_API)

# all:
# 	# Set a BLENDER_CACHE if not set yet
# 	#export BLENDER_CACHE=${BLENDER_CACHE:-"~/.blender_cache"}
# 	# Set a BLENDER_VERSION if not set yet
# 	#export BLENDER_VERSION=${BLENDER_VERSION:-"2.80"}
# 	rm -rf build/ dist/ *.egg-info
# 	pip install -r requirements.txt
# 	pip uninstall blender_addon_tester -y
# 	python setup.py bdist_wheel
# 	pip install dist/*.whl
# # 	cd examples/testing-*/
# # 	pwd
# # 	for testable_file in $(ls test_addon*.py); do
# #   		python "$testable_file" $BLENDER_VERSION fake_addon;
# # 	done
# # 	cd ../..
