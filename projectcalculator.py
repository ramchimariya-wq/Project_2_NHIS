import tkinter as tk
from tkinter import ttk
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("700x600")
        self.root.configure(bg="#1e1e1e")

        # ====== STATE ======
        self.expression = ""
        self.memory = 0.0
        self.degree_mode = True  # True = Degree, False = Radian

        # ====== DISPLAY ======
        self.equation = tk.StringVar()

        entry = tk.Entry(
            root,
            textvariable=self.equation,
            font=("Arial", 22),
            bg="#2d2d2d",
            fg="white",
            bd=10,
            relief="sunken",
            justify="right",
        )
        entry.pack(fill="x", padx=10, pady=5, ipady=15)

        # ====== MAIN FRAME ======
        main_frame = tk.Frame(root, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True)

        # ====== BUTTON FRAME ======
        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(side="left", padx=10)

        # ====== HISTORY PANEL ======
        history_frame = tk.Frame(main_frame, bg="#1e1e1e")
        history_frame.pack(side="right", fill="y")

        tk.Label(
            history_frame,
            text="History",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 14, "bold"),
        ).pack()

        self.history_list = tk.Listbox(
            history_frame,
            width=28,
            height=25,
            bg="#2d2d2d",
            fg="white",
        )
        self.history_list.pack(padx=5, pady=5)

        # ====== BUTTON STYLE ======
        self.btn_style = {
            "width": 6,
            "height": 2,
            "font": ("Arial", 12),
            "bg": "#3c3f41",
            "fg": "white",
        }

        # ====== BUTTONS ======
        buttons = [
            ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3), ('sqrt',1,4),
            ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3), ('x²',2,4),
            ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3), ('(',3,4),
            ('0',4,0), ('.',4,1), ('+',4,2), (')',4,3), ('=',4,4),
            ('sin',5,0), ('cos',5,1), ('tan',5,2), ('log',5,3), ('ln',5,4),
            ('π',6,0), ('e',6,1), ('EXP',6,2), ('C',6,3), ('⌫',6,4),
            ('M+',7,0), ('M-',7,1), ('MR',7,2), ('MC',7,3), ('Deg',7,4),
        ]

        for (text, row, col) in buttons:
            self.create_button(btn_frame, text, row, col)

        # Keyboard bindings
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())

    # =========================================================
    # BUTTON CREATOR
    # =========================================================
    def create_button(self, frame, text, row, col):
        action_map = {
            '=': self.calculate,
            'C': self.clear,
            '⌫': self.backspace,
            'sin': self.sin_func,
            'cos': self.cos_func,
            'tan': self.tan_func,
            'sqrt': self.sqrt_func,
            'log': self.log_func,
            'ln': self.ln_func,
            'π': lambda: self.press(math.pi),
            'e': lambda: self.press(math.e),
            'x²': lambda: self.press("**2"),
            'EXP': lambda: self.press("e"),
            'M+': self.memory_add,
            'M-': self.memory_subtract,
            'MR': self.memory_recall,
            'MC': self.memory_clear,
            'Deg': self.toggle_mode,
        }

        if text in action_map:
            cmd = action_map[text]
        else:
            cmd = lambda t=text: self.press(t)

        btn = tk.Button(frame, text=text, command=cmd, **self.btn_style)
        btn.grid(row=row, column=col, padx=4, pady=4)

    # =========================================================
    # BASIC FUNCTIONS
    # =========================================================
    def press(self, value):
        self.expression += str(value)
        self.equation.set(self.expression)

    def clear(self):
        self.expression = ""
        self.equation.set("")

    def backspace(self):
        self.expression = self.expression[:-1]
        self.equation.set(self.expression)

    # =========================================================
    # SAFE CALCULATION
    # =========================================================
    def calculate(self):
        try:
            allowed = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e,
                "__builtins__": {}
            }

            result = eval(self.expression, allowed)
            self.history_list.insert(tk.END, f"{self.expression} = {result}")
            self.expression = str(result)
            self.equation.set(result)

        except Exception:
            self.equation.set("Error")
            self.expression = ""

    # =========================================================
    # SCIENTIFIC FUNCTIONS
    # =========================================================
    def _convert_angle(self, value):
        return math.radians(value) if self.degree_mode else value

    def sin_func(self):
        self._single_math(math.sin)

    def cos_func(self):
        self._single_math(math.cos)

    def tan_func(self):
        self._single_math(math.tan)

    def _single_math(self, func):
        try:
            value = float(self.expression)
            value = self._convert_angle(value)
            result = func(value)
            self.history_list.insert(tk.END, f"{func.__name__} = {result}")
            self.expression = str(result)
            self.equation.set(result)
        except:
            self.equation.set("Error")

    def sqrt_func(self):
        self._simple_apply(math.sqrt)

    def log_func(self):
        self._simple_apply(math.log10)

    def ln_func(self):
        self._simple_apply(math.log)

    def _simple_apply(self, func):
        try:
            value = float(self.expression)
            result = func(value)
            self.history_list.insert(tk.END, f"{func.__name__} = {result}")
            self.expression = str(result)
            self.equation.set(result)
        except:
            self.equation.set("Error")

    # =========================================================
    # MEMORY FUNCTIONS
    # =========================================================
    def memory_add(self):
        try:
            self.memory += float(self.expression)
        except:
            pass

    def memory_subtract(self):
        try:
            self.memory -= float(self.expression)
        except:
            pass

    def memory_recall(self):
        self.expression += str(self.memory)
        self.equation.set(self.expression)

    def memory_clear(self):
        self.memory = 0.0

    # =========================================================
    # DEG/RAD TOGGLE
    # =========================================================
    def toggle_mode(self):
        self.degree_mode = not self.degree_mode
        mode = "Deg" if self.degree_mode else "Rad"
        self.history_list.insert(tk.END, f"Mode → {mode}")


# =============================================================
# RUN APP
# =============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
