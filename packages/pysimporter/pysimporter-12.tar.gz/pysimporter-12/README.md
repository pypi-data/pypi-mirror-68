### PyPi CI/DI github project

## Code Structure
```
YourProjectDir
    -file1.py
    -file2.py
    -__init__.py (mandatory to importing module)
__init__.py
README.md
setup.py
```
#### Just add your folder to this project and it instantly will push to pypi

# Few important things
### change version in setup.py every change you make. If you have not changed the version, your updates dont will not be pushed to pypi
### Add requirements to setup.py too, append it in "install_requires" variable
### I don't know why, but 3.3 version < 3.19, keep it in mind
