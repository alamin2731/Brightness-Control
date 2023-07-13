import tkinter as tk
from tkinter import ttk
import wmi

def set_brightness(level):
    # Connect to the WMI service
    c = wmi.WMI(namespace='wmi')

    # Get the active display
    brightness_methods = c.WmiMonitorBrightnessMethods()[0]
    brightness_methods.WmiSetBrightness(level, 0)

def update_brightness(event):
    brightness_level = custom_brightness_slider.get()
    set_brightness(brightness_level)
    update_brightness_label(brightness_level)

def increase_brightness():
    current_brightness = get_brightness()
    brightness_level = min(100, current_brightness + 10)
    set_brightness(brightness_level)
    update_brightness_label(brightness_level)
    custom_brightness_slider.set(brightness_level)

def decrease_brightness():
    current_brightness = get_brightness()
    brightness_level = max(0, current_brightness - 10)
    set_brightness(brightness_level)
    update_brightness_label(brightness_level)

def get_brightness():
    # Connect to the WMI service
    c = wmi.WMI(namespace='wmi')

    # Get the active display
    brightness = c.WmiMonitorBrightness()[0]
    return brightness.CurrentBrightness

def update_brightness_label(level):
    brightness_label.config(text=f"Brightness: {level}%", foreground="white", background="#303030")
    brightness_preview_frame.config(bg="#303030", width=int(level * 2))

def change_brightness_mode(event):
    mode = brightness_mode_combo.get()
    if mode == "Movie":
        set_brightness(80)
        update_brightness_label(80)
        custom_brightness_slider.set(80)
    elif mode == "Work":
        set_brightness(60)
        update_brightness_label(60)
        custom_brightness_slider.set(60)
    elif mode == "Gaming":
        set_brightness(90)
        update_brightness_label(90)
        custom_brightness_slider.set(90)
    elif mode == "Reading":
        set_brightness(70)
        update_brightness_label(70)
        custom_brightness_slider.set(70)
    # Add more modes here

# Create the main window
window = tk.Tk()
window.title("Brightness Control")
window.geometry("400x300")
window.resizable(True, False)
window.configure(bg="#303030")

# Create styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))

# Create GUI elements
title_label = ttk.Label(window, text="Brightness Control", style="TLabel", background="#303030", foreground="white")
title_label.pack(pady=10)

brightness_buttons_frame = tk.Frame(window, bg="#303030")
brightness_buttons_frame.pack()

increase_button = ttk.Button(brightness_buttons_frame, text="Increase Brightness", command=increase_brightness, style="TButton")
increase_button.pack(side=tk.LEFT, padx=5)

decrease_button = ttk.Button(brightness_buttons_frame, text="Decrease Brightness", command=decrease_brightness, style="TButton")
decrease_button.pack(side=tk.LEFT, padx=5)

custom_brightness_label = ttk.Label(window, text="Custom Brightness", style="TLabel", background="#303030", foreground="white")
custom_brightness_label.pack()

custom_brightness_slider = ttk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=update_brightness)
custom_brightness_slider.pack()

brightness_mode_label = ttk.Label(window, text="Brightness Modes", style="TLabel", background="#303030", foreground="white")
brightness_mode_label.pack(pady=10)

brightness_modes = ["Movie", "Work", "Gaming", "Reading"]
brightness_mode_combo = ttk.Combobox(window, values=brightness_modes, state="readonly")
brightness_mode_combo.current(0)
brightness_mode_combo.bind("<<ComboboxSelected>>", change_brightness_mode)
brightness_mode_combo.pack()

brightness_label = ttk.Label(window, text="Brightness: --", style="TLabel", background="#303030", foreground="white")
brightness_label.pack(pady=10)

brightness_preview_frame = tk.Frame(window, bg="#303030", width=0, height=20)
brightness_preview_frame.pack()

window.mainloop()
#use this to create .exe file with icon
#pyinstaller --onefile --noconsole --name=Brightness-control brightness_control.py
