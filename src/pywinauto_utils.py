from pywinauto import application, findwindows
from pywinauto.timings import wait_until_passes

import constants


def expand_archive_menu(window):
    """
    Expands the Archive menu for the Adobe Acrobat application.

    This function tries to expand the archive menu for the Adobe Acrobat
    PDF Reader, showing all the possible options. 

    Parameters
    ----------
    window : 
        Current pywinauto window where the application is located.
    """
    wait_until_passes(
        10,
        0.5,
        lambda: window.descendants(
            title=constants.APPLICATION,
            control_type="MenuBar"
        )[0].children()[0].expand()
    )


def click_archive_option(window, option):
    """
    Clicks on a option inside the Archive menu for the Adobe Acrobat app.

    This function selects an option located inside the Archive option for the
    Adobe Acrobat PDF Reader application. Make sure that the Archive menu is
    expanded beforehand by using the expand_archive_menu funtion.

    Parameters
    ----------
    window 
        Current pywinauto window where the application is located.

    option : String
        Option that will be chosen. Check constants.py
    """
    wait_until_passes(
        10,
        0.5,
        lambda: window.children(
            title=constants.ARCHIVE,
            control_type="Menu"
        )[0].children(title=option)[0].click_input()
    )


def start_application(*, exec_path, app_title, app_class):
    """
    Starts an appliocation and returns the pywinauto objects related to it.

    This function receives the path for the .exe file for the program that will
    be executed, as well as the title and class for pywinauto to indentify the
    app execution. It then returns the app and window objects, required by
    other functions.

    Parameters
    ----------
    exec_path: String
        Complete path for the application .exe file. Check constants.py

    app_title: String
        Application title for pywinauto recognition. Check constants.py

    app_class: String
        Application class for pywinauto recognition. Check constants.py

    Returns
    -------
    Tuple< Application, Window >
        The Application and Window objects for pywinauto.
    """
    app = application.Application(backend='uia').start(exec_path)
    window = find_window(
        app=app,
        window_title=app_title,
        window_class=app_class
    )
    return [app, window]


def find_window(*, app, window_title, window_class=None):
    """
    Finds a window for pywinauto, with specified attributes, returning it.

    This function tries to find a window with an specified title while an
    Application is executed. Optionally, you can also provide the class
    of the window. If found, the window is then returned. 
    If not found, this function will retry it respecting a certain threshold.

    Parameters
    ----------
    app: Application
        Current application being executed by pywinauto.
        
    window_title: String
        Window title for pywinauto recognition. Check constants.py

    window_class: String [Optional]
        Window class for pywinauto recognition. Check constants.py

    Returns
    -------
    Window
        The Window object for pywinauto, representind the found window.
    """
    window_handler = wait_until_passes(
        10,
        0.5,
        lambda: findwindows.find_window(
            title=window_title,
            class_name=window_class
        )
    )
    return app.window_(handle=window_handler)


def find_window_no_wait(*, app, window_title, window_class=None):
    """
    Try to find a window for pywinauto, with specified attributes, once.

    This function tries to find a window with an specified title while an
    Application is executed. Optionally, you can also provide the class
    of the window. If found, the window is then returned. 

    Parameters
    ----------
    app: Application
        Current application being executed by pywinauto.
        
    window_title: String
        Window title for pywinauto recognition. Check constants.py

    window_class: String [Optional]
        Window class for pywinauto recognition. Check constants.py

    Returns
    -------
    Window
        The Window object for pywinauto, representind the found window.
    """
    window_handler = findwindows.find_window(
        title=window_title,
        class_name=window_class
    )
    return app.window_(handle=window_handler)
