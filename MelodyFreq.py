import tkinter as tk
from tkinter import messagebox
import ctypes
import numpy as np
import sounddevice as sd
from config import A4_FREQ, NOTE_OFFSETS

def get_frequency(note):
    if len(note) == 2:
        note_name, octave = note[0], note[1]
    elif len(note) == 3:
        note_name, octave = note[:2], note[2]
    else:
        raise ValueError("音符格式不正确")

    if note_name not in NOTE_OFFSETS:
        raise KeyError("音符名称不正确")

    try:
        octave = int(octave)
    except ValueError:
        raise ValueError("八度必须是数字")

    semitone_offset = NOTE_OFFSETS[note_name] + (octave - 4) * 12
    frequency = A4_FREQ * (2 ** (semitone_offset / 12.0))
    return frequency

def calculate_frequency(event=None):
    note = entry.get().strip()
    try:
        global current_frequency
        current_frequency = get_frequency(note)
        result_label.config(text=f"{note}的频率是 {current_frequency:.2f} Hz")
    except KeyError as e:
        messagebox.showerror("错误", f"输入的音符名称不正确：{e}")
    except ValueError as e:
        messagebox.showerror("错误", f"输入的八度不正确或音符格式不正确：{e}")

def play_sound():
    if current_frequency is None:
        messagebox.showerror("错误", "请先计算频率。")
        return

    try:
        duration = float(duration_entry.get().strip())
        volume = float(volume_entry.get().strip())
    except ValueError:
        messagebox.showerror("错误", "请确保音量和持续时间是有效的数字。")
        return

    if not (1 <= volume <= 100):
        messagebox.showerror("错误", "音量必须在1到100之间。")
        return
    volume = volume / 100

    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = volume * np.sin(2 * np.pi * current_frequency * t)

    sd.play(wave, sample_rate)
    sd.wait()

def quit_program():
    root.quit()

def enable_blur_effect(hwnd):
    accent_policy = ctypes.c_int(3)
    accent_struct_size = ctypes.sizeof(ctypes.c_int)
    data = ctypes.c_buffer(accent_struct_size)
    ctypes.memmove(data, ctypes.byref(accent_policy), accent_struct_size)
    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, data)

# 创建主窗口
root = tk.Tk()
root.title("音符频率计算器")

current_frequency = None

# 获取窗口句柄并启用毛玻璃效果
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
enable_blur_effect(hwnd)

prompt_label = tk.Label(root, text="请输入音符（例如C4, Db6等）：")
prompt_label.pack(pady=10)

entry = tk.Entry(root, font=('Arial', 14), justify='center')
entry.pack(ipadx=20, ipady=5, padx=10, pady=10)
entry.bind('<Return>', calculate_frequency)

result_label = tk.Label(root, text="", font=('Arial', 14))
result_label.pack(pady=10)

control_frame = tk.Frame(root)
control_frame.pack(fill='x', pady=10)

tk.Label(control_frame, text="音量（1到100之间）：").grid(row=0, column=0, padx=5)
volume_entry = tk.Entry(control_frame, font=('Arial', 14), justify='center')
volume_entry.grid(row=0, column=1, padx=5)

tk.Label(control_frame, text="持续时间（秒）：").grid(row=1, column=0, padx=5)
duration_entry = tk.Entry(control_frame, font=('Arial', 14), justify='center')
duration_entry.grid(row=1, column=1, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(fill='x', pady=10)

calculate_button = tk.Button(button_frame, text="计算频率", command=calculate_frequency)
calculate_button.grid(row=0, column=0, padx=10)

play_button = tk.Button(button_frame, text="播放声音", command=play_sound)
play_button.grid(row=0, column=1, padx=10)

quit_button = tk.Button(button_frame, text="退出程序", command=quit_program)
quit_button.grid(row=0, column=2, padx=10)

button_frame.grid_columnconfigure(1, weight=1)

root.mainloop()
