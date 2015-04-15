============
Medic Mobile's pyxform v0.9
============

This version of pyxform makes writing XForms for Medic Collect simpler by bringing SMS settings from the Settings worksheet to the XForms. The SMS settings currently used are `sms_keyword` and `sms_separator`. If they are omitted defaults appropriate for the medic-webapp parser are used.

This tool is entirely based on pyxform, a Python library that converts XLS(X) spreadsheets into XForms for ODK Collect and enketo. 

A new user of pyxform should
look at the documentation `here <https://formhub.org/syntax/>`_ or
`here <http://opendatakit.org/help/form-design/xlsform/>`_.

Running pyxform as a Python script:
===========================

1. install xlrd.

    #On ubuntu these terminal commands should do it:

    easy_install pip

    pip install xlrd

2. Run this command:

    python pyxform/xls2xform.py path_to_XLSForm output_path

Installation
============
Installing pyxform from github is easy with pip::

	pip install -e git+https://github.com/medic/pyxform.git@master#egg=pyxform

Testing
=======
To make sure the install worked out, you can do the following::

	pip install nose==1.0.0

	cd your-virtual-env-dir/src/pyxform

	nosetests

Documentation
=============
To check out the documentation for pyxform do the following::

	pip install Sphinx==1.0.7

	cd your-virtual-env-dir/src/pyxform/docs

	make html

Upstream Change Log
=========
https://github.com/UW-ICTD/pyxform/blob/master/CHANGES.txt
