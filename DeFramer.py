import subprocess
import sys
import os
from bs4 import BeautifulSoup
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
import webbrowser

def install_requirements():
    """Install the packages from requirements.txt."""
    if not os.path.exists('requirements.txt'):
        print("requirements.txt file is missing!")
        return

    # Run pip to install the packages from requirements.txt
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Install required packages when the script starts
install_requirements()

def open_link(event):
    webbrowser.open("https://buymeacoffee.com/javisek")

def remove_framer_badge(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated_content = content.replace('<div id="__framer-badge-container"></div>', '')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        messagebox.showinfo("Success", f"The badge div has been removed from {os.path.basename(file_path)}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def reorganize_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            input_html = file.read()
        
        # Remove comments of the format <!-- TEXT -->
        input_html = remove_comments(input_html)
        
        # Parse the HTML content
        soup = BeautifulSoup(input_html, "html.parser")
        
        # Extract style tags (CSS) and store them separately
        styles = soup.find_all("style")
        css_content = "\n".join([style.string or "" for style in styles])
        for style in styles:
            style.extract()  # Remove CSS from the original HTML
        
        # Extract the remaining HTML
        html_content = soup.prettify()
        
        # Combine HTML at the top and CSS at the bottom
        reorganized_content = f"{html_content}\n\n<!-- CSS Section -->\n<style>\n{css_content}\n</style>"
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(reorganized_content)

        messagebox.showinfo("Success", f"The HTML has been reorganized in {os.path.basename(file_path)}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reorganizing HTML: {e}")

def remove_comments(html_content):
    """Remove HTML comments (<!-- COMMENT -->) and replace them with a blank line."""
    import re
    # Remove comments using regex, replace with a newline or space
    html_content = re.sub(r'<!--.*?-->', '\n', html_content, flags=re.DOTALL)
    return html_content

def on_drop(event):
    file_path = event.data.strip()
    if os.path.exists(file_path) and file_path.endswith('.html'):
        remove_framer_badge(file_path)
        reorganize_html(file_path)
    else:
        messagebox.showerror("Error", "Invalid file. Please drag and drop a valid .html file.")

def create_gui():
    root = TkinterDnD.Tk()
    root.title("deFramer + Reorganizer")
    root.geometry("850x650")
    root.resizable(False, False)
    root.configure(bg="#212121")

    header = tk.Label(
        root,
        text="deFramer + Reorganizer Tool By Javaseq",
        font=("Arial", 16, "bold"),
        bg="#212121",
        fg="#F5F5F5",
        pady=60
    )
    header.pack()

    instruction = tk.Label(
        root,
        text="DROP your .html file",
        font=("Arial", 12),
        bg="#212121",
        fg="#888888",
    )
    instruction.pack(pady=25)

    drop_area = tk.Label(
        root,
        text="DROP FILE HERE",
        font=("Arial", 14, "bold"),
        bg="#151515",
        fg="#888888",
        width=30,
        height=5,
        relief="groove",
        bd=0
    )
    drop_area.pack(pady=20)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", on_drop)

    footer = tk.Label(
        root,
        text="❤️ DONATE ❤️",
        font=("Arial", 10),
        bg="#2E3440",
        fg="#81A1C1",
        cursor="hand2"
    )
    footer.pack(side=tk.BOTTOM, pady=10)
    footer.bind("<Button-1>", open_link)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
