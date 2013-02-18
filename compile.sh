#!/bin/sh

latexmk -pdflatex='xelatex %O %S' -pdf main.tex -g
