from pywinauto import findwindows
from pywinauto.keyboard import send_keys
from pywinauto_utils import expand_archive_menu, click_archive_option, start_application, find_window
import time
import constants

DUMMY_PATHS = [r"C:\Users\Batista\Desktop\Algoritmos Aproximativos - Relatório Apresentação.pdf", r"C:\Users\Batista\Desktop\Declaracao Nada Consta.pdf", r"C:\Users\Batista\Desktop\requerimento-de-outorga-de-grau-1a-via.pdf"]
DUMMY_SAVES = [r"C:\Users\Batista\Desktop\down\SuperArquivo1.pdf", r"C:\Users\Batista\Desktop\down\SuperArquivo2.pdf", r"C:\Users\Batista\Desktop\down\SuperArquivo3.pdf"]

app, window = start_application(exec_path=constants.ACROBAT_APP_PATH, app_title=constants.ACROBAT_APP_TITLE, app_class=constants.ACROBAT_APP_CLASS)

for i in range(0,3):
  expand_archive_menu(window)
  click_archive_option(window, option=constants.OPEN_FILE_OPTION)

  open_file_window = find_window(app=app, window_title=constants.OPEN_FILE_WINDOW)

  open_file_window.children(title=constants.FILE_NAME_FIELD, class_name="ComboBox")[0].select(DUMMY_PATHS[i])
  open_file_window.children(title=constants.OPEN_FILE_BUTTON, class_name="Button")[0].click_input()

  #time.sleep(1)

  expand_archive_menu(window)
  click_archive_option(window, option=constants.SAVE_AS_OPTION)

  time.sleep(3)
  send_keys("{ENTER}")

  save_as_window = find_window(app=app, window_title=constants.SAVE_AS_WINDOW)

  save_as_window.children(control_type="Pane")[0].children(title=constants.FILE_NAME_FIELD, control_type="ComboBox")[0].type_keys(DUMMY_SAVES[i])
  save_as_window.children(title=constants.SAVE_FILE_BUTTON, control_type="Button")[0].click_input()

  try:
    confirmation_window = find_window(app=app, window_title=constants.CONFIRM_SAVE_WINDOW)
    confirmation_window.children(title=constants.YES_BUTTON, control_type="Button")[0].click_input()

  except (findwindows.WindowNotFoundError):
    pass

expand_archive_menu(window)
click_archive_option(window, option=constants.EXIT_APP_OPTION)
