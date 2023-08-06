usage: swapdf [-h] input_file output_file

    swapdf 0.9.2

SWAP PDF pages after scan of a two-sided sheet pack through a one-sided feeder.

Let's have a two-sided sheet pack we want scan through a one-sided feeder. Then:

    - we open the scan utility, namely simple-scan
    - we click the "All Pages From Feeder" option
    - we scan all odd pages
    - then we put again the pack upside down in the feeder
    - we scan all even pages
    - finally we save our pages in a file, say scanned.pdf

Now scanned.pdf contains odd pages in ascending order, followed by even pages in
descending order.

For instance, say our sheets are 4, so our pages are 8, and scanned.pdf contains
the pages:

    1 3 5 7 8 6 4 2
    
We issue at terminal:

    $ swapdf scanned.pdf mydoc.pdf
    'scanned.pdf' -> 8 pages -> 'mydoc.pdf'

Now mydoc.pdf contains the pages:

    1 2 3 4 5 6 7 8

in the right order.

positional arguments:
    
    input_file   pages from scanner 1 3 5 ... 6 4 2
    output_file  swapped pages 1 2 3 4 5 6 ...

optional arguments:
    
    -h, --help   show this help message and exit
