# Welcome 

Contact : dsimonne@mit.edu

You can install the latest version of the package by cloning the repository and via the `setup.py` script (`pip install .`)

# Installing different packages yourself

* First, I advise you to create a `/Packages` directory to keep these.
* Secondly, I advise you to create a virtual environment to help with debogging, and so that once everything works, you don't update a package by mistake. To do so please follow the following steps:

## Create a virtual environment

* `mkdir rnice.dfxm`
* `cd rnice.dfxm/`
* `python3 -m venv .`
* `source bin/activate` # To activate the environment
* Make sure `wheel` and `setuptools` are installed: `pip install wheel setuptools pip --upgrade`

Then you should create an alias such as: `alias source_rnice.dfxm="source /home/user/rnice.dfxm/bin/activate"`

## 2) Install `dfxm`
* `cd /Packages`
* `git clone https://github.com/DSimonne/dfxm.git`
* `cd dfxm`
* `source_rnice.dfxm`
* `pip install .`