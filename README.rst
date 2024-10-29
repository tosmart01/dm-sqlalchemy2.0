DM dialect for SQLAlchemy

installation
------------

To install this dialect run::

    for linux::
    $ python setup.py bdist_rpm
    
    for windows::
    $ python setup.py bdist_wininst

or from source::

    $ python ./setup.py install


usage
-----

To start using this dialect::

    from sqlalchemy import create_engine
    engine = create_engine('dm+dmPython://SYSDBA:SYSDBA@localhost:5236')
    engine = create_engine('dm://SYSDBA:SYSDBA@localhost:5236')

If you don't want to install this library (for example during development) add
this folder to your PYTHONPATH and register this dialect with SQLAlchemy::

    from sqlalchemy.dialects import registry
    registry.register("dm", "sqlalchemy_dm.dmPython", "DMDialect_dmPython")
    registry.register("dm.dmPython", "sqlalchemy_dm.dmPython", "DMDialect_dmPython")

Authors
-------

 * Dameng
 * Caichichi
 
