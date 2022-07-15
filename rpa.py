import constants
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
from pywinauto_utils import expand_archive_menu, click_archive_option, find_window_no_wait, start_application, find_window
import time
from file_utils import gen_modified_path, get_article_pdf_files

def automate_file_renaming(*, files, app, window):
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

def close_application(window):
  expand_archive_menu(window)
  click_archive_option(window, option=constants.EXIT_APP_OPTION)