sphinxcontrib-excel-table-plus
==============================

The sphinxcontrib-excel-table-plus extension is to render an excel file as an excel-alike table in Sphinx documentation.

This contrib is inspired by sphinxcontrib-excel, which uses pyexcel and handsontable to do the
work, but the sphinxcontrib-excel-table-plus will instead use openpyxl and handsontable, mainly to
support the following features:

* merged cell
* display specific sheet
* display specific section in one sheet
* display specific rows in one sheet
* (plus) added support to render html in columns

Installation
------------

You can install it via pip:

.. code-block:: bash

    $ pip install sphinxcontrib-excel-table-plus

or install it from source code:

.. code-block:: bash

    $ git clone https://github.com/emerge-ehri/sphinxcontrib-excel-table-plus.git
    $ cd sphinxcontrib-excel-table-plus
    $ python setup.py install

Setup
-----

Add sphinxcontrib.excel_table_plus to your conf.py file::

    extensions = ['sphinxcontrib.excel_table_plus']

And you need to copy the resource files to your sphinx source directory, the resource files
has been installed to your python system path if you install the package via pip, you can copy
them from the installation path. You can get the installation path through::

    python -c "import sphinxcontrib.excel_table_plus; print sphinxcontrib.excel_table_plus"

for example in Mac:

.. code-block:: bash

    $ INSTALLATION_PATH=/Library/Python/2.7/site-packages/sphinxcontrib/excel_table_plus/
    $ cp $INSTALLATION_PATH/resources/_templates/layout.html path/to/your/project/_templates/
    $ cp $INSTALLATION_PATH/resources/_static/handsontable.full.min.js path/to/your/project/_static/
    $ cp $INSTALLATION_PATH/resources/_static/handsontable.full.min.css path/to/your/project/_static/

or you can copy the resource files from source code directly.

Usage
-----

Here is the syntax to present your excel file in sphinx documentation:

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx

This will translate to:

.. image:: https://raw.githubusercontent.com/emerge-ehri/sphinxcontrib-excel-table-plus/master/sphinx_excel_table.png

As you can see, it supports merged cells, and this is the mainly goal this contrib will achieve, because other sphinxcontrib excel extensions don't support this feature, and are not convenient to implement it. The sphinxcontrib-excel-table-plus can do this easily using openpyxl library.

Options
-------

This sphinxcontrib provides the following options:

**file (required)**

Relative path (based on document) to excel documentation. Note that as openpyxl only supports excel xlsx/xlsm/xltx/xltm files, so this contrib doesn't support other old excel file formats like xls.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx

**(NEW IN PLUS) transforms (optional)**

Relative path (based on document) to a json file that contains configuration for transforming cell values in the table using regular expressions. There are two "type"s of transformations that can be configured, both types will use a regex search to find all "matcher"s and substitute them with the corresponding "replacer"s. The type="decoder" version will additionally replace named group portions with decoded values (see below for how to configure). The schema for the json and the meaning is as follows:

.. code-block:: JSON

    {
        "transforms" : array of transforms with the following structure
            {   "type"    : (required) string enumeration (allowed values "substitution" or "decoder")
                "rows"    : (optional) csv string of row numbers to apply this transform, if blank or missing then all rows (e.g. "1", "1, 3, 4")
                "cols"    : (optional) csv string of column numbers to apply this transform, if blank or missing then all columns (e.g. "1", "1, 3, 4")
                "matcher" : (required) python regular expression to match and identify groupings to transform in "replacer" attribute (e.g. "(?P<label>Required|Fixed|Optional): ")
                "replacer": (required for type=substitution) python regular expression that replaces the matcher expression (e.g. for substitution "<b>\\1:</b>, for decoder "<a href=\\'{decoder.href}\\'>\\1</a>)" ")
                "group_decoders" : (required for type=decoder) array [] of the following sub-structure...
                    {   "group"    : (required) the regex grouper name from the "matcher" regex (e.g.  "label")
                        "decoders" : (required) a structure that maps to a python dictionary of key : object pairs
                            (e.g.
                                key        : object of attribute : value pairs for substituting with the {decoder.attribute} replacements in the "replacer" string before final substitutions              :
                                "Required" : {"href":"val1", "attrib2":"otherval1"},
                                "Fixed"    : {"href":"val2", "attrib2":"otherval2"},
                                "Optional" : {"href":"val3", "attrib2":"otherval3"}
                            )
                    }
            }
    }

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :transforms: path/to/transforms.json

**sheet (optional)**

Specify the name of the sheet to dispaly, if not given, it will default to the first sheet in the excel file.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :sheet: Sheet2

Note this contrib can only display one sheet in one excel-table-plus directive, but you can display different sheet in one excel in different directives.

**rows (optional)**

Specify the row range of one sheet do display, the default is to display all rows in one sheet, if you use this option, remember to specify a range seperated by a colon.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :rows: 1:10

**selection (optional)**

Selection defines from and to the selection reaches. If value is not defined, the whole data from sheet is taken into table. And if selection is used, it must specify the from and to range seperated by a colon.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :selection: A1:D10

**overflow (optional)**

Prevents table to overlap outside the parent element. If 'horizontal' option is chosen then table will appear horizontal
scrollbar in case where parent's width is narrower then table's width. The default is 'horizontal', if you want to disable this feature, you can set false to this option.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :overflow: false

**tablewidth (optional)**

Defines spreadsheet width in pixels. Accepts number, string (that will be converted to a number). The underlying
spreadsheet implementation defaults to a width of 600px, you can change the value here if needed.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :tablewidth: 1000

**colwidths (optional)**

Defines column widths in pixels. Accepts number, string (that will be converted to a number),
array of numbers (if you want to define column width separately for each column) or a
function (if you want to set column width dynamically on each render). The default value is undefined, means the width will be determined by the parent elements.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :colwidths: 100

**row_header (optional)**

To decide whether to show the row header, the default is true, means to show the row header, you can
set this to false to disable the row header.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :row_header: false

**col_header (optional)**

To decide whether to show the col header, the default is true, means to show the col header, you can
set this to false to disable the col header.

.. code-block::

    .. excel-table::
       :file: path/to/file.xlsx
       :col_header: false
