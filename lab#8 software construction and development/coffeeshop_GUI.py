# Lab 8 - Question 1
# Course: SE-3102 Software Construction & Development (Lab)
# Topic: Custom Exceptions

import tkinter as tk
from tkinter import messagebox

# ---------- Custom Exceptions ----------
class TooHotCoffeeCup(Exception):
    pass

class TooColdCoffeeCup(Exception):
    pass

# ---------- Logic Function ----------
def check_coffee_temperature(temp):
    if temp >= 85:
        raise TooHotCoffeeCup("Too Hot Coffee Cup: Temperature is 85 or above.")
    elif temp <= 65:
        raise TooColdCoffeeCup("Too Cold Coffee Cup: Temperature is 65 or below.")
    else:
        return f"Coffee temperature {temp} is within normal range (66-84)."

# ---------- GUI - COLOURFUL THEME ----------
NAVY = "#1F3A5F"
SLATE = "#E9EDF2"
WHITE = "#FFFFFF"
TEAL = "#0E7C7B"
DARK_TEXT = "#1F2937"
GREY_TEXT = "#6B7280"
RED = "#B91C1C"
GREEN = "#047857"

# New Colourful Colours
ORANGE = "#F97316"
PINK = "#EC4899"
PURPLE = "#7C3AED"
SKY = "#0EA5E9"
YELLOW_BG = "#FEF3C7"
LIGHT_PINK_BG = "#FCE7F3"
LIGHT_BLUE_BG = "#DBEAFE"
LIGHT_GREEN_BG = "#D1FAE5"

root = tk.Tk()
root.title("Lab 8 - Q1: Coffee Temperature Checker")
root.geometry("430x520")
root.configure(bg="#C7D2FE")  # Light Lavender Background
root.resizable(False, False)

# ---------- HEADER - Colourful Gradient Look ----------
header = tk.Frame(root, bg=NAVY, height=90)
header.pack(fill="x")
tk.Label(header, text="☕ Coffee Temperature Checker", font=("Segoe UI", 16, "bold"), bg=NAVY, fg="#FDE68A").pack(pady=(15, 0))
tk.Label(header, text="Lab 8  |  Q1  |  SE-3102", font=("Segoe UI", 10, "bold"), bg=NAVY, fg="#FBCFE8").pack(pady=(2, 0))
tk.Label(header, text="Too Hot  🔥   |   Perfect  ☕   |   Too Cold  ❄️", font=("Segoe UI", 9), bg=NAVY, fg="white").pack(pady=(2, 0))

# ---------- CARD ----------
card = tk.Frame(root, bg=WHITE, padx=25, pady=20, highlightbackground="#A78BFA", highlightthickness=2)
card.pack(fill="x", padx=25, pady=20)

tk.Label(card, text="Enter Coffee Temperature", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=PURPLE).pack(anchor="w")
tk.Label(card, text="Normal Range: 66 - 84 degrees", font=("Segoe UI", 10, "bold"), bg=WHITE, fg=SKY).pack(anchor="w", pady=(2, 12))

temp_entry = tk.Entry(card, font=("Segoe UI", 16, "bold"), justify="center", relief="solid", bd=2, bg="#FFF7ED", fg="#7C2D12", highlightbackground=ORANGE, highlightthickness=1)
temp_entry.pack(fill="x", pady=5)

# ---------- RESULT BOX - Colour Changes With Result ----------
result_frame = tk.Frame(card, bg=YELLOW_BG, padx=10, pady=10)
result_frame.pack(fill="x", pady=(15, 5))

result_label = tk.Label(result_frame, text="Status: Waiting for input ⏳", font=("Segoe UI", 11, "bold"), bg=YELLOW_BG, fg="#92400E", wraplength=320)
result_label.pack()

def on_check():
    try:
        temp = float(temp_entry.get())
        message = check_coffee_temperature(temp)
        # Normal = Green Box
        result_frame.config(bg=LIGHT_GREEN_BG)
        result_label.config(bg=LIGHT_GREEN_BG, text=f"Success: {message} ✅", fg=GREEN)
    except TooHotCoffeeCup as e:
        # Too Hot = Red / Orange Box
        result_frame.config(bg="#FEE2E2")
        result_label.config(bg="#FEE2E2", text=f"Exception: {e} 🔥", fg=RED)
        messagebox.showerror("Too Hot Coffee Cup", str(e))
    except TooColdCoffeeCup as e:
        # Too Cold = Blue Box
        result_frame.config(bg=LIGHT_BLUE_BG)
        result_label.config(bg=LIGHT_BLUE_BG, text=f"Exception: {e} ❄️", fg="#1D4ED8")
        messagebox.showerror("Too Cold Coffee Cup", str(e))
    except ValueError:
        result_frame.config(bg=LIGHT_PINK_BG)
        result_label.config(bg=LIGHT_PINK_BG, text="Invalid Input: Please enter a number. ⚠️", fg=RED)
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")

def on_clear():
    temp_entry.delete(0, tk.END)
    result_frame.config(bg=YELLOW_BG)
    result_label.config(bg=YELLOW_BG, text="Status: Waiting for input ⏳", fg="#92400E")

# ---------- COLOURFUL BUTTONS ----------
tk.Button(card, text="🔍  Check Temperature", font=("Segoe UI", 12, "bold"), bg=ORANGE, fg=WHITE, activebackground="#EA580C", activeforeground=WHITE, relief="flat", padx=20, pady=10, cursor="hand2", command=on_check).pack(fill="x", pady=(10, 8))

tk.Button(card, text="🧹  Clear", font=("Segoe UI", 11, "bold"), bg=PINK, fg=WHITE, activebackground="#DB2777", activeforeground=WHITE, relief="flat", padx=20, pady=8, cursor="hand2", command=on_clear).pack(fill="x")

# ---------- BOTTOM COLOURFUL LEGEND ----------
legend = tk.Frame(root, bg="white", padx=10, pady=10, highlightbackground="#F472B6", highlightthickness=1)
legend.pack(fill="x", padx=25, pady=5)

tk.Label(legend, text="🔥  >= 85 : Too Hot", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#DC2626").pack(anchor="w")
tk.Label(legend, text="☕  66 - 84 : Perfect", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#059669").pack(anchor="w")
tk.Label(legend, text="❄️  <= 65 : Too Cold", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#2563EB").pack(anchor="w")

tk.Label(root, text="Standard: 66-84  |  >= 85: Too Hot  |  <= 65: Too Cold", font=("Segoe UI", 9, "bold"), bg="#C7D2FE", fg=NAVY).pack(pady=5)

root.mainloop()