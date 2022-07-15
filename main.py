from requests import delete
import constants
import sys
from pywinauto_utils import start_application
from file_utils import delete_files, get_article_pdf_files
from rpa import automate_file_renaming, close_application
from os.path import isdir

def main():
  if(len(sys.argv) >= 2):
    dir_path = sys.argv[1]
  else:
    dir_path = input("Please, insert the file directory path: \n")

  if(len(sys.argv) >= 3):
    delete_input = sys.argv[2]
  else:
    delete_input = input("Would you like to erase the original files after completion? \n[Y]: Yes\n[N]: No (default)\n")

  if not isdir(dir_path):
    print("Invalid directory!\nPlease verify that you have entered a valid path.")
    return;

  PDF_FILES = get_article_pdf_files(dir_path)

  app, window = start_application(
    exec_path=constants.ACROBAT_APP_PATH, 
    app_title=constants.ACROBAT_APP_TITLE, 
    app_class=constants.ACROBAT_APP_CLASS
    )

  automate_file_renaming(
    files=PDF_FILES,
    app=app,
    window=window
    )
  close_application(window)

  if(delete_input.upper() == 'Y'):
    delete_files(PDF_FILES)

main()