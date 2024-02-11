import os
import sys
import threading
import time
import customtkinter
import keyboard
import webbrowser

from user.joy_translation import translate_txt
from io_operator.joy_rw_config import write_config


class UI:
    def translate_msg_display(self, vars):
        if vars.msg != '':
            self.SenseLabel12.configure(text = translate_txt(vars.msg))
        else:
            self.SenseLabel12.configure(text = '')
       
        
    def real_time_update_texts(self, vars):
        while vars.KeepMain:
            if self.button_r._state == customtkinter.DISABLED and vars.first_time == False:
                self.button_r.configure(state = customtkinter.NORMAL)
                self.button_r['background'] = '#*active background*'
                self.button_r.configure(text=translate_txt("Self-Calibrate (ctrl + shift + c) - release everything first"))
            
            self.translate_msg_display(vars)
                                    
            time.sleep(0.125)
        
            
    def capture_keys(self, vars):
        def on_key_event(e):
            if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl+shift+c') and vars.first_time == False:
                self.save_config(vars, from_joy=True)
                
        keyboard.hook(on_key_event)
    
    
    def reset_slider(self, slider, label, special: bool=False):
        if not special:
            slider.set(0.0)
            label.configure(text=f"{label.cget('text')[:label.cget('text').find('|')]}|  {0.0}")
        else:
            slider.set(-1.0)
            label.configure(text=f"{label.cget('text')[:label.cget('text').find('|')]}|  {-1.0}")
        
        
    def on_slider_release(self, slider, label):
        value = slider.get()
        label.configure(text=f"{label.cget('text')[:label.cget('text').find('|')]}|  {value:.5f}")
         
            
    def save_config(self, vars, from_joy: bool=False):
        if (self.entry.get()).isnumeric():
            vars.joy_id = int(self.entry.get())
            
        elif self.entry.get() == "" or self.entry.get() == " " or self.entry.get() is None:
            vars.joy_id = 1
        else:
            vars.joy_id = [int(s) for s in self.entry.get().split() if s.isdigit()][0]
        
        if not from_joy:
            context = {
                "usages": {
                    "use_l_analog": bool(self.switch_1.get()), 
                    "use_r_analog": bool(self.switch_2.get()),
                    "use_l_trigger": bool(self.switch_3.get()),
                    "use_r_trigger": bool(self.switch_4.get()),
                    "replicate_btns": bool(self.switch_5.get()),
                    "joy_id": vars.joy_id        
                },
                    
                "offsets": {
                    "l_analog_offset_x": self.slider.get(),
                    "l_analog_offset_y": self.slider1.get(),
                    "r_analog_offset_x": self.slider2.get(),
                    "r_analog_offset_y": self.slider3.get(),
                    #"l_trigger_offset": self.slider4.get(),
                    #"r_trigger_offset": self.slider5.get()
                    "l_trigger_offset": -1,
                    "r_trigger_offset": -1 
                }
            }
            vars.config = context
        else:
            context = {
                "usages": {
                    "use_l_analog": bool(self.switch_1.get()), 
                    "use_r_analog": bool(self.switch_2.get()),
                    "use_l_trigger": bool(self.switch_3.get()),
                    "use_r_trigger": bool(self.switch_4.get()),
                    "replicate_btns": bool(self.switch_5.get()),
                    "joy_id": vars.joy_id        
                },
                    
                "offsets": {
                    "l_analog_offset_x": vars.axis[0]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_x'],
                    "l_analog_offset_y": vars.axis[1]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_y'],
                    "r_analog_offset_x": vars.axis[2]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_x'],
                    "r_analog_offset_y": vars.axis[3]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_y'],
                    "l_trigger_offset": vars.axis[4] if vars.config['usages']['use_l_trigger'] else vars.config['offsets']['l_trigger_offset'],
                    "r_trigger_offset": vars.axis[5] if vars.config['usages']['use_r_trigger'] else vars.config['offsets']['r_trigger_offset']
                }
            }
            vars.config = context
            self.update_sliders(vars)
        write_config(context)


    def shutdown(self, vars):
        vars.ReadInput = False
        vars.KeepMain = False
        vars.kill_tasks_force()
        
        
    def update_sliders(self, vars):
        self.slider.set(vars.axis[0]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_x'])
        self.slider1.set(vars.axis[1]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_y'])
        self.slider2.set(vars.axis[2]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_x'])
        self.slider3.set(vars.axis[3]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_y'])
        #self.slider4.set(vars.axis[4] if vars.config['usages']['use_l_trigger'] else vars.config['offsets']['l_trigger_offset'])
        #self.slider5.set(vars.axis[5] if vars.config['usages']['use_r_trigger'] else vars.config['offsets']['r_trigger_offset'])
        
        self.SenseLabel.configure(text=f"{translate_txt('Left analog offset X')}  |  {vars.axis[0]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_x']}")
        self.SenseLabel1.configure(text=f"{translate_txt('Left analog offset Y')}  |  {vars.axis[1]*-1 if vars.config['usages']['use_l_analog'] else vars.config['offsets']['l_analog_offset_y']}")
        self.SenseLabel2.configure(text=f"{translate_txt('Right analog offset X')}  |  {vars.axis[2]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_x']}")
        self.SenseLabel3.configure(text=f"{translate_txt('Right analog offset Y')}  |  {vars.axis[3]*-1 if vars.config['usages']['use_r_analog'] else vars.config['offsets']['r_analog_offset_y']}")
        #self.SenseLabel4.configure(text=f"{translate_txt('Left trigger_offset')}  |  {vars.axis[4] if vars.config['usages']['use_l_trigger'] else vars.config['offsets']['l_trigger_offset']}")
        #self.SenseLabel5.configure(text=f"{translate_txt('Right trigger_offset')}  |  {vars.axis[5] if vars.config['usages']['use_r_trigger'] else vars.config['offsets']['r_trigger_offset']}")
        
        
    def __init__(self, vars):
        self.root = customtkinter.CTk()
        
        config_name = os.path.join('assets', 'ico')
        config_name_theme = os.path.join('assets', 'Extreme')
        
        if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
            # Executando como executable (PyInstaller)
            path = os.path.dirname(sys.executable)
        else:
            # Executando como  script .py
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
                
        icon_path = os.path.join(path, config_name, "emucon.ico")
        theme = os.path.join(path, config_name_theme, "extreme.json")
        
        #customtkinter.set_default_color_theme(theme)
        
        self.cwd =os.path.join(os.path.expanduser(os.getenv('USERPROFILE')), 'AppData', 'Local', 'Joy_Offset', 'Settings')

        self.root.title("Joy Offset")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.shutdown(vars))
        self.root.iconbitmap(icon_path)
        
        #self.app_width = int(0.33 * self.root.winfo_screenwidth())
        self.app_width = 1000
        self.app_height = int(0.89 * self.root.winfo_screenheight())
        
        self.root.resizable(0,1)
        self.root.eval('tk::PlaceWindow . center')
        self.root.geometry('%dx%d+%d+%d' % (self.app_width, self.app_height, (self.root.winfo_screenwidth() //2 - self.app_width // 2), (self.root.winfo_screenheight() // 2 - self.app_height // 2 - 48)))
        
        self.scroll_frame = customtkinter.CTkFrame(self.root)
        self.scroll_frame.pack(side="top", fill="both", expand=True)
        
        self.title = customtkinter.CTkLabel(master = self.scroll_frame, text = "Joy Offset", font = ("Roboto", 22))
        self.title.pack(pady=(20,0), padx=0)
        
        self.frameA = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frameA.pack(pady=(20,0), padx=60, fill="x", expand=True)
        
        self.entry = customtkinter.CTkEntry(master = self.frameA, placeholder_text = f"Joystick ID {vars.joy_id}", justify="center")
        self.entry.pack(pady=12, padx=(10), fill="x")
        self.entry.configure(textvariable = f"{vars.joy_id}")
        
        self.frame = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame.pack(pady=(20,0), padx=60, fill="x", expand=True)
        
        self.switch1_var = customtkinter.IntVar(value = vars.config['usages']['use_l_analog'])
        self.switch_1 = customtkinter.CTkSwitch(master=self.frame, text=translate_txt("Use left analog"),  onvalue=1, offvalue=0, variable = self.switch1_var)
        self.switch_1.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch2_var = customtkinter.IntVar(value = vars.config['usages']['use_r_analog'])
        self.switch_2 = customtkinter.CTkSwitch(master=self.frame, text=translate_txt("Use right analog"),  onvalue=1, offvalue=0, variable = self.switch2_var)
        self.switch_2.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch3_var = customtkinter.IntVar(value = vars.config['usages']['use_l_trigger'])
        self.switch_3 = customtkinter.CTkSwitch(master=self.frame, text=translate_txt("Use left trigger"),  onvalue=1, offvalue=0, variable = self.switch3_var)
        self.switch_3.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch4_var = customtkinter.IntVar(value = vars.config['usages']['use_r_trigger'])
        self.switch_4 = customtkinter.CTkSwitch(master=self.frame, text=translate_txt("Use right trigger"),  onvalue=1, offvalue=0, variable = self.switch4_var)
        self.switch_4.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch5_var = customtkinter.IntVar(value = vars.config['usages']['replicate_btns'])
        self.switch_5 = customtkinter.CTkSwitch(master=self.frame, text=translate_txt("Replicate buttons"),  onvalue=1, offvalue=0, variable = self.switch5_var)
        self.switch_5.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.frame3 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame3.pack(pady=(20,0),  padx=60, fill="x", expand=True)
        
        self.slider = customtkinter.CTkSlider(master=self.frame3, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider.set(vars.config['offsets']['l_analog_offset_x'])
        
        self.SenseLabel = customtkinter.CTkLabel(master = self.frame3, text=f"{translate_txt('Left analog offset X')}  |  {vars.config['offsets']['l_analog_offset_x']:.5f}", font = ("Roboto", 14))
        self.SenseLabel.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_0 = customtkinter.CTkButton(master=self.frame3, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider, self.SenseLabel))
        self.button_0.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider, self.SenseLabel))
        
        self.frame4 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame4.pack(pady=(0,0),  padx=60, fill="x", expand=True)
        
        self.slider1 = customtkinter.CTkSlider(master=self.frame4, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider1.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider1.set(vars.config['offsets']['l_analog_offset_y'])
        
        self.SenseLabel1 = customtkinter.CTkLabel(master = self.frame4, text=f"{translate_txt('Left analog offset Y')}  |  {vars.config['offsets']['l_analog_offset_y']:.5f}", font = ("Roboto", 14))
        self.SenseLabel1.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_1 = customtkinter.CTkButton(master=self.frame4, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider1, self.SenseLabel1))
        self.button_1.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider1.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider1, self.SenseLabel1))
        
        self.frame5 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame5.pack(pady=(20,0),  padx=60, fill="x", expand=True)
        
        self.slider2 = customtkinter.CTkSlider(master=self.frame5, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider2.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider2.set(vars.config['offsets']['r_analog_offset_x'])
        
        self.SenseLabel2 = customtkinter.CTkLabel(master = self.frame5, text=f"{translate_txt('Right analog offset X')}  |  {vars.config['offsets']['r_analog_offset_x']:.5f}", font = ("Roboto", 14))
        self.SenseLabel2.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_2 = customtkinter.CTkButton(master=self.frame5, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider2, self.SenseLabel2))
        self.button_2.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider2.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider2, self.SenseLabel2))
        
        self.frame6 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame6.pack(pady=(0,0),  padx=60, fill="x", expand=True)
        
        self.slider3 = customtkinter.CTkSlider(master=self.frame6, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider3.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider3.set(vars.config['offsets']['r_analog_offset_y'])
        
        self.SenseLabel3 = customtkinter.CTkLabel(master = self.frame6, text=f"{translate_txt('Right analog offset Y')}  |  {vars.config['offsets']['r_analog_offset_y']:.5f}", font = ("Roboto", 14))
        self.SenseLabel3.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_3 = customtkinter.CTkButton(master=self.frame6, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider3, self.SenseLabel3))
        self.button_3.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider3.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider3, self.SenseLabel3))
        
        '''self.frame7 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame7.pack(pady=(20,0),  padx=60, fill="x", expand=True)
        
        self.slider4 = customtkinter.CTkSlider(master=self.frame7, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider4.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider4.set(vars.config['offsets']['l_trigger_offset'])
        
        self.SenseLabel4 = customtkinter.CTkLabel(master = self.frame7, text=f"{translate_txt('Left trigger_offset')}  |  {vars.config['offsets']['l_trigger_offset']:.5f}", font = ("Roboto", 14))
        self.SenseLabel4.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_4 = customtkinter.CTkButton(master=self.frame7, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider4, self.SenseLabel4, special=True))
        self.button_4.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider4.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider4, self.SenseLabel4))
        
        self.frame8 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame8.pack(pady=(0,0),  padx=60, fill="x", expand=True)
        
        self.slider5 = customtkinter.CTkSlider(master=self.frame8, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider5.pack(pady=1, padx=(1,6), fill="x", expand=True, side = "left")
        self.slider5.set(vars.config['offsets']['r_trigger_offset'])
        
        self.SenseLabel5 = customtkinter.CTkLabel(master = self.frame8, text=f"{translate_txt('Right trigger_offset')}  |  {vars.config['offsets']['r_trigger_offset']:.5f}", font = ("Roboto", 14))
        self.SenseLabel5.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_5 = customtkinter.CTkButton(master=self.frame8, border_width=0, corner_radius=8, text=translate_txt('Reset'), width=360, command = lambda: self.reset_slider(self.slider5, self.SenseLabel5, special=True))
        self.button_5.pack(pady=0, padx=(6,6), side = "right", fill='x')
        
        self.slider5.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider5, self.SenseLabel5))'''
        
        self.frame9 = customtkinter.CTkFrame(master=self.scroll_frame)
        self.frame9.pack(pady=(20,60),  padx=60, fill="x", expand=True, side="bottom")
        
        self.SenseLabel12 = customtkinter.CTkLabel(master = self.scroll_frame, text = vars.msg,font = ("Roboto", 16))
        self.SenseLabel12.pack(pady=20, padx=(6,1), side = "top")
            
        self.button_x = customtkinter.CTkButton(master=self.frame9, border_width=0, corner_radius=8, text=translate_txt('Settings Folder'), command = lambda: os.startfile(self.cwd))
        self.button_x.pack(pady=6, padx=60, side = "left", expand = True, fill='x')
        
        self.button = customtkinter.CTkButton(master=self.frame9, border_width=0, corner_radius=8, text=translate_txt('Save'), command = lambda: self.save_config(vars))
        self.button.pack(pady=6, padx=60, side = "bottom", expand = True, fill='x')
        
        self.button_r = customtkinter.CTkButton(master=self.frame9, border_width=0, corner_radius=8, text=translate_txt('To activate self-calibration, press any joystick key'), command = lambda: self.save_config(vars, from_joy=True))
        self.button_r.pack(pady=6, padx=0, side = "right", expand = True)
        self.button_r.configure(state = customtkinter.DISABLED)
        self.button_r['background'] = '#*disabled background*'
        
        self.button_code = customtkinter.CTkButton(master=self.frame9, border_width=0, corner_radius=8, width=250, text=translate_txt('Source Code'), command = lambda: webbrowser.open("https://github.com/Suundumused/Joystick-drifting-fix"))
        self.button_code.pack(pady=8, padx=0, side = "bottom", expand = True)
        
        thread3 = threading.Thread(target = self.real_time_update_texts, args=(vars, ))
        thread3.daemon = True
        thread3.start()
        
        thread4 = threading.Thread(target = self.capture_keys, args=(vars, ))
        thread4.daemon = True
        thread4.start()
                
        self.root.mainloop()