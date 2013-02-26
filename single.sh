#!/bin/sh

latexmk -pdflatex='xelatex %O %S' -pdf single.tex -g
