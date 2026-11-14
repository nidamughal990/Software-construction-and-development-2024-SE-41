import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

CARPET_PRICES = {
    "Basic Carpet": 500,
    "Standard Carpet": 800,
    "Premium Carpet": 1200
}

BG = "#F4F0E8"
WHITE = "#FFFFFF"
TEAL = "#176B67"
GOLD = "#D9A441"
CORAL = "#D96C55"
DARK = "#263238"
LIGHT = "#E3F1EE"

calculation = None
invoice_text = ""
invoice_number = ""

def update_price(event=None):
    selected = carpet_type.get()
    price = CARPET_PRICES[selected]
    price_label.config(text=f"Price: Rs. {price:,.2f} per square unit")

def measure_price_summary(length, width, selected_carpet, price):
    area = length * width
    carpet_cost = area * price
    tax_rate = 10 if carpet_cost < 30000 else 15
    tax_amount = carpet_cost * tax_rate / 100
    final_cost = carpet_cost + tax_amount

    area_result.set(f"{area:,.2f}")
    cost_result.set(f"Rs. {carpet_cost:,.2f}")
    tax_result.set(f"{tax_rate}%")
    tax_amount_result.set(f"Rs. {tax_amount:,.2f}")
    final_result.set(f"Rs. {final_cost:,.2f}")

    return {
        "length": length, "width": width, "carpet": selected_carpet,
        "price": price, "area": area, "carpet_cost": carpet_cost,
        "tax_rate": tax_rate, "tax_amount": tax_amount, "final_cost": final_cost
    }

def convert_to_meter(value, unit):
    # اگر Feet Select کیا ہو گا تو اس کو Meter میں بدل دو
    if unit == "Feet":
        return value * 0.3048
    return value

def calculate_cost():
    global calculation
    try:
        length_raw = float(length_entry.get().strip())
        width_raw = float(width_entry.get().strip())
        if length_raw <= 0 or width_raw <= 0:
            messagebox.showerror("Invalid Input", "Length and width must be greater than zero.")
            return
        
        # یہاں سے ڈبے والی Value لی ہے
        length = convert_to_meter(length_raw, length_unit.get())
        width = convert_to_meter(width_raw, width_unit.get())

        selected_carpet = carpet_type.get()
        price = CARPET_PRICES[selected_carpet]
        calculation = measure_price_summary(length, width, selected_carpet, price)
        # Invoice کے لیے اصلی والی Value بھی رکھ لی
        calculation["length_raw"] = length_raw
        calculation["width_raw"] = width_raw
        calculation["length_unit"] = length_unit.get()
        calculation["width_unit"] = width_unit.get()
        messagebox.showinfo("Calculated", "Price calculated successfully! Check Price Summary.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for length and width.")

def generate_invoice():
    global invoice_text, invoice_number
    if calculation is None:
        messagebox.showwarning("Warning", "Please calculate the carpet cost first.")
        return
    data = calculation
    invoice_number = datetime.now().strftime("INV%Y%m%d%H%M%S")
    invoice_date = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    invoice_text = f"""
          CARPET SELLER SHOP
               INVOICE
Invoice Number: {invoice_number}
Date: {invoice_date}
           PRODUCT DETAILS
Carpet Type: {data['carpet']}
Length: {data.get('length_raw', data['length'])} {data.get('length_unit', 'Meter')}
Width: {data.get('width_raw', data['width'])} {data.get('width_unit', 'Meter')}
Area: {data['area']:,.2f} square units
Price per square unit: Rs. {data['price']:,.2f}
             PRICE DETAILS
Carpet Cost: Rs. {data['carpet_cost']:,.2f}
Tax Rate: {data['tax_rate']}%
Tax Amount: Rs. {data['tax_amount']:,.2f}
FINAL COST: Rs. {data['final_cost']:,.2f}
       Thank You For Your Purchase!
"""
    invoice_window = tk.Toplevel(root)
    invoice_window.title("Carpet Invoice")
    invoice_window.geometry("500x600")
    invoice_window.configure(bg=BG)
    tk.Label(invoice_window, text="YOUR INVOICE", font=("Arial", 20, "bold"), bg=TEAL, fg=WHITE, pady=15).pack(fill="x")
    invoice_box = tk.Text(invoice_window, font=("Courier New", 10), bg=WHITE, fg=DARK, padx=20, pady=20, relief="flat")
    invoice_box.pack(fill="both", expand=True, padx=20, pady=15)
    invoice_box.insert("1.0", invoice_text)
    invoice_box.config(state="disabled")
    tk.Button(invoice_window, text="SAVE INVOICE", command=save_invoice, bg=GOLD, fg=DARK, font=("Arial", 11, "bold"), relief="flat", padx=25, pady=10, cursor="hand2").pack(pady=15)

def save_invoice():
    if not invoice_text: return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=invoice_number + ".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file: file.write(invoice_text)
        messagebox.showinfo("Success", "Invoice saved successfully.")

def clear_fields():
    global calculation, invoice_text, invoice_number
    length_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)
    length_unit.set("Meter")
    width_unit.set("Meter")
    carpet_type.set("Basic Carpet")
    update_price()
    area_result.set("-"); cost_result.set("-"); tax_result.set("-"); tax_amount_result.set("-"); final_result.set("-")
    calculation = None; invoice_text = ""; invoice_number = ""

root = tk.Tk()
root.title("Carpet Cost Estimation System")
root.geometry("800x600")
root.minsize(700, 550)
root.configure(bg=BG)

header = tk.Frame(root, bg=TEAL, height=80)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="CARPET COST ESTIMATOR", font=("Arial", 20, "bold"), bg=TEAL, fg=WHITE).pack(pady=(15, 2))
tk.Label(header, text="Carpet Price Calculation and Invoice System", font=("Arial", 10), bg=TEAL, fg=WHITE).pack()

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=25, pady=10)

