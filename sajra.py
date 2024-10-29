import os
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import time

# Configure the appearance of customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DirectoryExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iziSajra directory Extractor")
        self.root.geometry("900x700")

        # Create a main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Directory Extractor",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 5))

        # Include Hidden Files Checkbox
        self.include_hidden_var = tk.BooleanVar(value=False)
        self.include_hidden_checkbox = ctk.CTkCheckBox(
            self.main_frame,
            text="Include Hidden Files and Directories",
            variable=self.include_hidden_var
        )
        self.include_hidden_checkbox.pack(pady=5)

        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Browse button
        self.browse_button = ctk.CTkButton(
            self.button_frame, text="Browse", command=self.browse_directory, width=120
        )
        self.browse_button.grid(row=0, column=0, padx=10)

        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame, text="Clear", command=self.clear_text, width=120
        )
        self.clear_button.grid(row=0, column=1, padx=10)

        # Save button
        self.save_button = ctk.CTkButton(
            self.button_frame, text="Save as TXT", command=self.save_as_txt, width=120
        )
        self.save_button.grid(row=0, column=2, padx=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(pady=(5, 10), fill="x", padx=20)
        self.progress_bar.set(0)

        # Textbox for output
        self.textbox = ctk.CTkTextbox(self.main_frame, wrap="word")
        self.textbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.textbox.configure(font=("Arial", 12))

        # Keyboard shortcuts
        self.textbox.bind("<Control-c>", self.copy_text)
        self.textbox.bind("<Control-x>", self.cut_text)
        self.textbox.bind("<Control-v>", self.paste_text)
        self.textbox.bind("<Control-a>", self.select_all)

        # Flag to control progress bar animation
        self.progress_bar_running = False

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            # Start the progress bar animation
            self.progress_bar_running = True
            threading.Thread(target=self.animate_progress_bar, daemon=True).start()
            # Disable buttons during processing
            self.toggle_buttons("disable")
            # Start a new thread to process directory extraction
            threading.Thread(target=self.extract_directory_data, args=(directory,), daemon=True).start()

    def animate_progress_bar(self):
        while self.progress_bar_running:
            for value in range(100):
                if not self.progress_bar_running:
                    break
                self.progress_bar.set(value / 100)
                time.sleep(0.01)
        self.progress_bar.set(0)

    def extract_directory_data(self, directory):
        try:
            output_text = f"DIRECTORY STRUCTURE\n{directory}\n\n"
            output_text += self.get_directory_tree(directory)
            output_text += "\nFILES :\n____\n"

            for root, dirs, files in os.walk(directory):
                if not self.include_hidden_var.get():
                    # Modify dirs in-place to skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    # Filter out hidden files
                    files = [f for f in files if not f.startswith('.')]
                for filename in files:
                    if not self.include_hidden_var.get() and filename.startswith('.'):
                        continue  # Skip hidden files
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                            output_text += f"{filename} :\n\n{file_content}\n____\n"
                    except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                        # Ignore binary files and restricted files
                        output_text += f"{filename} :\n\n[Cannot read file content]\n____\n"

            # Schedule the GUI update in the main thread
            self.textbox.after(0, self.update_textbox, output_text)
        finally:
            # Stop the progress bar animation
            self.progress_bar_running = False
            # Enable buttons after processing
            self.toggle_buttons("enable")

    def update_textbox(self, text):
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, text)

    def get_directory_tree(self, directory, level=0):
        tree_str = ""
        indent = "  " * level
        tree_str += f"{indent}{os.path.basename(directory)}/\n"
        try:
            for item in os.listdir(directory):
                if not self.include_hidden_var.get() and item.startswith('.'):
                    continue  # Skip hidden files and directories
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    tree_str += self.get_directory_tree(item_path, level + 1)
                else:
                    tree_str += f"{indent}  {item}\n"
        except PermissionError:
            tree_str += f"{indent}  [Permission Denied]\n"
        return tree_str

    def clear_text(self):
        self.textbox.delete(1.0, tk.END)

    def save_as_txt(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.textbox.get(1.0, tk.END))
                messagebox.showinfo("Success", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    # Keyboard Shortcut Methods
    def copy_text(self, event=None):
        try:
            selected_text = self.textbox.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            pass
        return "break"

    def cut_text(self, event=None):
        self.copy_text()
        try:
            self.textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
        return "break"

    def paste_text(self, event=None):
        try:
            position = self.textbox.index(tk.INSERT)
            self.textbox.insert(position, self.root.clipboard_get())
        except tk.TclError:
            pass
        return "break"

    def select_all(self, event=None):
        self.textbox.tag_add(tk.SEL, "1.0", tk.END)
        self.textbox.mark_set(tk.INSERT, "1.0")
        self.textbox.see(tk.INSERT)
        return "break"

    def toggle_buttons(self, state):
        if state == "disable":
            self.browse_button.configure(state="disabled")
            self.clear_button.configure(state="disabled")
            self.save_button.configure(state="disabled")
            self.include_hidden_checkbox.configure(state="disabled")
        else:
            self.browse_button.configure(state="normal")
            self.clear_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.include_hidden_checkbox.configure(state="normal")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DirectoryExtractorApp(root)
    root.mainloop()

