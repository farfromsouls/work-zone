import json
import tkinter as tk
import pygame
from tkinter import ttk


class App:
    def __init__(self, root):
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
        self.tasks = {}
        self.task_widgets = []
        self.slider_labels = []
        self.time = 0
        self.volume_names = ["Music", "Rain", "Fire", "Clock"]
        self.__start_sounds()

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

        sliders_frame = ttk.Frame(main_frame)
        sliders_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        for col in range(4):
            sliders_frame.columnconfigure(col, weight=1)
            column_frame = ttk.Frame(sliders_frame)
            column_frame.grid(row=0, column=col, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
            value_label = ttk.Label(column_frame, text=self.volumes[col], font=('Arial', 12))
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
            
        input_frame = ttk.Frame(preset_frame)
        input_frame.pack(pady=(10, 0), fill=tk.X)
        
        self.text_input = ttk.Entry(input_frame)
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.add_button = ttk.Button(input_frame, text="Create task", 
                                     command=self.__create_task)
        self.add_button.pack(side=tk.RIGHT)
        
        self.tasks_frame = ttk.LabelFrame(preset_frame, text="Tasks", padding="10")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.__update_tasks_display()
        
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
        
        timer_frame = ttk.Frame(main_frame)
        timer_frame.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        timer_button = ttk.Button(timer_frame, text="Start timer", 
                                     command=self.__start_timer)
        timer_button.pack(side=tk.RIGHT)
        timer_label = ttk.Label(timer_frame, text=f"Осталось: {self.time}", font=('Arial', 12))
        timer_label.pack(pady=(0, 10))
    
        with open("./presets/last_used.txt", "r", encoding="utf-8") as f:
            last_used_preset = f.read()
            self.preset_dropdown.set(last_used_preset)
            self.__load_preset(last_used_preset)
            
    def __start_timer():
        pass
            
    def __create_task(self):
        task_text = self.text_input.get().strip()
        if task_text:
            self.tasks[task_text] = False
            self.text_input.delete(0, tk.END)
            self.__update_tasks_display()
    
    def __update_tasks_display(self):
        for widget in self.task_widgets:
            widget.destroy()
        self.task_widgets.clear()
        
        for i, (task_text, task_completed) in enumerate(self.tasks.items()):
            task_frame = ttk.Frame(self.tasks_frame)
            task_frame.pack(fill=tk.X, pady=2)
            
            check_var = tk.BooleanVar(value=task_completed)
            
            check_var.trace_add("write", lambda *args, var=check_var, text=task_text: 
                                self.tasks.update({text: var.get()}))
            
            checkbutton = tk.Checkbutton(
                task_frame,
                variable=check_var
            )
            checkbutton.pack(side=tk.LEFT, padx=(0, 5))
            
            task_label = ttk.Label(task_frame, text=task_text, font=('Arial', 10))
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            delete_btn = ttk.Button(task_frame, text="×", width=3,
                                   command=lambda text=task_text: self.__delete_task(text))
            delete_btn.pack(side=tk.RIGHT)
            
            self.task_widgets.append(task_frame)

    def __delete_task(self, task_text):
        if task_text in self.tasks:
            del self.tasks[task_text]
            self.__update_tasks_display()

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
                self.volumes = [0,0,0,0]

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