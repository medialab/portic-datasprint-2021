#!/usr/bin/env python
from urllib.parse import quote
import re
import uuid
import base64
import os
import sys

"""
Script forked and modified from a first version of imaziz (initial gist : https://gist.github.com/iamaziz/1d87582adcb4450b2f66)
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

PUB_URL_BASE = 'https://medialab.github.io/portic-datasprint-2021/'


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
            convert_cmd = 'jupyter nbconvert --to latex --post PDF {}'.format(nb)
        else:
            convert_cmd = 'jupyter nbconvert --to {} {} --no-input'.format(form, nb)
        os.system(convert_cmd)
    print("\nSee output at: {}".format(outputdir))


def remove_tags(text):
  # scripts = re.compile(r'<script.*?/script>')
  scripts = re.compile(r'<(script).*?</\1>(?s)', re.DOTALL)
  # css = re.compile(r'<style.*?/style>', re.DOTALL)
  # tags = re.compile(r'<.*?>')

  text = scripts.sub('', text)
  # text = css.sub('', text)
  # text = tags.sub('', text)
  return text

  
def extract_images(filename, dir, assets_dir):
  print('extracting images from ', filename)
  book_parts = filename.split('/')[-1].split('.')
  book_name = '.'.join(book_parts[0:-1])
  base_path = assets_dir + '/' + quote(book_name + '-')
  base_url = PUB_URL_BASE + dir + 'assets/' + quote(book_name + '-')
  try:
    infile = open(filename, 'r')
  except FileNotFoundError:
    print('File not found: ', filename)
    return None
  content = infile.read()

  # Regular Expression match <img src=''
  pattern = re.compile(r'<img [^>]*src="([^"]+)')
  images = pattern.findall(content) # array
  print(len(images), ' images found')
  id = str(uuid.uuid4())
  # loop matched
  for index, url in enumerate(images):
    if url.startswith('data:image'): # 'data:image/jpeg;base64,' 'data:image/png;base64,'
      # get file suffix like "jpeg" "png"
      array = url.split('/')
      suffix = array[1].split(';')[0]
      # get the part after 'data:image/jpeg;base64,'
      data_array = url.split(',')
      base64_naked = data_array[1]
      imgdata = base64.b64decode(base64_naked)
      # save_filename = 'images/' + id + '.' + suffix
      save_filename = base_path + str(index) + '.' + suffix
      print("creating image", save_filename)
      # save image
      with open(save_filename, 'wb') as f:
        f.write(imgdata)
      # replace content
      img_wittcism = base_url + str(index) + '.' + suffix
      # print('url: ', url[0:10])
      # print('replace', img_wittcism)
      # print('length before', len(content))
      content = content.replace(url, img_wittcism)
      # print('length after', len(content))
  # save content to new file
  # print('final length', len(content))
  # stripping scripts
  content = remove_tags(content)
  # print('final length after clean', len(content))
  print('rewriting', filename)
  final_file = open(filename, "w")
  final_file.write(content)


def main():
    #___ parse input
    desc = 'Convert all ipython notebook(s) in a given directory into the selected format and place output in a separate folder. Using: ipython nbconvert and find command (Unix-like OS only).'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("dir", help="Name of the folder where the `*.ipynb` files are (or in its sub-folders).", type=str)
    parser.add_argument("-to", help="Convert to what format. (default: pdf) other formats: html, latex, markdown, python, rst, or slides.", default='pdf', type=str)
    args = parser.parse_args()

    #___ validate args
    wdir = get_path(args.dir)
    convert_to = get_format(args.to) if args.to is not None else 'html'

    #___ start
    ipynb_files = list(collect_ipynbs(wdir))
    output_dir = change_to_output_dir(wdir, convert_to)
    convert_ipynb(ipynb_files, convert_to, output_dir)
    # convert base64 images
    if convert_to == 'html':
      assets_dir = wdir + '/assets'
      # cleanup
      if not os.path.exists(assets_dir):
        # create
        try:
            os.mkdir(assets_dir)
        except OSError:
            print ("Creation of the directory %s failed" % assets_dir)
      html_files = [f.replace(".ipynb", ".html") for f in ipynb_files]
      for f in html_files:
        extract_images(f, args.dir, assets_dir)

if __name__ == '__main__':
    main()