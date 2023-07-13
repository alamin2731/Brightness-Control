import tkinter as tk
from tkinter import ttk
import wmi
import ctypes

class BrightnessController:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Brightness Control")
        self.window.geometry("400x300")
        self.window.resizable(True, False)
        self.window.configure(bg="#303030")

        self.create_styles()
        self.create_gui_elements()

        self.check_wmi_compatibility()
        if not self.is_wmi_compatible:
            self.display_wmi_error()
        else:
            self.custom_brightness_slider.configure(state="normal")
            self.update_brightness_label(self.get_brightness())

        self.window.mainloop()

    def create_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))

    def create_gui_elements(self):
        title_label = ttk.Label(self.window, text="Brightness Control", style="TLabel", background="#303030", foreground="white")
        title_label.pack(pady=10)

        brightness_buttons_frame = tk.Frame(self.window, bg="#303030")
        brightness_buttons_frame.pack()

        increase_button = ttk.Button(brightness_buttons_frame, text="Increase Brightness", command=self.increase_brightness, style="TButton")
        increase_button.pack(side=tk.LEFT, padx=5)

        decrease_button = ttk.Button(brightness_buttons_frame, text="Decrease Brightness", command=self.decrease_brightness, style="TButton")
        decrease_button.pack(side=tk.LEFT, padx=5)

        custom_brightness_label = ttk.Label(self.window, text="Custom Brightness", style="TLabel", background="#303030", foreground="white")
        custom_brightness_label.pack()

        self.custom_brightness_slider = ttk.Scale(self.window, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=self.update_brightness, state="disabled")
        self.custom_brightness_slider.pack()

        brightness_mode_label = ttk.Label(self.window, text="Brightness Modes", style="TLabel", background="#303030", foreground="white")
        brightness_mode_label.pack(pady=10)

        brightness_modes = ["Movie", "Work", "Gaming", "Reading"]
        self.brightness_mode_combo = ttk.Combobox(self.window, values=brightness_modes, state="readonly")
        self.brightness_mode_combo.current(0)
        self.brightness_mode_combo.bind("<<ComboboxSelected>>", self.change_brightness_mode)
        self.brightness_mode_combo.pack()

        self.brightness_label = ttk.Label(self.window, text="Brightness: --", style="TLabel", background="#303030", foreground="white")
        self.brightness_label.pack(pady=10)

        self.brightness_preview_frame = tk.Frame(self.window, bg="#303030", width=0, height=20)
        self.brightness_preview_frame.pack()

    def check_wmi_compatibility(self):
        try:
            c = wmi.WMI(namespace='root\\wmi')
            brightness_methods = c.WmiMonitorBrightnessMethods()
            brightness = c.WmiMonitorBrightness()
            self.is_wmi_compatible = True
        except Exception as e:
            print(f"Error accessing WMI service: {e}")
            self.is_wmi_compatible = False

    def display_wmi_error(self):
        error_label = ttk.Label(self.window, text="WMI service not available on this system.", style="TLabel", background="#303030", foreground="red")
        error_label.pack(pady=10)

    def hide_wmi_error(self):
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None

    def set_brightness(self, level):
        try:
            c = wmi.WMI(namespace='wmi')
            brightness_methods = c.WmiMonitorBrightnessMethods()[0]
            brightness_methods.WmiSetBrightness(level, 0)
            return
        except Exception as e:
            print(f"WMI Error: {e}")

        try:
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            brightness_key = "ACBrightness"
            brightness = level * 255 // 100
            reg = ctypes.windll.advapi32.RegOpenKeyExW(ctypes.c_void_p(0x80000002), registry_path, 0, ctypes.c_uint32(0x20019), ctypes.pointer(ctypes.c_void_p()))
            ctypes.windll.advapi32.RegSetValueExW(reg, brightness_key, 0, ctypes.c_uint32(1), ctypes.pointer(ctypes.c_uint8(int(brightness))), 1)
            ctypes.windll.advapi32.RegCloseKey(reg)
        except Exception as e:
            print(f"Alternative Method 2 Error: {e}")

    def get_brightness(self):
        try:
            c = wmi.WMI(namespace='wmi')
            brightness = c.WmiMonitorBrightness()[0]
            return brightness.CurrentBrightness
        except Exception as e:
            print(f"Error getting brightness: {e}")
            return 0

    def update_brightness_label(self, level):
        self.brightness_label.config(text=f"Brightness: {level}%", foreground="white", background="#303030")
        self.brightness_preview_frame.config(bg="#303030", width=int(level * 2))

    def update_brightness(self, event):
        brightness_level = self.custom_brightness_slider.get()
        self.set_brightness(brightness_level)
        self.update_brightness_label(brightness_level)

    def increase_brightness(self):
        current_brightness = self.get_brightness()
        brightness_level = min(100, current_brightness + 10)
        self.set_brightness(brightness_level)
        self.update_brightness_label(brightness_level)
        self.custom_brightness_slider.set(brightness_level)

    def decrease_brightness(self):
        current_brightness = self.get_brightness()
        brightness_level = max(0, current_brightness - 10)
        self.set_brightness(brightness_level)
        self.update_brightness_label(brightness_level)
        self.custom_brightness_slider.set(brightness_level)

    def change_brightness_mode(self, event):
        mode = self.brightness_mode_combo.get()
        if mode == "Movie":
            self.set_brightness(80)
            self.update_brightness_label(80)
            self.custom_brightness_slider.set(80)
        elif mode == "Work":
            self.set_brightness(60)
            self.update_brightness_label(60)
            self.custom_brightness_slider.set(60)
        elif mode == "Gaming":
            self.set_brightness(90)
            self.update_brightness_label(90)
            self.custom_brightness_slider.set(90)
        elif mode == "Reading":
            self.set_brightness(70)
            self.update_brightness_label(70)
            self.custom_brightness_slider.set(70)
        # Add more modes here
BrightnessController()
#pyinstaller --onefile --noconsole --name=Brightness-control brightness_control.py