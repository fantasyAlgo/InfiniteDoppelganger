from pyray import *


init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    draw_rectangle(50, 50, 500, 500, (0,155,0, 255))
    end_drawing()
close_window()
