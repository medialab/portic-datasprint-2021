#!/usr/bin/env python

"""
Script courtesy of imaziz (initial gist : https://gist.github.com/iamaziz/1d87582adcb4450b2f66)
"""

__author__ = 'Aziz'

"""
Convert all ipython notebook(s) in a given directory into the selected format and place output in a separate folder.
usages: python cipynb.py `directory` [-to FORMAT]
Using: ipython nbconvert and find command (Unix-like OS).
For a downloadable example of notebooks see:
    http://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/
"""

import os
import argparse


def get_path(dir):
    if os.path.exists(dir):
        return os.path.realpath(dir)
    else:
        print("No folder named {}!".format(dir))
        exit(0)


def collect_ipynbs(wdir):
    nbooks = os.popen('find {} -name "*.ipynb" -not -path "*/\.*"'.format(wdir)).read()
    if nbooks:
        ##___ clean up ipynb file names
        nbooks = nbooks.replace(" ", "\ ")  # avoid white spaces in a file name
        ipynb_files = nbooks.split('\n')    # split files by new line
        ipynb_files = filter(None, ipynb_files)
        return ipynb_files
    else:
        print("No ipython notebook(s) found in {}!".format(wdir))
        exit(0)


def change_to_output_dir(wdir, fldr):
    ##___ output directory
    outd = os.path.join(wdir, fldr.upper())
    if not os.path.exists(outd):
        os.makedirs(outd)
    os.chdir(outd)
    return outd


def get_format(to):
    available = ['pdf', 'html', 'latex', 'markdown', 'python', 'rst', 'slides']
    if to in available:
        return to
    else:
        print("UNKNOWN TYPE: {}".format(to))
        exit(0)


def convert_ipynb(ipynb_files, form, outputdir):
    print("Converting {} notebooks into {} ... \n\n".format( len(ipynb_files), form))
    for nb in ipynb_files:
        if form == 'pdf':
            convert_cmd = 'ipython nbconvert --to latex --post PDF {}'.format(nb)
        else:
            convert_cmd = 'ipython nbconvert --to {} {} --no-input'.format(form, nb)
        os.system(convert_cmd)
    print("\nSee output at: {}".format(outputdir))


def main():
    #___ parse input
    desc = 'Convert all ipython notebook(s) in a given directory into the selected format and place output in a separate folder. Using: ipython nbconvert and find command (Unix-like OS only).'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("dir", help="Name of the folder where the `*.ipynb` files are (or in its sub-folders).", type=str)
    parser.add_argument("-to", help="Convert to what format. (default: pdf) other formats: html, latex, markdown, python, rst, or slides.", default='pdf', type=str)
    args = parser.parse_args()

    #___ validate args
    wdir = get_path(args.dir)
    convert_to = get_format(args.to)

    #___ start
    ipynb_files = list(collect_ipynbs(wdir))
    output_dir = change_to_output_dir(wdir, convert_to)
    convert_ipynb(ipynb_files, convert_to, output_dir)

if __name__ == '__main__':
    main()