============
Medic Mobile's pyxform v0.9
============

This version of pyxform makes writing XForms for Medic Collect simpler by bringing SMS settings from the Settings worksheet to the XForms. The SMS settings currently used are ``sms_keyword`` and ``sms_separator``. If they are omitted, defaults appropriate for the Medic Mobile parser are used.

Documentation on XForms for Medic Collect can be found `here <https://github.com/medic/medic-docs/blob/master/md/config/create-xforms-for-medic-collect.md>`_, 
while more general info on XForms can be found `here <https://formhub.org/syntax/>`_ and
`here <http://opendatakit.org/help/form-design/xlsform/>`_.

This tool is entirely based on pyxform, a Python library that converts XLS(X) spreadsheets into XForms for ODK Collect and enketo. 

Running pyxform as a Python script:
===========================

1. install xlrd.

    #On ubuntu these terminal commands should do it:

    easy_install pip

    pip install xlrd
    
    # on mac
    brew install python && pip install xlrd

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
