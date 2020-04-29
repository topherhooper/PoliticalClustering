#!/bin/bash
set -eux
pip install -U scikit-learn
python -m pip show scikit-learn # to see which version and where scikit-learn is installed
python -m pip freeze # to see all packages installed in the active virtualenv
python -c "import sklearn; sklearn.show_versions()"

pip install -r /bash_lib/requirements.txt
