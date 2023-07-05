import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.font import Font
import re


class Notepad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notepad")
        self.root.geometry("800x600")

        self.current_file = None
        self.text_changed = False
        self.dark_mode = False
        self.spell_check_enabled = False

        self.create_menu()
        self.create_toolbar()
        self.create_textarea()
        self.create_line_number()

        self.status_bar = tk.Label(self.root, text="Line: 1 | Column: 0", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-Shift-S>", self.save_file_as)
        self.root.bind("<Control-f>", self.find_replace)
        self.root.bind("<Control-b>", self.toggle_bold)
        self.root.bind("<Control-i>", self.toggle_italic)
        self.root.bind("<Control-u>", self.toggle_underline)
        self.root.bind("<Control-l>", self.toggle_line_numbers)
        self.root.bind("<Control-d>", self.toggle_dark_mode)
        self.root.bind("<Control-h>", self.toggle_syntax_highlighting)
        self.root.bind("<Control-w>", self.word_count)
        self.root.bind("<Control-e>", self.toggle_spell_check)
        self.textarea.bind("<<Modified>>", self.on_text_change)

    def create_menu(self):
        self.menu = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)
        edit_menu.add_command(label="Find and Replace", accelerator="Ctrl+F", command=self.find_replace)
        self.menu.add_cascade(label="Edit", menu=edit_menu)

        # Format Menu
        format_menu = tk.Menu(self.menu, tearoff=0)
        format_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.toggle_bold)
        format_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.toggle_italic)
        format_menu.add_command(label="Underline", accelerator="Ctrl+U", command=self.toggle_underline)
        format_menu.add_separator()
        format_menu.add_command(label="Toggle Line Numbers", accelerator="Ctrl+L", command=self.toggle_line_numbers)
        format_menu.add_command(label="Toggle Dark Mode", accelerator="Ctrl+D", command=self.toggle_dark_mode)
        format_menu.add_command(label="Toggle Syntax Highlighting", accelerator="Ctrl+H",
                                command=self.toggle_syntax_highlighting)
        self.menu.add_cascade(label="Format", menu=format_menu)

        # Tools Menu
        tools_menu = tk.Menu(self.menu, tearoff=0)
        tools_menu.add_command(label="Word Count", accelerator="Ctrl+W", command=self.word_count)
        tools_menu.add_command(label="Toggle Spell Check", accelerator="Ctrl+E", command=self.toggle_spell_check)
        self.menu.add_cascade(label="Tools", menu=tools_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=self.menu)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        bold_button = tk.Button(toolbar, text="Bold", command=self.toggle_bold)
        bold_button.pack(side=tk.LEFT, padx=2, pady=2)

        italic_button = tk.Button(toolbar, text="Italic", command=self.toggle_italic)
        italic_button.pack(side=tk.LEFT, padx=2, pady=2)

        underline_button = tk.Button(toolbar, text="Underline", command=self.toggle_underline)
        underline_button.pack(side=tk.LEFT, padx=2, pady=2)

        line_numbers_button = tk.Button(toolbar, text="Line Numbers", command=self.toggle_line_numbers)
        line_numbers_button.pack(side=tk.LEFT, padx=2, pady=2)

        dark_mode_button = tk.Button(toolbar, text="Dark Mode", command=self.toggle_dark_mode)
        dark_mode_button.pack(side=tk.LEFT, padx=2, pady=2)

    def create_textarea(self):
        self.textarea = tk.Text(self.root)
        self.textarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.textarea)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textarea.yview)

    def create_line_number(self):
        self.line_number = tk.Text(self.root, width=4, padx=4, takefocus=0, border=0, background="#f0f0f0",
                                   state=tk.DISABLED)
        self.line_number.pack(side=tk.LEFT, fill=tk.Y)

    def run(self):
        self.root.mainloop()

    def exit_application(self):
        if self.text_changed:
            if messagebox.askyesno("Unsaved Changes", "Do you want to save changes?"):
                self.save_file()
        self.root.destroy()

    def new_file(self, event=None):
        if self.text_changed:
            if not messagebox.askyesno("Unsaved Changes", "Do you want to save changes?"):
                self.textarea.delete("1.0", tk.END)
                self.root.title("Notepad")
                self.current_file = None
                self.text_changed = False
                return

        self.textarea.delete("1.0", tk.END)
        self.root.title("Notepad")
        self.current_file = None
        self.text_changed = False

    def open_file(self, event=None):
        if self.text_changed:
            if not messagebox.askyesno("Unsaved Changes", "Do you want to save changes?"):
                file_path = filedialog.askopenfilename(initialdir=".", title="Open File",
                                                       filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
                if file_path:
                    self.current_file = file_path
                    self.root.title(f"Notepad - {self.current_file}")
                    self.text_changed = False
                    self.textarea.delete("1.0", tk.END)
                    with open(file_path, "r") as file:
                        self.textarea.insert(tk.END, file.read())
            return

        file_path = filedialog.askopenfilename(initialdir=".", title="Open File",
                                               filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.current_file = file_path
            self.root.title(f"Notepad - {self.current_file}")
            self.text_changed = False
            self.textarea.delete("1.0", tk.END)
            with open(file_path, "r") as file:
                self.textarea.insert(tk.END, file.read())

    def save_file(self, event=None):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.textarea.get("1.0", tk.END))
            self.text_changed = False
        else:
            self.save_file_as()

    def save_file_as(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=".", title="Save File",
                                                 filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.textarea.get("1.0", tk.END))
            self.current_file = file_path
            self.root.title(f"Notepad - {self.current_file}")
            self.text_changed = False

    def cut_text(self, event=None):
        self.textarea.event_generate("<<Cut>>")

    def copy_text(self, event=None):
        self.textarea.event_generate("<<Copy>>")

    def paste_text(self, event=None):
        self.textarea.event_generate("<<Paste>>")

    def select_all(self, event=None):
        self.textarea.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def find_replace(self, event=None):
        def find():
            search_text = search_entry.get()
            start_position = self.textarea.index("insert")
            start = self.textarea.search(search_text, start_position, tk.END, nocase=True)
            if start:
                end = f"{start}+{len(search_text)}c"
                self.textarea.tag_remove(tk.SEL, "1.0", tk.END)
                self.textarea.tag_add(tk.SEL, start, end)
                self.textarea.mark_set(tk.INSERT, end)
                self.textarea.see(tk.INSERT)
                search_window.focus_set()

        def replace():
            search_text = search_entry.get()
            replace_text = replace_entry.get()
            selected_text = self.textarea.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text == search_text:
                self.textarea.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.textarea.insert(tk.INSERT, replace_text)
                search_window.focus_set()

        search_window = tk.Toplevel(self.root)
        search_window.title("Find and Replace")
        search_window.geometry("300x120")
        search_window.resizable(False, False)
        search_window.transient(self.root)

        search_label = tk.Label(search_window, text="Find:")
        search_label.pack(pady=5)
        search_entry = tk.Entry(search_window, width=30)
        search_entry.pack()

        replace_label = tk.Label(search_window, text="Replace:")
        replace_label.pack(pady=5)
        replace_entry = tk.Entry(search_window, width=30)
        replace_entry.pack()

        find_button = tk.Button(search_window, text="Find", width=10, command=find)
        find_button.pack(side=tk.LEFT, padx=5, pady=5)

        replace_button = tk.Button(search_window, text="Replace", width=10, command=replace)
        replace_button.pack(side=tk.LEFT, padx=5, pady=5)

        search_entry.focus_set()
        search_window.bind("<Return>", lambda event: find())
        search_window.bind("<Escape>", lambda event: search_window.destroy())

    def toggle_bold(self, event=None):
        current_tags = self.textarea.tag_names("sel.first")
        if "bold" in current_tags:
            self.textarea.tag_remove("bold", "sel.first", "sel.last")
            self.textarea.tag_configure("bold", font=("Arial", 12, "normal"))
        else:
            self.textarea.tag_add("bold", "sel.first", "sel.last")
            self.textarea.tag_configure("bold", font=("Arial", 12, "bold"))

    def toggle_italic(self, event=None):
        current_tags = self.textarea.tag_names("sel.first")
        if "italic" in current_tags:
            self.textarea.tag_remove("italic", "sel.first", "sel.last")
            self.textarea.tag_configure("italic", font=("Arial", 12, "normal"))
        else:
            self.textarea.tag_add("italic", "sel.first", "sel.last")
            self.textarea.tag_configure("italic", font=("Arial", 12, "italic"))

    def toggle_underline(self, event=None):
        current_tags = self.textarea.tag_names("sel.first")
        if "underline" in current_tags:
            self.textarea.tag_remove("underline", "sel.first", "sel.last")
            self.textarea.tag_configure("underline", underline=False)
        else:
            self.textarea.tag_add("underline", "sel.first", "sel.last")
            self.textarea.tag_configure("underline", underline=True)

    def toggle_line_numbers(self, event=None):
        if self.line_number.winfo_ismapped():
            self.line_number.pack_forget()
        else:
            self.line_number.pack(side=tk.LEFT, fill=tk.Y)

    def toggle_dark_mode(self, event=None):
        self.dark_mode = not self.dark_mode
        bg_color = "#1f1f1f" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        self.root.config(bg=bg_color)
        self.textarea.config(bg=bg_color, fg=fg_color)
        self.line_number.config(bg=bg_color, fg=fg_color)
        self.scrollbar.config(bg=bg_color)
        self.status_bar.config(bg=bg_color, fg=fg_color)

    def toggle_syntax_highlighting(self, event=None):
        if self.textarea.tag_ranges("syntax_highlight"):
            self.textarea.tag_remove("syntax_highlight", "1.0", tk.END)
        else:
            keywords = ["class", "def", "if", "else", "elif", "for", "while", "in", "return", "import", "from",
                        "as", "global", "nonlocal", "try", "except", "finally", "raise", "assert", "with",
                        "yield", "lambda", "None", "True", "False"]
            pattern = "\\b(" + "|".join(keywords) + ")\\b"
            tags = [("keyword", "blue"), ("string", "green"), ("comment", "gray")]
            for tag, color in tags:
                self.textarea.tag_configure(tag, foreground=color)
            for line_number, line in enumerate(self.textarea.get("1.0", tk.END).split("\n")):
                for match in re.finditer(pattern, line):
                    start = f"{line_number + 1}.{match.start()}"
                    end = f"{line_number + 1}.{match.end()}"
                    self.textarea.tag_add("syntax_highlight", start, end)

    def word_count(self, event=None):
        text = self.textarea.get("1.0", tk.END)
        word_count = len(re.findall(r'\b\w+\b', text))
        character_count = len(text.replace(" ", "").replace("\n", ""))
        messagebox.showinfo("Word Count", f"Word Count: {word_count}\nCharacter Count: {character_count}")

    def toggle_spell_check(self, event=None):
        self.spell_check_enabled = not self.spell_check_enabled
        if self.spell_check_enabled:
            self.textarea.bind("<KeyRelease>", self.spell_check)
            messagebox.showinfo("Spell Check", "Spell Check enabled.")
        else:
            self.textarea.unbind("<KeyRelease>")
            messagebox.showinfo("Spell Check", "Spell Check disabled.")

    def spell_check(self, event=None):
        current_index = self.textarea.index("insert")
        words = re.findall(r'\b\w+\b', self.textarea.get("1.0", tk.END))
        if current_index == "1.0" or current_index == tk.END or current_index[-1] == " " or not words:
            return
        current_word = words[-1]
        dictionary = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]
        if current_word not in dictionary:
            messagebox.showwarning("Spell Check", f"Possible spelling mistake: {current_word}")

    def on_text_change(self, event=None):
        self.text_changed = True
        lines = self.textarea.get("1.0", tk.END).split("\n")
        line_count = len(lines)
        column_count = len(lines[-1])
        self.status_bar.config(text=f"Line: {line_count} | Column: {column_count}")

    def show_about(self):
        messagebox.showinfo("About", "Advanced Notepad\nVersion 1.0\n\nCreated by Bennet Nkolele")


if __name__ == "__main__":
    notepad = Notepad()
    notepad.run()