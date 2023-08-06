darfix
=========

Darfix is a Python library to provide the id06 at the ESRF a series of computer vision techniques, together with a graphical user interface and an Orange3(https://github.com/biolab/orange3) add-on to define the workflow.

Installation
------------

To install the last release run

.. code-block:: bash

    pip install darfix

To install from sources:

.. code-block:: bash

    git clone https://gitlab.esrf.fr/julia.garriga/darfix.git
    cd darfix
    pip install -r requirements.txt
    pip install .

To test the orange workflow (only from sources) just run

.. code-block:: bash

    orange-canvas orangecontrib/tutorials/example_tutorial.ows