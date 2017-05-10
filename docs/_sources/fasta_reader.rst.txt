.. _fasta_reader:


=======================================
Lightweight and efficient Fasta reader.
=======================================

I'm not the author of this fasta reader.
I found it on http://biostar.stackexchange, but the url of this code is not available anymore.
So I decide to adapt it to python3 and share it on this site.

This Fasta parser is not very robust as if your file is not a well formed fasta the code does not detect it.
The file must begin by '>' otherwise the parser fail.
It's a very compact code only 6 lines but very efficient.
But the code is very simple and it's easy to add some controls if necessary.
An other advantage of this code is that it is an iterator,
so the memory footprint is rather low.


.. literalinclude:: _static/code/fasta_iterator.py
   :linenos:
   :language: python

:download:`fasta_iterator.py <_static/code/fasta_iterator.py>` .