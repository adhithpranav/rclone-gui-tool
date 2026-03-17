import tkinter as tk
from tkinter import TRUE, scrolledtext
import subprocess
import threading


def configure_rclone():
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Starting automated rclone setup...\nFollow browser login.\n\n")

    process = subprocess.Popen(["./rclone.exe", "config"], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

    inputs = [
        "n\n",
        "gdrive_demo\n",
        "drive\n",
        "\n",
        "\n",
        "1\n",
        "\n"
        "\n"
        "n\n"
        "y\n"
        "n\n"
        "y\n"
        "q\n"

    ]

    for i in inputs:
        process.stdin.write(i)
        process.stdin.flush()

    stdout, stderr = process.communicate()

    output_box.insert(tk.END, stdout if stdout else stderr)


def check_rclone():
    result = subprocess.run(["./rclone.exe", "listremotes"],
                            capture_output=True, text=True)
    return result.stdout




def list_files():
    remote = entry.get()
    command = ["rclone", "lsf", f"{remote}:"]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="ignore")
   
    output_box.delete(1.0, tk.END)

    output = result.stdout if result.stdout else result.stderr
    output_box.insert(tk.END, output)

def download_files():
    def task():
        remote = entry.get()
        command = ["./rclone.exe", "copy", f"{remote}:", "./dump", "--progress"]

        try:
            output_box.delete(1.0, tk.END)
        except:
            return

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        for line in process.stdout:
            try:
                output_box.insert(tk.END, line)
                output_box.see(tk.END)
            except:
                break

        process.wait()

        try:
            output_box.insert(tk.END, "\nDownload Finished!\n")
        except:
            pass

    # 👇 THIS is the important part
    threading.Thread(target=task).start()

root = tk.Tk()
root.title("Cloud Extractor Tool")

tk.Label(root, text="Remote Name:").pack()

entry = tk.Entry(root)
entry.insert(0, "gdrive_demo")
entry.pack()

tk.Button(root, text="Configure rclone", command=configure_rclone).pack()
tk.Button(root, text="List Files", command=list_files).pack()
tk.Button(root, text="Download Files", command=download_files).pack()

output_box = scrolledtext.ScrolledText(root, width=60, height=20)
output_box.pack()

root.mainloop()
   