details = tk.Frame(main, bg=WHITE, highlightbackground="#DDDDDD", highlightthickness=1)
details.pack(fill="x", pady=(0, 10))
tk.Label(details, text="Carpet Information", font=("Arial", 13, "bold"), bg=WHITE, fg=DARK).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=10)

# --- Length + اس کا ڈبہ ---
tk.Label(details, text="Carpet Length", font=("Arial", 10, "bold"), bg=WHITE, fg=DARK).grid(row=1, column=0, sticky="w", padx=15, pady=2)
length_frame = tk.Frame(details, bg=WHITE)
length_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))
length_entry = tk.Entry(length_frame, font=("Arial", 11), relief="solid", bd=1)
length_entry.pack(side="left", fill="x", expand=True, ipady=5)
length_unit = tk.StringVar(value="Meter")
length_box = ttk.Combobox(length_frame, textvariable=length_unit, values=["Meter", "Feet"], state="readonly", width=8, font=("Arial", 10))
length_box.pack(side="left", padx=(5, 0))

# --- Width + اس کا ڈبہ ---
tk.Label(details, text="Carpet Width", font=("Arial", 10, "bold"), bg=WHITE, fg=DARK).grid(row=1, column=1, sticky="w", padx=15, pady=2)
width_frame = tk.Frame(details, bg=WHITE)
width_frame.grid(row=2, column=1, sticky="ew", padx=15, pady=(0, 10))
width_entry = tk.Entry(width_frame, font=("Arial", 11), relief="solid", bd=1)
width_entry.pack(side="left", fill="x", expand=True, ipady=5)
width_unit = tk.StringVar(value="Meter")
width_box = ttk.Combobox(width_frame, textvariable=width_unit, values=["Meter", "Feet"], state="readonly", width=8, font=("Arial", 10))
width_box.pack(side="left", padx=(5, 0))

tk.Label(details, text="Select Carpet Type", font=("Arial", 10, "bold"), bg=WHITE, fg=DARK).grid(row=3, column=0, sticky="w", padx=15, pady=2)
carpet_type = tk.StringVar(value="Basic Carpet")
style = ttk.Style(); style.theme_use("clam"); style.configure("TCombobox", padding=5, fieldbackground=WHITE, background=WHITE)
carpet_box = ttk.Combobox(details, textvariable=carpet_type, values=list(CARPET_PRICES.keys()), state="readonly", font=("Arial", 10))
carpet_box.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 10))
carpet_box.bind("<<ComboboxSelected>>", update_price)
price_label = tk.Label(details, text="Price: Rs. 500.00 per square unit", font=("Arial", 9, "bold"), bg=LIGHT, fg=TEAL, padx=10, pady=10)
price_label.grid(row=4, column=1, sticky="ew", padx=15, pady=(0, 10))
details.grid_columnconfigure(0, weight=1); details.grid_columnconfigure(1, weight=1)

summary = tk.Frame(main, bg=WHITE, highlightbackground="#DDDDDD", highlightthickness=1)
summary.pack(fill="both", expand=True)
tk.Label(summary, text="Price Summary", font=("Arial", 13, "bold"), bg=WHITE, fg=DARK).pack(anchor="w", padx=15, pady=10)
area_result = tk.StringVar(value="-"); cost_result = tk.StringVar(value="-"); tax_result = tk.StringVar(value="-"); tax_amount_result = tk.StringVar(value="-"); final_result = tk.StringVar(value="-")
def add_result_row(parent, title, value):
    row = tk.Frame(parent, bg=WHITE); row.pack(fill="x", padx=15, pady=3)
    tk.Label(row, text=title, font=("Arial", 10), bg=WHITE, fg="#555555").pack(side="left")
    tk.Label(row, textvariable=value, font=("Arial", 10, "bold"), bg=WHITE, fg=DARK).pack(side="right")
add_result_row(summary, "Carpet Area", area_result)
add_result_row(summary, "Overall Carpet Cost", cost_result)
add_result_row(summary, "Tax Percentage", tax_result)
add_result_row(summary, "Tax Amount", tax_amount_result)
total_frame = tk.Frame(summary, bg=LIGHT); total_frame.pack(fill="x", padx=15, pady=10)
tk.Label(total_frame, text="FINAL COST", font=("Arial", 11, "bold"), bg=LIGHT, fg=TEAL).pack(side="left", padx=10, pady=10)
tk.Label(total_frame, textvariable=final_result, font=("Arial", 14, "bold"), bg=LIGHT, fg=TEAL).pack(side="right", padx=10, pady=10)

buttons = tk.Frame(main, bg=BG); buttons.pack(fill="x", pady=10)
tk.Button(buttons, text="CALCULATE COST", command=calculate_cost, bg=TEAL, fg=WHITE, font=("Arial", 10, "bold"), relief="flat", cursor="hand2", padx=15, pady=10).pack(side="left", padx=5)
tk.Button(buttons, text="GENERATE INVOICE", command=generate_invoice, bg=GOLD, fg=DARK, font=("Arial", 10, "bold"), relief="flat", cursor="hand2", padx=15, pady=10).pack(side="left", padx=5)
tk.Button(buttons, text="CLEAR", command=clear_fields, bg=CORAL, fg=WHITE, font=("Arial", 10, "bold"), relief="flat", cursor="hand2", padx=20, pady=10).pack(side="right", padx=5)

tk.Label(root, text="Software Construction & Development | Lab 7", font=("Arial", 8), bg=BG, fg="#777777").pack(pady=(0, 5))
root.mainloop()