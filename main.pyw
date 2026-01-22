import os
import json

import tkinter as tk
import pygame

from tkinter import ttk


class App:
    def __init__(self, root):
        # main config
        self.root = root
        self.root.title("App")
        self.root.geometry("700x400")  
        self.root.resizable(width=0, height=0)
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)  
        main_frame.rowconfigure(1, weight=0)
        
        self.presets = []
        self.volumes = [0,0,0,0]
        self.sliders = []
        self.slider_labels = []
        self.volume_names = ["Music", "Rain", "Fire", "Clock"]
        self.__start_sounds()

        # choose presets
        preset_frame = ttk.Frame(main_frame)
        preset_frame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E), padx=(20, 0), pady=10)
        ttk.Label(preset_frame, text="Preset:", font=('Arial', 10)).pack(anchor=tk.W)
        self.selected_preset = tk.StringVar()
        self.preset_dropdown = ttk.Combobox(
            preset_frame,
            textvariable=self.selected_preset,
            state="readonly",
            width=20
        )
        self.preset_dropdown.pack(pady=(5, 0))
        self.preset_dropdown['values'] = self.__preset_names()
        self.preset_dropdown.current(0)
        self.preset_dropdown.bind("<<ComboboxSelected>>", 
        lambda event: self.__load_preset(self.preset_dropdown.get()))

        # sliders
        sliders_frame = ttk.Frame(main_frame)
        sliders_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        for col in range(4):
            sliders_frame.columnconfigure(col, weight=1)
            column_frame = ttk.Frame(sliders_frame)
            column_frame.grid(row=0, column=col, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
            value_label = ttk.Label(column_frame, text="50%", font=('Arial', 12))
            value_label.pack(pady=(0, 10))
            self.slider_labels.append(value_label)
            
            slider = ttk.Scale(
                column_frame,
                from_=0,
                to=100,
                value=100-self.volumes[col],
                orient=tk.VERTICAL,
                length=200,
                command=lambda val, idx=col: self.__update_percent(100-float(val), idx)
            )
            slider.pack(expand=True, fill=tk.Y, pady=(0, 10))
            self.sliders.append(slider)
            button = ttk.Button(
                column_frame,
                text=f"{self.volume_names[col]}"
            )
            button.pack()
        
        # timer progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate',
            maximum=100,
            value=50
        )
        self.progress_bar.pack(fill=tk.X, expand=True)
        self.progress_label = ttk.Label(progress_frame, text="Progress: 50%")
        self.progress_label.pack(pady=(5, 0))

        # loading last preset
        with open("./presets/last_used.txt", "r", encoding="utf-8") as f:
            last_used_preset = f.read()
            self.preset_dropdown.set(last_used_preset)
            self.__load_preset(last_used_preset)

    def __update_sliders(self):
        for i in range(4):
            self.sliders[i].set(100-self.volumes[i])
    
    def __load_preset(self, name: str) -> list:
        with open(f"./presets/presets.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            try:
                self.volumes = data[name]["volumes"]
                self.__update_sliders()
                with open("./presets/last_used.txt", "w", encoding="utf-8") as f:
                    f.write(name)
            except:
                self.volumes = [50,50,50,50]

    def __preset_names(self):
        with open(f"./presets/presets.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            return [i for i in data]

    def __update_sounds(self):
        for i in range(len(self.sounds)):
            self.sounds[i].set_volume(self.volumes[i]/100)
    
    def __start_sounds(self):
        pygame.init()
        pygame.mixer.init()
        self.sounds = [pygame.mixer.Sound(f"./sounds/{i}.mp3") for i in range(4)]
        for i in range(4):
            self.sounds[i].set_volume(self.volumes[i]/100)
            self.sounds[i].play(loops=-1)

    def __update_percent(self, val: int, idx: int):
        self.slider_labels[idx].config(text=f"{val:.0f}%")
        self.volumes[idx] = val
        self.__update_sounds()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()