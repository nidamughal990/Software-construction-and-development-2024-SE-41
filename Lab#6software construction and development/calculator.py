import tkinter as tk

# Main window
root = tk.Tk()
root.title("Professional Calculator")
root.geometry("380x590")
root.resizable(False, False)
root.config(bg="#15152B")

# Calculator variables
first_number = None
operator = None
new_number = False

# Display variables
display = tk.StringVar(value="0")
expression = tk.StringVar(value="Ready")

# Header
header = tk.Frame(root, bg="#15152B")
header.pack(fill="x", padx=22, pady=(22, 10))

title = tk.Label(
    header,
    text="CALCULATOR",

    font=("Arial", 19, "bold"),
    fg="#FFFFFF",
    bg="#15152B"
)
title.pack(anchor="w")

subtitle = tk.Label(
    header,
    text="SMART • SIMPLE • PROFESSIONAL",
    font=("Arial", 8, "bold"),
    fg="#9B9BC0",
    bg="#15152B"
)
subtitle.pack(anchor="w", pady=(5, 0))

# Display section
display_frame = tk.Frame(
    root,
    bg="#252544",
    padx=15,
    pady=15
)
display_frame.pack(fill="x", padx=18, pady=15)

expression_label = tk.Label(
    display_frame,
    textvariable=expression,
    font=("Arial", 11),
    fg="#A9A9C8",
    bg="#252544",
    anchor="e"
)
expression_label.pack(fill="x", pady=(0, 12))

screen = tk.Entry(
    display_frame,
    textvariable=display,
    font=("Arial", 32, "bold"),
    fg="#FFFFFF",
    bg="#252544",
    justify="right",
    bd=0,
    state="readonly",
    readonlybackground="#252544"
)
screen.pack(fill="x", ipady=10)

# Button functions

def number_click(number):
    global new_number

    if new_number or display.get() == "Error":
        display.set(number)
        new_number = False
    elif display.get() == "0":
        display.set(number)
    else:
        display.set(display.get() + number)


def decimal_click():
    global new_number

    if new_number or display.get() == "Error":
        display.set("0.")
        new_number = False
    elif "." not in display.get():
        display.set(display.get() + ".")


def calculate():
    global first_number, operator, new_number

    if first_number is None or operator is None:
        return

    if display.get() == "Error":
        return

    second_number = float(display.get())

    expression.set(
        f"{first_number:g} {operator} {second_number:g}"
    )

    if operator == "+":
        result = first_number + second_number

    elif operator == "-":
        result = first_number - second_number

    elif operator == "*":
        result = first_number * second_number

    elif operator == "/":
        if second_number == 0:
            display.set("Error")
            first_number = None
            operator = None
            new_number = True
            return

        result = first_number / second_number

    display.set(f"{result:.10g}")

    first_number = None
    operator = None
    new_number = True


def operator_click(selected_operator):
    global first_number, operator, new_number

    if display.get() == "Error":
        return

    if first_number is not None and new_number:
        operator = selected_operator
        return

    if first_number is None:
        first_number = float(display.get())
    else:
        calculate()
        first_number = float(display.get())

    operator = selected_operator
    expression.set(f"{first_number:g} {operator}")
    new_number = True


def clear():
    global first_number, operator, new_number

    display.set("0")
    expression.set("Ready")

    first_number = None
    operator = None
    new_number = False


def backspace():
    global new_number

    if new_number or display.get() == "Error":
        return

    current = display.get()

    if len(current) > 1:
        display.set(current[:-1])
    else:
        display.set("0")


def percentage():
    global new_number

    if display.get() != "Error":
        result = float(display.get()) / 100
        display.set(f"{result:.10g}")
        new_number = True


def change_sign():
    global new_number

    if display.get() != "Error":
        result = float(display.get()) * -1
        display.set(f"{result:.10g}")
        new_number = False


# Button section
button_frame = tk.Frame(root, bg="#15152B")
button_frame.pack(fill="both", expand=True, padx=16, pady=10)

# Button information
buttons = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="]
]

# Button colors
number_color = "#303052"
special_color = "#45456A"
operator_color = "#7048D8"
clear_color = "#D94B5B"
equal_color = "#168C76"

# Create buttons
for row_index, row in enumerate(buttons):

    for column_index, text_value in enumerate(row):

        if text_value == "C":
            color = clear_color
            command = clear

        elif text_value == "⌫":
            color = special_color
            command = backspace

        elif text_value == "%":
            color = special_color
            command = percentage

        elif text_value == "±":
            color = special_color
            command = change_sign

        elif text_value == "=":
            color = equal_color
            command = calculate

        elif text_value in ["÷", "×", "−", "+"]:
            color = operator_color

            if text_value == "÷":
                command = lambda: operator_click("/")
            elif text_value == "×":
                command = lambda: operator_click("*")
            elif text_value == "−":
                command = lambda: operator_click("-")
            else:
                command = lambda: operator_click("+")

        elif text_value == ".":
            color = number_color
            command = decimal_click

        else:
            color = number_color
            command = lambda value=text_value: number_click(value)

        button = tk.Button(
            button_frame,
            text=text_value,
            font=("Arial", 17, "bold"),
            bg=color,
            fg="white",
            activebackground="#8888B8",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=command
        )

        button.grid(
            row=row_index,
            column=column_index,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=2,
            ipady=13
        )

# Equal button and all other buttons
for row in range(5):
    button_frame.rowconfigure(row, weight=1)

for column in range(4):
    button_frame.columnconfigure(column, weight=1)

# Footer
footer = tk.Label(
    root,
    text="MY PROFESSIONAL CALCULATOR",
    font=("Arial", 8, "bold"),
    fg="#77779C",
    bg="#15152B"
)
footer.pack(pady=(5, 15))

# Start application
root.mainloop()