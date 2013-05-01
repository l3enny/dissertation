Dissertation
============

This repository contains all the necessary files to build my
dissertation. This includes the text, data, and figures. Languages used
will (probably) include:

* XeTeX
* Gnuplot
* Shell scripts

While it is tempting to integrate the two, the data analysis will be
separate from the dissertation. If this sounds interesting to you, check
out Sweave (an unholy merging of LaTeX and R). I would do it myself if I
hadn't already set myself the goal of using gnuplot (I may end up
returning to Veusz instead).

If I have done my job right, all you'll need is a (close to) bog
standard TeX distribution (I am using some variety of TeX Live on Mac
and GNU/Linux). To compile, simply type:

    latexmk -xelatex -pdf main

The, somewhat awkward, command is a result of the obsolete version of
latexmk that is on my machine. If you're fortunate enough to have
version >= 4.31, then the simple switches '-xelatex -pdf' should suffice.
