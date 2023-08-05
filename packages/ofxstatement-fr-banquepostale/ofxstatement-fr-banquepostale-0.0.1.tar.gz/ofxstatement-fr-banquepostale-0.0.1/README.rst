~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
plugin for ofxstatement La Banque Postale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ofxstatement: https://github.com/kedder/ofxstatement

ofxstatement_ is a tool to convert proprietary bank statement to OFX format,
suitable for importing to GnuCash. 

La Banque Postale is a french bank. The plugin can convert PDF statements and
convert them to OFX format. Those statements contain more information than
the OFX files supplied by 'La Banque Postale'.

Parameters
----------

pdftotext
   path to the `pdftotext` binary (default `pdftotext`)

smart
   use smart algorithm for payee/memo split (default 'y')
