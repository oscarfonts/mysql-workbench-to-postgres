# mysql-workbench-to-postgres

Automatically exported from https://code.google.com/p/mysql-workbench-to-postgres/

## Original README (2011)

These script was tested with Mysql Workbench 5.1 in linux version.

The script receive a sql script file, originated by Mysql Workbenchs and
converts it to a PostgreSQL script compatible. The export is made by
Forward Engeneer SQL CREATE script option. The following options can't be
marked:

* Generate Separate CREATE INDEX Statments

Some of the options were not tested yet. The running syntax is:

    python exporter <input.sql> <output.sql>

This project is in early version, and any help is welcome.
