# prettyrepo

This is a cookie-cutter project for the way I like to set up a Python repo.


Components:
- MIT `LICENSE.md` file and `CHANGELOG.md` changelog template
- pipenv for dependency management (`Pipfile` and `Pipfile.lock`)
- `setup.py`, `setup.cfg`,` MANFIEST.in` for packaging
- flake8 linting
  - Configured in a `.flake8` file
  - Extension flake8-quotes to favor single-quoted strings
  - Extension flake8-import-order to force import order
- pytest unit tests
  - `.gitignore` set up to include `runConfigurations` to share PyCharm IDE config
  - `pytest.ini` to configure xunit XML output
  - `pytest-flake8` to run flake8 as part of the unit testing and get JUnit XML output
  - Coverage reporting with the help of pytest-cov, configured in a `.coveragerc`
- `.rst` `README` and docs directory for sphinx documentation
- `semver.txt` to drive the version
- `tox` to test installation of the package on multiple python versions
  - Also including a `Dockerfile` to run tox in a dockerized environment rather than manage multiple installations in the test environment
- `.gitlab-ci.yml` for CI using the GitLab runner
  - Runs `pytest --flake8` with some config to get xunit xml output which it uploads so it can be viewed in the pipeline report
  - Runs actual unit tests using the same Docker image and uploads tests
  - In GitLab you can go to Settings &rarr; CI/CD &rarr; General Pipelines and set the coverage regex to `^TOTAL.+?(\d+.\d+\%)$`
  
  
Maybe one day part of this repo will be to help automate actually setting things up.


## Notes
- readthedocs doesn't support reading requirements from pipenv, so you'll have to run something like `pipenv run pip freeze > docs/requirements.txt`
- 

<<<<<<< HEAD
[![pipeline status](https://gitlab.com/tkutcher/prettyrepo/badges/dev/pipeline.svg)](https://gitlab.com/tkutcher/prettyrepo/-/commits/dev)
[![PyPI version](https://badge.fury.io/py/prettyrepo.svg)](https://badge.fury.io/py/prettyrepo)
[![coverage report](https://gitlab.com/tkutcher/prettyrepo/badges/dev/coverage.svg)](https://gitlab.com/tkutcher/prettyrepo/-/commits/dev)
<<<<<<< HEAD
[![docs](https://img.shields.io/static/v1?label=docs&message=wiki&color=purple)](https://gitlab.com/tkutcher/prettyrepo/-/wikis/home)
=======
>>>>>>> c814c69... Add badges


## Overview
All of the functionality as [invoke](http://docs.pyinvoke.org/en/stable/) with a smidge more flexibility (maybe just for me?) than something like [invocations](https://github.com/pyinvoke/invocations). 

In general, this project (as well as invoke), give an OS-agnostic solution for automating common commands during development (cleaning build files, running unit tests, etc.). Similar to how a Makefile might be used, prettyrepo makes it so that with a small set of commands you can run any typical task. Furthermore, you can have configurable arguments for each of those tasks being run (see [example](#example)).  

This project introduces a `TaskManager` so every available task can be tweaked as desired and persistent for a project. Reference [tasks.py](tasks.py) for this project's own tasks file.


### Example

```python

from invoke import task

from prettyrepo import TaskManager
from prettyrepo.utils import run_unittest
from prettyrepo.utils import get_python_cleans

# Create a TaskManager that knows the root of your project
mgr = TaskManager(source_root='prettyrepo', tasks_module=__name__)

# Add tasks from the "task library" or a simple command (by specifying the cmd kwarg)
mgr.add_task('clean', cleans=get_python_cleans())
mgr.add_task('test', lib='unittest', dir_='tests')
mgr.add_task('cov', aliases=['cover'], lib='coverage', func=run_unittest, dir_='tests')
mgr.add_task('lint', aliases=['flake8'], cmd='flake8 prettyrepo', doc='Run flake8 lints.')

# You can use the normal invoke task decorator in conjunction with prettyrepo tasks.
@task(name='bleh', help={'times': 'number of times to say blah'})
def blah(_, times=1):
    """Say blah."""
    print('\n'.join(['blah']*times))


ns = mgr.namespace
```

With this in your `tasks.py` file in the root of your repository, you can run 

`inv <command> [-h] [<command options...>]`

Where `-h` is available to show the help message. For example, running `inv clean -h` yields:

```
Docstring:
  Clean unnecessary files.

Options:
  -l INT, --level=INT       the level of "cleanliness" [0-2], default 1
  -v INT, --verbosity=INT   how verbose information to log to the console [0-3], default 1
```

Where `-l` and `-v` can be used to specify what the clean task does (the higher the level, the more files it removes - i.e. venv, dist files; the higher the verbosity, the more info it logs):


<img src="https://gitlab.com/tkutcher/prettyrepo/-/raw/dev/gfx/clean-demo.gif" alt="command line screenshot" height="400px">

 
 Documentation available in the [repository wiki](https://gitlab.com/tkutcher/prettyrepo/-/wikis/home/documentation/setup).
=======
>>>>>>> c77323a... add cookie cutter files
