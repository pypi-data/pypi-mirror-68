
MMSICHE
======

A python class which implements MMSICHE algorithm on image.
MMSICHE: Median-Mean based Sub-Image-Clipping Histogram Equalization.

The code is Python 2, but Python 3 compatible.

Installation
------------

Fast install:

::

    pip install MMSICHE

For a manual install get this package:

::

    wget https://github.com/abhinavbajpai2012/MMSICHE
    unzip master.zip
    rm master.zip
    cd MMSICHE-master

Install the package:

::

    python setup.py install    

Example
--------

.. code:: python

    from MMSICHE import MMSICHE

    # get formatted address of any location
	img = cv2.imread('temp.png', 0)
    obj = MMSICHE(img)
    
    