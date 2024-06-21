import ctypes
user32 = ctypes.windll.user32
screen_widht= int(user32.GetSystemMetrics(0)/2)
screen_height= int(user32.GetSystemMetrics(1)-100)