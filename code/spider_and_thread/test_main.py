from test_ui import *
from test_time import *

a = GUI()
a.window_init()

a.ui_thread_start()
a.timer_thread_start()

a.main_window.mainloop()

a.ui_thread.join()
a.timer_thread.join()


