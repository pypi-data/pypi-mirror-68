=============
Cryoef plugin
=============

This plugin provide a wrapper around `cryoEF <https://www.mrc-lmb.cam.ac.uk/crusso/cryoEF/>`_ program.

+------------------+------------------+
| stable: |stable| | devel: | |devel| |
+------------------+------------------+

.. |stable| image:: http://scipion-test.cnb.csic.es:9980/badges/cryoef_prod.svg
.. |devel| image:: http://scipion-test.cnb.csic.es:9980/badges/cryoef_sdevel.svg


Installation
------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-cryoef

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-cryoef.git

    * install

    .. code-block::

        scipion installp -p path_to_scipion-em-cryoef --devel

CryoEF binaries will be installed automatically with the plugin, but you can also link an existing installation. 
Default installation path assumed is ``software/em/cryoEF-1.1.0``, if you want to change it, set *CRYOEF_HOME* in `scipion.conf`` file to the folder where the cryoEF is installed. To check the installation, simply run the following Scipion test:

``scipion test cryoef.tests.test_protocols_cryoef.TestCryoEF``

Supported versions
------------------

1.1.0

Protocols
---------

    * orientation analysis

Detailed manual can be found in ``software/em/cryoEF-1.1.0/cryoEF_v1.1.0_manual.pdf``

References
----------

    * `1.  Naydenova, K and Russo, CJ "Measuring the effects of particle orientation to improve the efficiency of electron cryomicroscopy" Nature Communications (2017). <https://www.nature.com/articles/s41467-017-00782-3>`_
