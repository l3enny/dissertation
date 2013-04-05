#!/bin/sh

latexmk -pdflatex='xelatex %O %S' -pdf thesis-sample -g
