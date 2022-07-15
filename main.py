import constants
from pywinauto_utils import start_application
from file_utils import get_article_pdf_files
from rpa import automate_file_renaming, close_application

DUMMY_PATH = r"C:\Users\Batista\Desktop\down\RPA - Artigo"

PDF_FILES = get_article_pdf_files(DUMMY_PATH)

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
