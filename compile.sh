#!/bin/sh

cp ~/Dropbox/References/Thesis.bib .
latexmk -xelatex -pdf main
