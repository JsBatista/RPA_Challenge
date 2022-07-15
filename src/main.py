from os.path import isdir
import sys

import constants
from pywinauto_utils import start_application
from file_utils import delete_files, get_article_pdf_files
from rpa import automate_file_renaming, close_application

def main():
  """
    Runs the primary script functionalities.

    This function checks for the user input and passes it in order to
    correctly perform all the RPA functionalities stablished on the challenge
    description.
    """
  
  # Extracts the path of the directory containing all the .pdf files. 
  if(len(sys.argv) >= 2):
    dir_path = sys.argv[1]
  else:
    dir_path = input("Please, insert the file directory path: \n")

  # Checks if the original files should be deleted after the task completion. 
  if(len(sys.argv) >= 3):
    should_delete_files = sys.argv[2]
  else:
    should_delete_files = input(
      "Would you like to erase the original files after completion?\n"
      "[Y]: Yes\n[N]: No (default)\n"
      )

  # Checks if the received path is a valid directory. 
  if not isdir(dir_path):
    print(
      "Invalid directory!\nPlease verify that you have entered a valid path."
      )
    return;

  pdf_files = get_article_pdf_files(dir_path)

  app, window = start_application(
    exec_path=constants.ACROBAT_APP_PATH, 
    app_title=constants.ACROBAT_APP_TITLE, 
    app_class=constants.ACROBAT_APP_CLASS
    )

  automate_file_renaming(
    files=pdf_files,
    app=app,
    window=window
    )
  close_application(window)

  # Delete the files if needed.
  if(should_delete_files.upper() == 'Y'):
    delete_files(pdf_files)

main()