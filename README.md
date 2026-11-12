# ContinuousPaste

Windows/macOS/Linux 桌面小工具：按设定间隔循环把剪贴板内容粘贴到当前焦点窗口，支持“粘贴后再按组合键/单键”（如回车、Tab、Ctrl+S）。适合批量填表、重复提交文本、自动化录入演示。

## Features
- 图形界面（Tkinter）：设置粘贴间隔、启动延迟、粘贴方式、粘贴后按键
- 粘贴方式三选一：Ctrl+V / Shift+Insert / 右键菜单粘贴
- 粘贴后按键：通过弹窗可视化选择功能键，支持单键（Enter/Tab/…）或组合键（Ctrl+Enter 等）
- 启动前倒计时/延迟，给人工切换到目标窗口留出时间
- 后台线程执行粘贴，界面不卡；状态框实时日志
- 剪贴板空内容自动跳过，避免空粘贴

## Requirements
- Python 3.8+（建议 3.10/3.11/3.12，未在全版本测试）
- pyperclip（读剪贴板）
- pyautogui（发送粘贴热键/后处理按键）
- Tkinter（标准库；Linux 可能需单独装 python3-tk）

## Install
git clone https://github.com/berserkross/ContinuousPaste.git
cd ContinuousPaste
pip install pyperclip pyautogui
# Tkinter：Windows/macOS 通常随 Python 自带；Ubuntu/Debian 补 sudo apt install python3-tk

## Usage
python ContinuousPaste.py

1. 先复制要重复粘贴的文本到剪贴板
2. 间隔填 0.5~若干秒，启动延迟填 3~5 秒（用于切到目标窗口）
3. 粘贴方式选 Ctrl+V / Shift+Insert / 右键粘贴
4. 如需“粘完按回车”：点“设置按键”→选 Enter→确认；组合键可依次点 Ctrl、Enter
5. 点“开始粘贴”，切到目标输入框；点“停止粘贴”结束

## Platform notes
- Windows：普通窗口直接跑；若目标窗口是管理员权限（如任务管理器），用管理员 CMD/IDE 启动本工具。pyautogui 模拟输入可能受 UAC 与目标权限影响。
- macOS：系统设置→隐私与安全性→辅助功能，授权运行脚本的 Python/终端/IDE；截图类才需要屏幕录制，本工具纯粘贴主要开辅助功能。pyautogui 在 macOS 通常还需 PyObjC。
- Linux：X11 下较稳，需 python3-tk；Wayland 下鼠标/键盘注入可能受限，建议切 X11。scrot/xlib 按需补：sudo apt install python3-tk scrot python3-xlib。
- 中文/非ASCII文本：本工具走剪贴板+粘贴热键，不依赖 typewrite，避免输入法问题。
- 安全：pyautogui 可设 FAILSAFE；本工具虽未强制开启，跑自动粘贴时人不要离开，失控可手动关程序。

## Use cases
批量表单录入、问卷/工单重复提交原型、教学演示“自动化粘贴”、配合其他工具做数据录入 pipeline 的初级环节。

## Known limitations
- 依赖当前焦点窗口，坐标不固定；切换窗口会改变粘贴目标
- 不校验目标应用是否允许粘贴（部分沙箱/远程桌面会拦）
- 未做“按行换内容”或“从文件逐条读取”，当前只循环粘贴同一剪贴板内容
