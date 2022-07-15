from pathlib import Path, PurePath
from os import listdir
from os.path import isfile, join
import re

def is_valid_pdf_file(path, file):
  return ( 
    isfile(join(path, file)) and 
    Path(file).suffix == '.pdf' and 
    file[0].isdigit()
    )

def gen_modified_path(file_path):
  pure_file_path = PurePath(file_path).parts
  page_number = re.findall('[0-9]+', pure_file_path[-1])[0]
  return Path(*pure_file_path[:-1], 'Página {} – Modificado'.format(page_number))

def get_article_pdf_files(path):
  print(path)
  print(listdir(path))
  return [join(path, f) for f in listdir(path) if is_valid_pdf_file(path, f)]
