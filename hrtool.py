# https://gist.github.com/miratcan/429895ef7c78a2c00cb7de9a44b11e6b
import os
import re
import glob
import subprocess
import sys

from os.path import exists
from sys import exit

cwd = os.getcwd()
INPUT_FOLDER = cwd + '/py/input/'
OUTPUT_FOLDER = cwd + '/py/output/'
SOLUTION_FILE = cwd + '/solution.py'
WRONG_PLACE_TO_RUN_MSG = 'You have to run this program under, downloaded inputs and outputs.'
REQUIRED_FOLDERS = [INPUT_FOLDER, OUTPUT_FOLDER]
NUMBER_FINDER = re.compile(r'\d+.txt$')

def get_output_filename(input_filename):
  return OUTPUT_FOLDER + 'output%s' % NUMBER_FINDER.findall(input_filename)[0]

wrong_place_to_run = False
for folder in REQUIRED_FOLDERS:
  if not exists(folder):
    print('Folder \'%s\' does not exists. ' % folder)
    wrong_place_to_run = True

if wrong_place_to_run:
  print(WRONG_PLACE_TO_RUN_MSG)
  exit(1)

passed, failed = 0, 0
if not exists(SOLUTION_FILE):
  print('Solution must be inside solution.py, put your solution to there and run this command again.')
  exit(1)

input_files = glob.glob(INPUT_FOLDER + '*.txt')

print('')
for input_file in input_files:
  output_file = get_output_filename(input_file)
  cmd = 'python3 solution.py ' + str(os.getpid())
  
  process = subprocess.Popen(
   cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
   text=True,
   shell=True)
  
  with open(input_file) as f:
    input_data = f.read()
  
  with open(output_file) as f:
    output_data = f.read()
  
  _out, err = process.communicate(input=input_data)
  
  if err:
    print(err)
    exit(1)
  out = ''
  for out_ in _out:
    out += out_
  if out and int(out) == int(output_data):
    # print(out)
    passed += 1
  else:
    print(os.path.basename(output_file) + ': ' + output_data.strip() + ' ? ' + out)
    failed += 1
print('\ntotal: {} passed: {} failed: {}'.format(passed + failed, passed, failed))

