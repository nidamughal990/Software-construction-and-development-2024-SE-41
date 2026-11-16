import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Carpet Cost Calculator")
root.geometry("760x760")
root.resizable(False, False)
root.configure(bg="#F2F6F7")

# ---------------- COLORS ----------------

BG = "#F2F6F7"
DARK = "#174A5B"
TEAL = "#247C80"
GOLD = "#E5A93D"
WHITE = "#FFFFFF"
CORAL = "#E47768"
TEXT = "#263B43"

# ---------------- CARPET PRICES ----------------
# Rates are sample prices per square unit.

carpet_prices = {
    "Basic Carpet": 500,
    "Standard Carpet": 800,
    "Premium Carpet": 1200
}

invoice_text = ""


# ---------------- HEADER ----------------

header = tk.Frame(root, bg=DARK, height=95)
header.pack(fill="x")

tk.Label(
    header,
    text="CARPET COST CALCULATOR",
    font=("Arial", 22, "bold"),
    bg=DARK,
    fg=WHITE
).pack(pady=(18, 5))

tk.Label(
    header,
    text="Calculate carpet price and generate your invoice",
    font=("Arial", 10),
    bg=DARK,
    fg="#D8E9EA"
).pack()


# ---------------- MAIN FORM ----------------

main_frame = tk.Frame(root, bg=WHITE)
main_frame.pack(padx=35, pady=20, fill="both", expand=True)

