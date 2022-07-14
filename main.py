from pydoc import classname
from pywinauto import application, findwindows
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until_passes
import time

app = application.Application(backend='uia')
app.start("C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe")

window_handler = wait_until_passes(10, 0.5, lambda: findwindows.find_window(title="Adobe Acrobat Reader DC (64-bit)", class_name="AcrobatSDIWindow"))

window = app.window_(handle=window_handler)

# Expande o menu de abrir
window.descendants(control_type="MenuBar")[1].children()[0].expand()

window.children(title="Arquivo", control_type="Menu")[0].children(title="Abrir... Ctrl+O")[0].click_input()

popup_handler = wait_until_passes(10, 0.5, lambda: findwindows.find_window(title="Abrir"))
popup = app.window_(handle=popup_handler)

# Aqui eu especifico a path que eu preciso
popup.children(title="Nome:", class_name='ComboBox')[0].select(r"C:\Users\Batista\Desktop\Algoritmos Aproximativos - Relatório Apresentação.pdf")
popup.children(title="Abrir", class_name="Button")[0].click_input()

#time.sleep(1)

window.descendants(control_type="MenuBar")[1].children()[0].expand()
window.children(title="Arquivo", control_type="Menu")[0].children(title="Salvar como... Shift+Ctrl+S")[0].click_input()

time.sleep(3)
send_keys("{ENTER}")

popup_handler2 = wait_until_passes(10, 0.5, lambda: findwindows.find_window(title="Salvar como"))
popup2 = app.window_(handle=popup_handler2)


popup2.children(control_type='Pane')[0].children(title='Nome:', control_type='ComboBox')[0].type_keys(r"C:\Users\Batista\Desktop\down\Apresentação2.pdf")
popup2.children(title='Salvar', control_type='Button')[0].click_input()

try:
  popup_handler3 = findwindows.find_window(title="Confirmar Salvar como")
  popup3 = app.window_(handle=popup_handler3)
  popup3.children(title='Sim', control_type='Button')[0].click_input()


except (findwindows.WindowNotFoundError):
  pass

window.descendants(control_type="MenuBar")[1].children()[0].expand()
window.children(title='Arquivo')[0].children(title='Sair do aplicativo Ctrl+Q')[0].click_input()
