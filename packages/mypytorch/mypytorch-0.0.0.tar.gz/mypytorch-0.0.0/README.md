# py-template

Template for a Python project with testing, documentation, publishing to pypi and continuous integration with github actions. Start your own project from this template clicking [here](https://github.com/juansensio/py-template/generate).

## Instructions

Once your new repository is created and cloned, you can start with the following command

```
python tools/start.py <your-project-name-here>
```

This will create the necessary files and folders to start working.

### Testing

Place your tests int the `tests` folders. Here, we use [unittest](https://docs.python.org/3/library/unittest.html). You can run the tests with

```
make test
```

Your tests should be named with the termiantion `_test.py` to be recognized as tests. You can have tests in subfolders, but you will need an `__init__.py` file for this to work. Tests run automattically when you push to master using Github actions.

### Documentation

The documentation is generated automatically, looking for all the files inside your library folder and generating documentation from docstrings using [sphinx](http://www.sphinx-doc.org/en/master/). You can generate the documentation with

```
make docum
```

A `docs` folder will be generated with your documentation ready to be deployed in Github Pages, for example.

### Deploying to PyPi

To publish your module to pypi, you can run

```
make pypi
```

Make sure to set the correct name of your project, version, and all the required information in the `setup.py` file.