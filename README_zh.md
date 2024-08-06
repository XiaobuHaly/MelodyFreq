MelodyFreq



简介
MelodyFreq 是一个简单的音符频率计算器和音频播放工具。可以输入音符（例如 C4, Db6 等），程序将计算出该音符的频率，并可以播放该频率的声音。还可以自定义音量和播放持续时间。


功能
1.计算音符的频率
2.播放指定频率的声音
3.自定义音量和播放持续时间


安装

克隆此仓库：
git clone https://github.com/yourusername/MelodyFreq.git
cd MelodyFreq

安装依赖：
pip install numpy sounddevice
pip install tkinter
pip install ctypes
pip install sounddevice


使用

运行主程序：
MelodyFreq.py
输入音符（例如 C4, Db6 等）并按回车键计算频率。
输入音量（0 到 1 之间）和持续时间（秒）。
点击“播放声音”按钮播放声音。

文件结构
MelodyFreq.py：主程序文件
config.py：配置文件，包含常量和音符映射


贡献
欢迎贡献代码！请 fork 此仓库并提交分支请求。