tk.Label(
    main_frame,
    text="Customer Information",
    font=("Arial", 15, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=25, pady=(15, 8))


def create_label(text):
    tk.Label(
        main_frame,
        text=text,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=25, pady=(5, 3))


# ---------------- CUSTOMER NAME ----------------

create_label("Customer Name")

name_entry = tk.Entry(
    main_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
name_entry.pack(fill="x", padx=25, ipady=6)


# ---------------- LENGTH ----------------

create_label("Carpet Length")

length_entry = tk.Entry(
    main_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
length_entry.pack(fill="x", padx=25, ipady=6)


# ---------------- WIDTH ----------------

create_label("Carpet Width")

width_entry = tk.Entry(
    main_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
width_entry.pack(fill="x", padx=25, ipady=6)


# ---------------- MEASUREMENT UNIT ----------------

create_label("Select Measurement Unit")

unit_var = tk.StringVar()

unit_box = ttk.Combobox(
    main_frame,
    textvariable=unit_var,
    values=["Feet", "Metres"],
    state="readonly",
    font=("Arial", 11)
)

unit_box.pack(fill="x", padx=25, ipady=4)
unit_box.current(0)


# ---------------- CARPET TYPE ----------------

create_label("Select Carpet Type")

carpet_var = tk.StringVar()

carpet_box = ttk.Combobox(
    main_frame,
    textvariable=carpet_var,
    values=list(carpet_prices.keys()),
    state="readonly",
    font=("Arial", 11)
)

carpet_box.pack(fill="x", padx=25, ipady=4)
carpet_box.current(0)


# ---------------- PRICE DISPLAY ----------------

price_label = tk.Label(
    main_frame,
    text="Price per square unit: Rs. 500",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEAL
)

price_label.pack(anchor="w", padx=25, pady=8)


def update_price(event=None):

    selected = carpet_var.get()
    price = carpet_prices[selected]

    price_label.config(
        text=f"Price per square unit: Rs. {price:,.2f}"
    )


carpet_box.bind("<<ComboboxSelected>>", update_price)


# ---------------- RESULT AREA ----------------

result_frame = tk.Frame(
    main_frame,
    bg="#E5F1F0",
    padx=15,
    pady=10
)

result_frame.pack(fill="x", padx=25, pady=8)

result_label = tk.Label(
    result_frame,
    text="Your calculation will appear here.",
    font=("Arial", 10),
    bg="#E5F1F0",
    fg=DARK,
    justify="left"
)

result_label.pack(anchor="w")


# ---------------- CALCULATE COST ----------------

def calculate_cost():

    global invoice_text

    customer_name = name_entry.get().strip()

    if not customer_name:
        messagebox.showerror(
            "Missing Information",
            "Please enter the customer name."
        )
        name_entry.focus()
        return

    try:
        length = float(length_entry.get())
        width = float(width_entry.get())

        if length <= 0 or width <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Length and width must be greater than zero."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for length and width."
        )
        return

    # Get selected unit and carpet type

    unit = unit_var.get()
    carpet_type = carpet_var.get()
    rate = carpet_prices[carpet_type]

    # Calculate area

    area = length * width

    if unit == "Feet":
        area_unit = "Square Feet"
    else:
        area_unit = "Square Metres"

    # Calculate carpet cost

    carpet_cost = area * rate

    # Calculate tax

    if carpet_cost < 30000:
        tax_rate = 10
    else:
        tax_rate = 15

    tax_amount = carpet_cost * tax_rate / 100
    final_cost = carpet_cost + tax_amount

    # Invoice date and number

    invoice_number = datetime.now().strftime(
        "INV%Y%m%d%H%M%S"
    )

    invoice_date = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    # Prepare invoice

    invoice_text = f"""
========================================
             CARPET INVOICE
========================================

Invoice Number: {invoice_number}
Date: {invoice_date}

Customer Name: {customer_name}

----------------------------------------
             PRODUCT DETAILS
----------------------------------------

Carpet Type:       {carpet_type}

Length:            {length:g} {unit}
Width:             {width:g} {unit}

Total Area:        {area:,.2f} {area_unit}

Rate:              Rs. {rate:,.2f}
                   per square unit

----------------------------------------
             PRICE DETAILS
----------------------------------------

Carpet Cost:       Rs. {carpet_cost:,.2f}

Tax Rate:          {tax_rate}%

Tax Amount:        Rs. {tax_amount:,.2f}

----------------------------------------

FINAL AMOUNT:      Rs. {final_cost:,.2f}

========================================
          THANK YOU FOR YOUR VISIT!
========================================
"""

    # Display calculation

    result_label.config(
        text=(
            f"Customer: {customer_name}\n"
            f"Area: {area:,.2f} {area_unit}\n"
            f"Carpet Cost: Rs. {carpet_cost:,.2f}\n"
            f"Tax ({tax_rate}%): Rs. {tax_amount:,.2f}\n"
            f"Final Cost: Rs. {final_cost:,.2f}"
        )
    )

    messagebox.showinfo(
        "Calculation Complete",
        f"Final Carpet Cost: Rs. {final_cost:,.2f}"
    )


# ---------------- GENERATE INVOICE ----------------

def generate_invoice():

    if not invoice_text:
        messagebox.showwarning(
            "No Invoice",
            "Please calculate the carpet cost first."
        )
        return

    invoice_window = tk.Toplevel(root)
    invoice_window.title("Customer Invoice")
    invoice_window.geometry("520x600")
    invoice_window.configure(bg=BG)

    tk.Label(
        invoice_window,
        text="CUSTOMER INVOICE",
        font=("Arial", 19, "bold"),
        bg=DARK,
        fg=WHITE,
        pady=18
    ).pack(fill="x")

    invoice_display = tk.Text(
        invoice_window,
        font=("Consolas", 10),
        bg=WHITE,
        fg=TEXT,
        relief="solid",
        bd=1,
        wrap="none"
    )

    invoice_display.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    invoice_display.insert("1.0", invoice_text)
    invoice_display.config(state="disabled")

    tk.Button(
        invoice_window,
        text="Save Invoice",
        font=("Arial", 11, "bold"),
        bg=TEAL,
        fg=WHITE,
        cursor="hand2",
        command=save_invoice,
        relief="flat",
        padx=20,
        pady=10
    ).pack(pady=(0, 20))


# ---------------- SAVE INVOICE ----------------

def save_invoice():

    if not invoice_text:
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile="Carpet_Invoice.txt"
    )

    if file_path:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(invoice_text)

        messagebox.showinfo(
            "Saved Successfully",
            "Your invoice has been saved successfully."
        )


# ---------------- CLEAR FORM ----------------

def clear_fields():

    global invoice_text

    name_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)

    unit_box.current(0)
    carpet_box.current(0)

    update_price()

    invoice_text = ""

    result_label.config(
        text="Your calculation will appear here."
    )


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(
    main_frame,
    bg=WHITE
)

button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Calculate Cost",
    command=calculate_cost,
    font=("Arial", 10, "bold"),
    bg=TEAL,
    fg=WHITE,
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=10
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Generate Invoice",
    command=generate_invoice,
    font=("Arial", 10, "bold"),
    bg=GOLD,
    fg=DARK,
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=10
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=("Arial", 10, "bold"),
    bg=CORAL,
    fg=WHITE,
    cursor="hand2",
    relief="flat",
    padx=15,
    pady=10
).grid(row=0, column=2, padx=5)


# ---------------- FOOTER ----------------

tk.Label(
    root,
    text="Carpet Cost Calculator | Python Tkinter",
    font=("Arial", 9),
    bg=BG,
    fg="#65777D"
).pack(pady=(0, 10))


# ---------------- RUN APPLICATION ----------------

root.mainloop()