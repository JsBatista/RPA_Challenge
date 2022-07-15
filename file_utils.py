from os import listdir, remove
from os.path import isfile, join
import re

from pathlib import Path, PurePath

import constants

def is_valid_pdf_file(dir_path, file_name):
  """
    Verifies if a file within a path is a valid pdf file for the challenge.

    This function runs a series of checkings to see if the specified file:
      - Is an actual file
      - Is a .pdf file
      - Has its name starting with a number

    Parameters
    ----------
    dir_path : string
        Directory path there the file is located.
    file_name : string
        Name of the specified file.

    Returns
    -------
    boolean
        If the file passes all the verifications and is indeed a valid file.
    """
  return ( 
    isfile(join(dir_path, file_name)) and 
    Path(file_name).suffix == '.pdf' and 
    file_name[0].isdigit()
    )


def gen_modified_path(file_path):
  """
    Generates a new path for the file, following the challenge's specification.

    This function processes the path of the specified file and returns a
    new path where the directory of the file is the same, but the file 
    name is changed by the folowing pattern:

    Original name: <NUMBER><rest of the name>
    New name: <PREFIX> <NUMBER> - <SUFFIX>

    <PREFIX> and <SUFFIX> are specified in constants.py 
    
    Parameters
    ----------
    file_path : string
        Full path of the specified file.

    Returns
    -------
    Path
        The new path according to the challenge's specification.
    """
  pure_file_path = PurePath(file_path).parts
  page_number = re.findall('[0-9]+', pure_file_path[-1])[0]
  return Path(
    *pure_file_path[:-1], 
    '{prefix} {page} – {suffix}'.format(
      prefix=constants.PAGE_PREFIX, 
      page=page_number, 
      suffix=constants.PAGE_SUFFIX
      )
    )


def get_article_pdf_files(path):
  """
    Generates the valid pdf files path inside a directory.

    According to the is_valid_pdf_file checking, this function will check
    inside a directory for all valid pdf files inside of it. It then returns an
    array containing all the complete paths for these files.
    
    Parameters
    ----------
    path : string
        Directory path there the file are located.

    Returns
    -------
    List<Path>
        List of the paths for the valid files inside the directory.
    """
  return [join(path, f) for f in listdir(path) if is_valid_pdf_file(path, f)]

def gen_report_path(file_path):
  """
    Returns the path where the report file will be generated.

    This function processes the path of one of the .pdf files and returns
    the complete path for the generated report file. The report file 
    will always be generated in the same folder as the original .pdf files. 
    
    Parameters
    ----------
    file_path : string
        The complete path for one of the .pdf files.

    Returns
    -------
    Path
        The complete path for the report .csv file.
    """
  pure_file_path = PurePath(file_path).parts
  return Path(
    *pure_file_path[:-1], 
    "{}.csv".format(constants.REPORT_FILE_NAME)
    )

def delete_files(files):
  """
    Deletes all specified files.

    This function receives a list of files that will be deleted.
    Please, make sure that these files aren't used by any other processes
    before calling this function. 
    
    Parameters
    ----------
    files : List<string>
        A list with the complete paths for the files that should be deleted.
    """
  for file_path in files:
    remove(file_path)