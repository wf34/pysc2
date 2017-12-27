import argparse
import os
import random
import shutil
import string


def make_random_string(N = 30):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) \
      for _ in range(N))


def make_random_tmp_path(N = 30):
  return os.path.join('/tmp', make_random_string(N))


def clear_dir(directory):
  if os.path.isdir(directory):
    shutil.rmtree(directory)


def remove_file(f):
  if os.path.isfile(f):
    os.remove(f)


def create_dir(directory):
  clear_dir(directory)
  os.makedirs(directory)


def check_file(path, ext = ''):
  if not path.endswith(ext) or not os.path.isfile(path) :
     raise argparse.ArgumentTypeError("{} is not a path to a {}".format(path, ext))
  return path


def check_exisiting_dir(path):
  if not os.path.isdir(path):
     raise argparse.ArgumentTypeError("{} is not a path to a dir".format(path))
  return path

