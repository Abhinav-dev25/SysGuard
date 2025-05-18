import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time
import os

class SysGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SysGuard")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(pady=10)

        self.monitoring = False

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(root, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.sandbox_button = tk.Button(root, text="Launch Sandboxed Bash", command=self.launch_sandbox)
        self.sandbox_button.pack(side=tk.LEFT, padx=10)

    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_processes)
            self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False

    def clear_log(self):
        self.text_area.delete('1.0', tk.END)

    def launch_sandbox(self):
        subprocess.Popen(["python3", "sandbox.py", "/bin/bash"])

    def monitor_processes(self):
        while self.monitoring:
            try:
                output = subprocess.check_output(["ps", "aux"], universal_newlines=True)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, output)
                time.sleep(5)
            except Exception as e:
                self.text_area.insert(tk.END, f"Error: {e}\n")
                time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SysGuardApp(root)
    root.mainloop()
