from pywinauto import application, findwindows
from pywinauto.timings import wait_until_passes

def expand_archive_menu(window):
  wait_until_passes(10, 0.5, lambda: window.descendants(title='Aplicativo', control_type="MenuBar")[0].children()[0].expand())

def click_archive_option(window, option):
  wait_until_passes(10, 0.5, lambda: window.children(title="Arquivo", control_type="Menu")[0].children(title=option)[0].click_input())

def start_application(*, exec_path, app_title, app_class):
  app = application.Application(backend='uia').start(exec_path)
  window = find_window(app=app, window_title=app_title, window_class=app_class)
  return [app, window]

def find_window(*, app, window_title, window_class = None):
  window_handler = wait_until_passes(10, 0.5, lambda: findwindows.find_window(title=window_title, class_name=window_class))
  return app.window_(handle=window_handler)