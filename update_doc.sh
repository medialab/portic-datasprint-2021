#!/bin/bash
jupyter nbconvert --to html documentation_lib.ipynb
mv documentation_lib.html index.html