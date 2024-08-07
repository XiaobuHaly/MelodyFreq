import tkinter as tk
from tkinter import messagebox
import numpy as np
import sounddevice as sd
from config import A4_FREQ, NOTE_OFFSETS

# 常量定义
SAMPLE_RATE = 44100
DEFAULT_VOLUME = 50
DEFAULT_DURATION = 1.0

class NoteFrequencyCalculator:
    def __init__(self):
        # 初始化当前频率
        self.current_frequency = None

    def get_note_frequency(self, note):
        # 解析音符和八度
        if len(note) == 2:
            note_name, octave = note[0], note[1]
        elif len(note) == 3:
            note_name, octave = note[:2], note[2]
        else:
            raise ValueError("音符格式不正确")

        # 检查音符名称有效性
        if note_name not in NOTE_OFFSETS:
            raise KeyError("音符名称不正确")

        # 转换八度为整数
        try:
            octave = int(octave)
        except ValueError:
            raise ValueError("八度必须是数字")

        # 计算频率
        semitone_offset = NOTE_OFFSETS[note_name] + (octave - 4) * 12
        frequency = A4_FREQ * (2 ** (semitone_offset / 12.0))
        return frequency

    def calculate_note_frequency(self, note):
        # 计算频率并存储
        try:
            self.current_frequency = self.get_note_frequency(note)
            return f"{note}的频率是 {self.current_frequency:.2f} Hz"
        except KeyError as e:
            raise ValueError(f"输入的音符名称不正确：{e}")
        except ValueError as e:
            raise ValueError(f"输入的八度不正确或音符格式不正确：{e}")

    def play_sound(self, duration, volume):
        # 检查频率是否已计算
        if self.current_frequency is None:
            raise RuntimeError("请先计算频率。")

        # 验证音量范围
        if not (1 <= volume <= 100):
            raise ValueError("音量必须在1到100之间。")
        
        # 生成音频波形
        volume = volume / 100
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = volume * np.sin(2 * np.pi * self.current_frequency * t)

        # 播放音频
        try:
            sd.play(wave, SAMPLE_RATE)
            sd.wait()
        except Exception as e:
            raise RuntimeError(f"播放声音时出错：{e}")

def main():
    calculator = NoteFrequencyCalculator()

    def on_calculate():
        # 获取输入并计算频率
        note = entry.get().strip()
        try:
            result = calculator.calculate_note_frequency(note)
            result_label.config(text=result)
        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def on_play():
        # 播放计算的音符声音
        try:
            duration = float(duration_entry.get().strip() or DEFAULT_DURATION)
            volume = float(volume_entry.get().strip() or DEFAULT_VOLUME)
            calculator.play_sound(duration, volume)
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("错误", str(e))

    def on_quit():
        # 退出程序
        root.quit()

    # 创建主窗口
    root = tk.Tk()
    root.title("音符频率计算器")

    # 输入提示标签
    prompt_label = tk.Label(root, text="请输入音符（例如C4, Db6等）：")
    prompt_label.pack(pady=10)

    # 输入框
    entry = tk.Entry(root, font=('Arial', 14), justify='center')
    entry.pack(ipadx=20, ipady=5, padx=10, pady=10)
    entry.bind('<Return>', lambda _: on_calculate())

    # 结果显示标签
    result_label = tk.Label(root, text="", font=('Arial', 14))
    result_label.pack(pady=10)

    # 控制框架
    control_frame = tk.Frame(root)
    control_frame.pack(fill='x', pady=10)

    # 音量输入
    tk.Label(control_frame, text="音量（1到100之间）：").grid(row=0, column=0, padx=5)
    volume_entry = tk.Entry(control_frame, font=('Arial', 14), justify='center')
    volume_entry.grid(row=0, column=1, padx=5)
    volume_entry.insert(0, str(DEFAULT_VOLUME))

    # 持续时间输入
    tk.Label(control_frame, text="持续时间（秒）：").grid(row=1, column=0, padx=5)
    duration_entry = tk.Entry(control_frame, font=('Arial', 14), justify='center')
    duration_entry.grid(row=1, column=1, padx=5)
    duration_entry.insert(0, str(DEFAULT_DURATION))

    # 按钮框架
    button_frame = tk.Frame(root)
    button_frame.pack(fill='x', pady=10)

    # 按钮定义
    calculate_button = tk.Button(button_frame, text="计算频率", command=on_calculate)
    calculate_button.grid(row=0, column=0, padx=10)

    play_button = tk.Button(button_frame, text="播放声音", command=on_play)
    play_button.grid(row=0, column=1, padx=10)

    quit_button = tk.Button(button_frame, text="退出程序", command=on_quit)
    quit_button.grid(row=0, column=2, padx=10)

    button_frame.grid_columnconfigure(1, weight=1)

    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
