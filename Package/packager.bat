cd "V0.0.0-beta"

py setup.py sdist bdist_wheel
twine upload dist/*