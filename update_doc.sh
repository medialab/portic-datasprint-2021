#!/bin/bash
jupyter nbconvert  --clear-output --to html documentation_lib.ipynb
mv documentation_lib.html index.html