import ctypes
import msvcrt
import time
user32 = ctypes.windll.user32

class Point(ctypes.Structure):
    _fields_= [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long)
    ]

class Rect(ctypes.Structure):
    _fields_= [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(f"{screen_width}x{screen_height}")

point = Point()
prison = Rect(300, 300, 700, 700)
monitor_limit = Rect(0, 0, screen_width, screen_height)

prison_active = False
program_is_running = True

def check_cursor_position():
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def get_keyboard_key():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key in (b"\x00", b"\xe0"):
            key = msvcrt.getch()
            return key
        if key == b" ":
            return key
        return key.decode()
    return None

def toggle_prison():
    global prison_active
    if prison_active:
        user32.ClipCursor(None)
        prison_active = False
        print("Border deactivated")
    else:
        user32.ClipCursor(ctypes.byref(prison))
        prison_active = True
        print("Border activated")
 
speed = 10

def action_by_key(x, y, key):
    match key:
            case b"M":
                user32.SetCursorPos(x + speed, y)
            case b"K":
                user32.SetCursorPos(x - speed, y)
            case b"H":
                user32.SetCursorPos(x, y - speed)
            case b"P":
                user32.SetCursorPos(x, y + speed)
            case b" ":
                toggle_prison()
            case "q":
                shut_down()


def shut_down():
    global program_is_running
    program_is_running = False
def mainloop():
    global program_is_running
    while program_is_running:
        
        x, y = check_cursor_position()
        
        key = get_keyboard_key()
        action_by_key(x, y, key)
        
        x, y = check_cursor_position()

        time.sleep(1/30)
        # print(str_position)

try:
    mainloop()
finally:
    print("\nProgram terminated.\n")
    user32.ClipCursor(None)
