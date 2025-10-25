Installation
============

Requirements
------------

opensection requires:

* Python 3.8 or higher
* NumPy >= 1.20.0
* Matplotlib >= 3.3.0

Installation from PyPI
----------------------

The easiest way to install opensection is using pip::

    pip install opensection

Installation from Source
-------------------------

To install from source::

    git clone https://github.com/opensection/opensection.git
    cd opensection
    pip install -e .

Development Installation
------------------------

For development, install with development dependencies::

    pip install -e ".[dev]"

This includes:

* pytest and pytest-cov for testing
* black and isort for code formatting
* flake8 and mypy for linting
* sphinx for documentation

Verify Installation
-------------------

Check that opensection is correctly installed::

    python -c "import opensection; print(opensection.__version__)"

This should print the version number, e.g., ``0.1.0``.

Upgrading
---------

To upgrade to the latest version::

    pip install --upgrade opensection

Dependencies
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

* **numpy**: Numerical computations and array operations
* **matplotlib**: Visualization and plotting

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

* **sphinx**: Build documentation (dev)
* **pytest**: Run tests (dev)
* **black**: Code formatting (dev)

Troubleshooting
---------------

Import Error
~~~~~~~~~~~~

If you get an import error, make sure opensection is installed::

    pip list | grep opensection

Version Conflicts
~~~~~~~~~~~~~~~~~

If you have version conflicts with dependencies::

    pip install --upgrade numpy matplotlib

Virtual Environment
~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install opensection

