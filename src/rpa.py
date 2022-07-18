from os.path import exists
from time import sleep

import pandas as pd
from pathlib import PurePath
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
from pywinauto_utils import expand_archive_menu, click_archive_option, find_window_no_wait, find_window

import constants
from file_utils import gen_modified_path, gen_report_path


def automate_file_renaming(*, files, app, window):
    """
    Rename all files using Adobe Acrobat Reader.

    This function renames all the files specified following the stablished 
    pattern (check file_utils.py). This is done by a RPA process using
    pywinauto. 

    Parameters
    ----------
    files : List<string>
        A list with the complete paths for the files that should be renamed.
    
    app: Application
        Current application being executed by pywinauto.
 
    window: Window
        Current window running the application with pywinauto.
    """

    # If we have no files, we don't need to create a report.
    if len(files) > 0:
        create_csv_empty_report(files[0])

    for file_path in files:
        expand_archive_menu(window)
        click_archive_option(window, option=constants.OPEN_FILE_OPTION)

        open_file_window = find_window(
            app=app,
            window_title=constants.OPEN_FILE_WINDOW
        )

        # Sets the file that should be opened
        open_file_window.children(
            title=constants.FILE_NAME_FIELD,
            control_type="ComboBox"
        )[0].children()[0].set_text(file_path)

        # Opens the file
        open_file_window.children(
            title=constants.OPEN_FILE_BUTTON,
            class_name="Button"
        )[0].click_input()

        expand_archive_menu(window)
        click_archive_option(window, option=constants.SAVE_AS_OPTION)

        # This is a sleep that I couldn't find a way to remove. We must wait for
        # the custom 'Save As' Acrobat window to show up and load its optioons.
        # However, we don't seem to have access to it in pywinauto.
        # Sleeping for 3 seconds seems more than enough time for it to load.
        sleep(3)
        send_keys("{ENTER}")

        save_as_window = find_window(
            app=app,
            window_title=constants.SAVE_AS_WINDOW
        )

        combo_box_field = save_as_window.children(control_type="Pane")[0].children(
            title=constants.FILE_NAME_FIELD,
            control_type="ComboBox"
        )[0].children(title=constants.FILE_NAME_FIELD)[0]

        # Sets the file name that should be saved
        # This is needed in order to set_text to actually updates the
        # comboBox value, otherwise, the changes are just visual.
        combo_box_field.set_text(gen_modified_path(file_path))
        combo_box_field.set_focus()
        combo_box_field.type_keys(" ", with_spaces=True)

        save_as_window.children(
            title=constants.SAVE_FILE_BUTTON,
            control_type="Button"
        )[0].click_input()

        # If we already have a file, a prompt will show up asking if we
        # want to replace it. We then click 'Yes' if it does.
        try:
            confirmation_window = find_window_no_wait(
                app=app,
                window_title=constants.CONFIRM_SAVE_WINDOW
            )
            confirmation_window.children(
                title=constants.YES_BUTTON,
                control_type="Button"
            )[0].click_input()

        # If the prompt doesn't show up, we just ignore this.
        except (findwindows.WindowNotFoundError):
            pass

        add_report_entry(file_path)

        # Closes the current file
        send_keys('^w')


def close_application(window):
    """
    Closes the Adobe Acrobat Reader app.

    This function closes the Adobe Acrobat application by using the in-app
    exit option.

    Parameters
    ----------
    window: Window
        Current window running the application with pywinauto.
    """
    expand_archive_menu(window)
    click_archive_option(window, option=constants.EXIT_APP_OPTION)


def create_csv_empty_report(path):
    """
    Creates a new report .csv file, if it doens't exists.

    Parameters
    ----------
    path: String
        A path for any .pdf valid file for the report path generation.
    """
    report_path = gen_report_path(path)
    if not exists(report_path):
        data = {
            constants.DOCUMENT_NAME_COLUMN: [],
            constants.DOCUMENT_STATUS_COLUMN: []
        }
        pd.DataFrame(data).to_csv(report_path, index=False)


def add_report_entry(file_path):
    """
    Adds a new entre for the report .csv file.

    Parameters
    ----------
    file_path: String
        The path for the file representing the current entry being added.
    """
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
