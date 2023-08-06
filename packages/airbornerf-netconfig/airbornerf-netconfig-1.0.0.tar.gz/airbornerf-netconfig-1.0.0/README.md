This package contains sqlalchemy model files for the general "network config" 
database. This database is a SQLite file that carriers can use to send us
network config data. The cell importer has dedicated support for that kind
of DB files.

When the pipeline successfully ran, release the package to PyPI:

```
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Check the project page: https://pypi.org/project/airbornerf-netconfig/
