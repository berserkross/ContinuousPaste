import pyperclip
import pyautogui
import time
import threading
import sys
import logging
import tkinter as tk
from tkinter import messagebox, ttk

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class KeySelectionWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.selected_keys = []

        # 创建键盘按键选择窗口
        self.window = tk.Toplevel(parent)
        self.window.title("功能键选择")
        self.window.geometry("800x1000")
        self.window.resizable(True, True)

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.window, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(main_frame, text="功能键选择", font=("微软雅黑", 14, "bold"))
        title_label.pack(pady=(0, 10))

        # 指示说明
        instruction_label = tk.Label(main_frame, text="请先点击'开始选择'按钮，然后按下您需要的功能键组合，最后点击'结束选择'完成设置",
                                   font=("微软雅黑", 10), fg="gray", wraplength=550)
        instruction_label.pack(pady=(0, 15))

        # 当前选择的键显示
        selected_frame = tk.LabelFrame(main_frame, text="当前选择的键", padx=10, pady=5)
        selected_frame.pack(fill=tk.X, pady=(0, 15))

        self.selected_keys_label = tk.Label(selected_frame, text="无", font=("微软雅黑", 12), fg="blue")
        self.selected_keys_label.pack(pady=5)

        # 键盘按键网格
        keys_frame = tk.LabelFrame(main_frame, text="常用功能键", padx=10, pady=10)
        keys_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 创建按键网格
        self.create_key_buttons(keys_frame)

        # 操作按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.start_select_btn = tk.Button(button_frame, text="开始选择", command=self.start_selecting,
                                        bg="#4CAF50", fg="white", width=12)
        self.start_select_btn.pack(side=tk.LEFT, padx=5)

        self.end_select_btn = tk.Button(button_frame, text="结束选择", command=self.end_selecting,
                                      bg="#FF9800", fg="white", width=12, state=tk.DISABLED)
        self.end_select_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(button_frame, text="清空", command=self.clear_selection,
                                 bg="#f44336", fg="white", width=12)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 确认按钮
        confirm_btn = tk.Button(main_frame, text="确认选择", command=self.confirm_selection,
                              bg="#2196F3", fg="white", width=15, font=("微软雅黑", 10))
        confirm_btn.pack(pady=10)

        # 监听键盘事件
        self.listening = False
        self.window.bind('<KeyPress>', self.on_key_press)
        self.window.focus_set()

    def create_key_buttons(self, parent):
        # 定义功能键
        keys = [
            ['ctrl', 'alt', 'shift', 'win'],
            ['caps', 'esc', 'tab', 'space'],
            ['enter', 'backspace', 'delete', 'insert'],
            ['home', 'end', 'pageup', 'pagedown'],
            ['f1', 'f2', 'f3', 'f4'],
            ['f5', 'f6', 'f7', 'f8'],
            ['f9', 'f10', 'f11', 'f12'],
            ['up', 'down', 'left', 'right'],
            ['0', '1', '2', '3', '4'],
            ['5', '6', '7', '8', '9']
        ]

        for i, row in enumerate(keys):
            frame = tk.Frame(parent)
            frame.pack(fill=tk.X, pady=2)
            for j, key in enumerate(row):
                btn = tk.Button(frame, text=key.upper(), width=12, command=lambda k=key: self.add_key(k))
                btn.pack(side=tk.LEFT, padx=2, pady=2)

        # 字母键
        letter_frame = tk.Frame(parent)
        letter_frame.pack(fill=tk.X, pady=2)
        letters = "abcdefghijklmnopqrstuvwxyz"
        for i, letter in enumerate(letters):
            if i % 13 == 0:  # 每13个字母换行
                row_frame = tk.Frame(letter_frame)
                row_frame.pack(fill=tk.X)
            btn = tk.Button(row_frame, text=letter.upper(), width=4, command=lambda k=letter: self.add_key(k))
            btn.pack(side=tk.LEFT, padx=1, pady=1)

    def add_key(self, key):
        if key not in self.selected_keys:
            self.selected_keys.append(key)
            self.update_selected_display()

    def start_selecting(self):
        self.listening = True
        self.selected_keys = []
        self.update_selected_display()
        self.start_select_btn.config(state=tk.DISABLED)
        self.end_select_btn.config(state=tk.NORMAL)
        self.window.focus_set()

    def end_selecting(self):
        self.listening = False
        self.start_select_btn.config(state=tk.NORMAL)
        self.end_select_btn.config(state=tk.DISABLED)

    def on_key_press(self, event):
        if self.listening:
            key = event.keysym.lower()
            if key not in self.selected_keys:
                self.selected_keys.append(key)
                self.update_selected_display()

    def clear_selection(self):
        self.selected_keys = []
        self.update_selected_display()

    def update_selected_display(self):
        if self.selected_keys:
            display_text = " + ".join([k.upper() for k in self.selected_keys])
            self.selected_keys_label.config(text=display_text)
        else:
            self.selected_keys_label.config(text="无")

    def confirm_selection(self):
        if not self.selected_keys:
            messagebox.showwarning("警告", "请至少选择一个键")
            return
        self.callback(self.selected_keys)
        self.window.destroy()


class ContinuousPasteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("连续粘贴工具")
        self.root.geometry("500x800")
        self.root.resizable(True, True)

        # 控制变量
        self.running = False
        self.paste_thread = None

        # 参数变量
        self.interval_var = tk.StringVar(value="0.5")
        self.start_delay_var = tk.StringVar(value="3")
        self.post_paste_keys = []  # 存储粘贴后要按的键
        self.paste_method_var = tk.StringVar(value="ctrl+v")

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(main_frame, text="连续粘贴工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 设置框架
        settings_frame = tk.LabelFrame(main_frame, text="设置选项", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=5)

        # 间隔时间
        interval_frame = tk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        tk.Label(interval_frame, text="粘贴间隔(秒):", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(side=tk.LEFT, padx=(10, 0))

        # 启动延迟
        delay_frame = tk.Frame(settings_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        tk.Label(delay_frame, text="启动延迟(秒):", width=15, anchor="w").pack(side=tk.LEFT)
        tk.Entry(delay_frame, textvariable=self.start_delay_var, width=10).pack(side=tk.LEFT, padx=(10, 0))

        # 粘贴后按键设置
        post_paste_frame = tk.LabelFrame(settings_frame, text="粘贴后按键", padx=10, pady=5)
        post_paste_frame.pack(fill=tk.X, pady=10)

        self.keys_display = tk.Label(post_paste_frame, text="未设置", font=("微软雅黑", 10), fg="gray")
        self.keys_display.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(post_paste_frame, text="设置按键", command=self.open_key_selector,
                 bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT)

        # 粘贴方法选择
        method_frame = tk.Frame(settings_frame)
        method_frame.pack(fill=tk.X, pady=5)
        tk.Label(method_frame, text="粘贴方法:", width=15, anchor="w").pack(side=tk.LEFT)
        method_combo = ttk.Combobox(method_frame, textvariable=self.paste_method_var,
                                   values=["ctrl+v", "shift+insert", "右键粘贴"], state="readonly")
        method_combo.pack(side=tk.LEFT, padx=(10, 0))

        # 控制按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        self.start_btn = tk.Button(button_frame, text="开始粘贴", command=self.start_paste,
                                  bg="#4CAF50", fg="white", width=12, font=("微软雅黑", 10))
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(button_frame, text="停止粘贴", command=self.stop_paste,
                                 bg="#f44336", fg="white", width=12, font=("微软雅黑", 10), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        # 状态显示
        status_frame = tk.LabelFrame(main_frame, text="状态", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_text = tk.Text(status_frame, height=8, state=tk.DISABLED)
        scrollbar = tk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)

        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 提示信息
        tk.Label(main_frame, text="提示: 程序运行时请确保目标应用程序已准备就绪",
                fg="gray", font=("微软雅黑", 9)).pack(pady=(10, 0))

    def open_key_selector(self):
        """打开键选择窗口"""
        KeySelectionWindow(self.root, self.set_post_paste_keys)

    def set_post_paste_keys(self, keys):
        """设置粘贴后的按键"""
        self.post_paste_keys = keys
        if keys:
            display_text = " + ".join([k.upper() for k in keys])
            self.keys_display.config(text=display_text, fg="blue")
        else:
            self.keys_display.config(text="未设置", fg="gray")

    def log_message(self, message):
        """向状态框添加日志信息"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def continuous_paste_worker(self):
        """粘贴工作线程"""
        try:
            interval = float(self.interval_var.get())
        except ValueError:
            self.log_message("错误: 粘贴间隔必须是数字")
            self.running = False
            return

        try:
            start_delay = int(self.start_delay_var.get())
        except ValueError:
            self.log_message("错误: 启动延迟必须是整数")
            self.running = False
            return

        paste_method = self.paste_method_var.get()

        self.log_message(f"开始连续粘贴，间隔: {interval}秒")
        self.log_message("请切换到目标应用程序...")

        # 等待启动延迟
        time.sleep(start_delay)
        self.log_message("粘贴开始...")

        while self.running:
            try:
                clipboard_content = pyperclip.paste()

                # 防御性检查
                if clipboard_content is None or not clipboard_content.strip():
                    time.sleep(interval)
                    continue

                # 根据选择的方法进行粘贴
                if paste_method == "ctrl+v":
                    pyautogui.hotkey('ctrl', 'v')
                elif paste_method == "shift+insert":
                    pyautogui.hotkey('shift', 'insert')
                elif paste_method == "右键粘贴":
                    pyautogui.click(button='right')
                    time.sleep(0.1)  # 等待菜单出现
                    pyautogui.press('v')  # 通常右键菜单中粘贴是V键

                # 执行粘贴后的按键操作
                if self.post_paste_keys:
                    if len(self.post_paste_keys) == 1:
                        # 单个按键
                        pyautogui.press(self.post_paste_keys[0])
                    else:
                        # 组合键
                        pyautogui.hotkey(*self.post_paste_keys)

                self.log_message(f"已粘贴: {clipboard_content[:30]}{'...' if len(clipboard_content) > 30 else ''}")
                time.sleep(interval/5)  # 短暂暂停确保粘贴完成

            except ValueError:
                self.log_message("错误: 间隔时间或延迟时间设置不正确")
                break
            except Exception as e:
                self.log_message(f"粘贴操作出现异常: {e}")

            time.sleep(interval)

        self.log_message("粘贴已停止")

    def start_paste(self):
        """开始粘贴"""
        if self.running:
            return

        # 检查参数是否有效
        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                raise ValueError("间隔必须大于0")
        except ValueError:
            messagebox.showerror("错误", "粘贴间隔必须是大于0的数字")
            return

        try:
            start_delay = int(self.start_delay_var.get())
            if start_delay < 0:
                raise ValueError("延迟不能为负数")
        except ValueError:
            messagebox.showerror("错误", "启动延迟必须是非负整数")
            return

        # 检查是否有内容在剪贴板
        try:
            content = pyperclip.paste()
            if not content.strip():
                messagebox.showwarning("警告", "剪贴板为空，请先复制一些内容")
                return
        except:
            messagebox.showerror("错误", "无法访问剪贴板，请检查权限")
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.paste_thread = threading.Thread(target=self.continuous_paste_worker, daemon=True)
        self.paste_thread.start()

        self.log_message("粘贴程序已启动")

    def stop_paste(self):
        """停止粘贴"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

        self.log_message("正在停止粘贴程序...")

def main():
    root = tk.Tk()
    app = ContinuousPasteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
