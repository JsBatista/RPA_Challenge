import constants
import pandas as pd
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
from pywinauto_utils import expand_archive_menu, click_archive_option, find_window_no_wait, find_window
import time
from file_utils import gen_modified_path, gen_report_path
from os.path import exists
from pathlib import PurePath

def automate_file_renaming(*, files, app, window):
  if len(files) > 0:
    create_csv_empty_report(files[0])
  
  for file_path in files:
    expand_archive_menu(window)
    click_archive_option(window, option=constants.OPEN_FILE_OPTION)

    open_file_window = find_window(app=app, window_title=constants.OPEN_FILE_WINDOW)

    open_file_window.children(
      title=constants.FILE_NAME_FIELD, 
      control_type="ComboBox"
      )[0].children()[0].set_text(file_path)

    open_file_window.children(
      title=constants.OPEN_FILE_BUTTON, 
      class_name="Button"
      )[0].click_input()

    expand_archive_menu(window)
    click_archive_option(window, option=constants.SAVE_AS_OPTION)

    time.sleep(3)
    send_keys("{ENTER}")

    save_as_window = find_window(
      app=app, 
      window_title=constants.SAVE_AS_WINDOW
      )

    combo_box_field = save_as_window.children(control_type="Pane")[0].children(
      title=constants.FILE_NAME_FIELD, 
      control_type="ComboBox"
      )[0].children(title=constants.FILE_NAME_FIELD)[0]

    combo_box_field.set_text(gen_modified_path(file_path))
    combo_box_field.set_focus()
    combo_box_field.type_keys(" ", with_spaces=True)

    save_as_window.children(
      title=constants.SAVE_FILE_BUTTON, 
      control_type="Button"
      )[0].click_input()

    try:
      confirmation_window = find_window_no_wait(
        app=app, 
        window_title=constants.CONFIRM_SAVE_WINDOW
        )
      confirmation_window.children(
        title=constants.YES_BUTTON, 
        control_type="Button"
        )[0].click_input()

    except (findwindows.WindowNotFoundError):
      pass

    add_report_entry(file_path)

def close_application(window):
  expand_archive_menu(window)
  click_archive_option(window, option=constants.EXIT_APP_OPTION)

def create_csv_empty_report(path):
  report_path = gen_report_path(path)
  if not exists(report_path):
    data = {
      constants.DOCUMENT_NAME_COLUMN: [], 
      constants.DOCUMENT_STATUS_COLUMN: []
      }
    pd.DataFrame(data).to_csv(report_path, index=False)

def add_report_entry(file_path):
  report_path = gen_report_path(file_path)
  data = {
    constants.DOCUMENT_NAME_COLUMN: [PurePath(file_path).parts[-1]], 
    constants.DOCUMENT_STATUS_COLUMN: [constants.FINISHED_STATUS_VALUE]
  }
  pd.DataFrame(data).to_csv(
    report_path, 
    mode="a", 
    index=False, 
    header=False
    )