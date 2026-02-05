# 1 Start a Python project from scratch on Ubuntu using uv + git


## Prerequisites on Ubuntu
```bash
# System tooling
sudo apt update
sudo apt install -y git curl build-essential


# (Optional but common) if you expect packages with native extensions
sudo apt install -y python3-dev
```


## install uv


`uv` is distributed as a standalone binary and is commonly installed via the official installer ([docs.astral.sh](https://docs.astral.sh/uv/?utm_source=chatgpt.com))


```bash
curl -LsSf https://astral.sh/uv/install.sh | sh


# ensure your shell can find uv
uv --version
uv 0.9.28 (0e1351e40 2026-01-29)
```


## create a new project (a package that you build on)

### uv init
Use `uv init` to scaffold a project. uv can also create a "bare" project (only pyproject.toml), but for learning it is helpful to generate the typical structure.


```bash
mkdir demo-pyproject-with-uv # or other project as you wish
cd demo-pyproject-with-uv # change to the project directory


# create project scaffold
uv init
```


* **Scaffolding**: in the world of software development, scaffolding is the process of automarically generating a standardized starting structure for a project. In uv, the scaffolding of a python project typically includes:
    - .gitignore
    - .python-version
    - README.md
    - main.py
    - pyproject.toml


The main.py file created by uv contains a simple "Hello world" program. Try it out with uv run:
```bash
uv run main.py
Hello from demo-pyproject-with-uv!
```


A project consists of a few important parts that work tegether and allow `uv` to manage the project. In addition to the files created by `uv init` listed above, `uv` will create a virtual environment and a `uv.lock` file in the root of the project the first time running a **project command**, e.g., `uv run`, `uv sync`, or `uv lock`.


> uv sync: is the *"make my local environment match the project definition"* command; it keeps dependencies reproducible across machines.


> Note: ```uv lock``` only adds a *uv.lock* file, but it **does not** create the virtual environment.


After running the uv run main.py command, the project structure now looks like as follows:


```bash
.
├── .venv
│   ├── bin
│   ├── lib
│   └── pyvenv.cfg
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```



* pyproject.toml file


    The pyproject.toml file contains meatadata about the python project:


    ```bash
    [project]
    name = "demo-pyproject-with-uv"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []
    ```


* `.python-version`


    The `.python-version` file contains the project's default Python version. THis file tells uv which Python version to use when creating the project's virtual environment.


* `.venv`


    The .venv folder contains the project's virtual environment, a Python environment that is isolated from the rest of your system. This is where uv will install your project's dependencies.


* `uv.lock`


    `uv.lock` is a cross-platform lockfile that contians exact information about your project's dependencies. Unlike the `pyproject.toml` file which is used to specify the broad requirements of your project, the lockfile contains the exact resolved versions that are installed in the project environment. THis file should be checked into version control, allowing for consistent and reproducible installations across machiens.


    > Note: `uv.lock` is a human-readable TOML file but is managed by uv and **should not** be edited manually.

### uv init --lib
```bash
uv init --lib
```
uv init --lib creates a packaged library using a src/ layout and includes a build system by default. The project layout is given as follows:

```bash
uv-demo-lib/
├─ .python-version
├─ README.md
├─ pyproject.toml
└─ src/
   └─ uv_demo_lib/
      ├─ __init__.py
      └─ py.typed
```

uv can add dependencies directly into pyproject.toml using uv add, and --dev places them into dev/dependency groups.

```bash
uv add --dev pytest pytest-cov ruff
```

Create the venv + lockfile (happens automatically on first project command):
```bash
uv run python -V
```
uv will create .venv/ and uv.lock when you first run/sync/lock a project.

### Mananging Dependencies

* **add** dependencies
    * using `uv add`:
    ```bash
        uv add requests numpy pandas
    ```
    * you can also specify version constraints or alternative sources:
    ```bash
    # specify version constraint
    uv add 'requests==2.31.0'


    # add a git dependency
    uv add git+https://github.com/psf/requests
    ```
    * migrating from a requirements.txt file:
    ```bash
    # add all dependencies from a requirements.txt file
    uv add -r requirements.txt -c contraints.txt
    ```
* **remove** dependencies using `uv remove`:
    ```bash
    uv remove requests
    ```
* **upgrade** a package using uv lock with the --upgrade-package flag:
    ```bash
    uv lock --upgrade-package requests
    ```


### Viewing project version
The uv version command can be used to read package's version


```bash
# to get the version of package
uv version
demo-pyproject-with-uv 0.1.0


# to get the version without package name
uv version --short
0.1.0


# to get a version information in JSON format
uv version --output-format json
{
    "package_name": "hello-world",
    "version": "0.1.0",
    "commit_info": null
}
```


## Initialize git and make the first commit


```bash
git init
git add .
git commit -m "initial scaffold: uv project"
```


## Add dependencies and create the local environment
### Add runtime dependencies
```bash
uv add requests flask
```


### Add dev dependencies (tests, linting, formatting):
```bash
uv add --dev pytest ruff
```


### Create/Sync the environment from pyproject.toml and uv.lock
```bash
uv sync
```


# 2. Local Workflow: Planning -> Developing -> Testing -> Building


## 2.1 Planning
A lightweight, practical approach:
1. Define the deliverable (e.g., "a CLI that fetches a URL and prints status code")
2. List acceptance criteria (inputs/outputs, error handling)
3. Sketch modules (e.g., client.py, cli.py) and tests (test_client.py)
Keep this in a `docs/` note or a short GitHub issue - what matters is clarity.


## 2.2 Developing
Create a package (example name: `demo_uv`) under `src/`:


```bash
mkdir -p src/demo_uv
touch src/demo_uv/__init__.py
```
> Note: the -p (or --parents) option tells mkdir to create any missing parent directories in the path and not to error if the target directory already exists. In this case, `mkdir -p src/demo_uv` will create src if needed, then demo_uv, and return success even if they already exist.


Add a simple function to `src/demo_uv/client.py`:
```python
import requests


def fetch_status(url: str) -> int:
    r = request.get(url, timeout=10)
    r.raise_for_status()
    return r.status_code
```


## 2.3 Testing locally with pytest
* Create a dir for `./tests`
    ```bash
    mkdir -p tests
    ```


* Create a test for client.py -> `tests/test_client.py`:
    ```python
    import pytest
    from demo_uv.client import fetch_status


    def test_fetch_status_ok():
        # A stable endpoint is ideal in real tests;
        # for tutorial purposes, keep it simple.
        assert fetch_status("https://example.com") == 200
    ```


* Run tests without manually activating the venv (**recommended for repeatability**):


    ```bash
    uv run pytest -q
    ```
   
    Alternatively, activate venv through `srouce .venv/bin/activate` and then run `pytest`, but `uv run ...` avoids shell differences.


## 2.4 Linting/ formatting


    ```bash
    uv run ruff check .
    uv run ruff format .
    ```


### Ruff vs. flake8
In the world of Python development, **Ruff** has largely emerged as the modern successor to Flake8. While both tools serve the same core purpose, i.e., catching errors and enforcing style. They differ significantly in their architecture and feature sets.


The fundamental difference is that Flake8 is a Python-based wrapper for several older tools (Pyflakes, pycodestyle, and McCable), whereas Ruff is a single, unified engine written in Rust.


1. Performace
Ruff is typically 10-100x faster than Flake8. In massive codebases where Flake8 might take 10-20 secondes to run, Ruff usually finishes in under 200ms. This speed makes Ruff viable as a "live" linter that shows errors as you type.


2. Built-in vs. Plugins
    * Flake8 is minimalist by design. If you want to check for security issues (bandit), import order (isort), or modern Python syntax (pyupgrade), you have to install separate packages and manage their dependencies.
    * Ruff re-implements the functionality of dozens of these plugins natively. By simply toggling a rule code in the config, you get the power of isort, flake8-bugbear, flake8-simplify, and more, without extra installs.


3. Auto-fixing and Formatting
    * Flake8 is "read-only" - it tells you what is wrong but won't touch your code.
    * Ruff can automatically fix many common issues (like removing unused imports or upgrading old syntax) using the --fix flag. Additionally, Ruff includes a formatter that is a drop-in replacement for Black, allowing you to replace your entire linting and formatting stack with one tool.


4. Configuration
    * Ruff follows the modern Python standard by using the `[tool.ruff]` section in pyproject.toml.
    * Flake8 does not natively support pyproject.toml without third-party plugins (like pyproject-flake8), typically requiring its own dedicated config file.


#### When to use Which
* Use Ruff if: You are staring a new project or want to modernize your current workflow. It is faster, easier to configure, and reduces the number of dependencies in your environment.


* Use Flake8 if: You have a legacy project with highly sepecific custom Flake8 plugins that have not yet been ported to Ruff, or if your team prefers the absolute stability of a tool that hasn't changed its core logic in years.


## 2.5 Building the project locally
**"Build"** in Python usually means producing distributable artifacts (a source distribution and a wheel) from your project metadata. With uv, this is done with `uv build`.


```bash
uv build
ls -la dist/
```
You should see artifacts in dist/ (e.g., `.whl` and `.tar.gz`)
* `uv_demo_lib-0.1.0-py3-none-any.whl`
* `uv_demo_lib-0.1.0.tar.gz`



#  Publishing Package

## to [Test PyPI](https://packaging.python.org/en/latest/guides/using-testpypi/) (Recommended first)
 Add a TestPyPI index definition in pyproject.toml by appending the following table:

```toml
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
explicit = true
```

uv's docs recommend configuring a custom index with `pushlish-url` and then using `uv publish --index <name>`. ([ref.](https://docs.astral.sh/uv/guides/package/?utm_source=chatgpt.com))

Now publish (token required):

```bash
uv publish --index testpypi --token <YOUR_TESTPYPI_TOKEN>
```

## To PyPI

```bash
uv publish --token <YOUR_PYPI_TOKEN>
```

# CI/CD with GitHub Actions (CI on PRs, CD on tags)
## CI Workflow: Triggered on PR, push

## CD Workflow: Publish on version tags

## [Configure Trusted Publishing on PyPI (one-time)](https://docs.pypi.org/trusted-publishers/using-a-publisher/?utm_source=chatgpt.com)
On PyPI, add a Trusted Publisher for your project that points to:
* Your GitHub org/user
* Repo: uv-demo-lib
* Workflow file: release.yml
* Environment (if you use one)

## Create a release tag (triggers CD)
When you are ready to publish version 0.1.0:

```bash
git add .
git commit -m "Initial dummy library with CI/CD"
git push origin main

git tag v0.1.0
git push origin v0.1.0
```

