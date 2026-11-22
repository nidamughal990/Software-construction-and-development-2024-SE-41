# Lab 8 - Question 2
# Course: SE-3102 Software Construction & Development (Lab)
# Topic: Custom Exceptions

import tkinter as tk
from tkinter import messagebox

# ---------- Custom Exceptions ----------
class LowHemoglobin(Exception):
    pass

class HighHemoglobin(Exception):
    pass

# ---------- Logic Function ----------
def check_hemoglobin(category, hb):
    ranges = {
        "men": (14, 18),
        "women": (12, 16),
        "children": (11, 16)
    }
    low, high = ranges[category]

    if hb < low:
        raise LowHemoglobin(f"Low Hemoglobin: {hb} g/dL is below normal range {low}-{high} g/dL for {category}.")
    elif hb > high:
        raise HighHemoglobin(f"High Hemoglobin: {hb} g/dL is above normal range {low}-{high} g/dL for {category}.")
    else:
        return f"Hemoglobin {hb} g/dL is NORMAL for {category} (Range: {low}-{high} g/dL)."

# ---------- GUI - BRIGHT COLOURFUL THEME ----------
NAVY = "#1F3A5F"
WHITE = "#FFFFFF"
DARK_TEXT = "#1F2937"
GREY_TEXT = "#6B7280"
RED = "#B91C1C"
GREEN = "#047857"

# New Bright Colours
BRIGHT_PINK = "#EC4899"
BRIGHT_ORANGE = "#F97316"
BRIGHT_PURPLE = "#7C3AED"
BRIGHT_BLUE = "#2563EB"
BRIGHT_TEAL = "#06B6D4"
BRIGHT_YELLOW = "#FACC15"
LIGHT_PINK_BG = "#FCE7F3"
LIGHT_BLUE_BG = "#DBEAFE"
LIGHT_GREEN_BG = "#D1FAE5"
LIGHT_YELLOW_BG = "#FEF3C7"
LIGHT_PURPLE_BG = "#EDE9FE"

root = tk.Tk()
root.title("Lab 8 - Q2: Hemoglobin Checker")
root.geometry("430x600")
root.configure(bg="#FBCFE8")  # Bright Light Pink Background
root.resizable(False, False)

# ---------- HEADER - Bright ----------
header = tk.Frame(root, bg=NAVY, height=90)
header.pack(fill="x")
tk.Label(header, text="🩸 Hemoglobin (Hb) Checker", font=("Segoe UI", 16, "bold"), bg=NAVY, fg="#FDE68A").pack(pady=(15, 0))
tk.Label(header, text="Lab 8  |  Q2  |  SE-3102", font=("Segoe UI", 10, "bold"), bg=NAVY, fg="#FBCFE8").pack(pady=(2, 0))
tk.Label(header, text="Low  ↓   |   Normal  ✓   |   High  ↑", font=("Segoe UI", 9, "bold"), bg=NAVY, fg="white").pack(pady=(2, 0))

# ---------- CARD ----------
card = tk.Frame(root, bg=WHITE, padx=25, pady=20, highlightbackground="#EC4899", highlightthickness=2)
card.pack(fill="x", padx=25, pady=20)

tk.Label(card, text="Select Category", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=BRIGHT_PURPLE).pack(anchor="w")

selected = tk.StringVar(value="women")
cat_frame = tk.Frame(card, bg=WHITE)
cat_frame.pack(fill="x", pady=(8, 12))

# Radio Buttons - Har ek ka alag Bright Colour
tk.Radiobutton(cat_frame, text="👨 Men", variable=selected, value="men",
               bg=WHITE, fg=BRIGHT_BLUE, font=("Segoe UI", 10, "bold"), selectcolor="#BFDBFE", activebackground=WHITE).pack(side="left", padx=(0, 12))

tk.Radiobutton(cat_frame, text="👩 Women", variable=selected, value="women",
               bg=WHITE, fg=BRIGHT_PINK, font=("Segoe UI", 10, "bold"), selectcolor="#FBCFE8", activebackground=WHITE).pack(side="left", padx=(0, 12))

tk.Radiobutton(cat_frame, text="🧒 Children", variable=selected, value="children",
               bg=WHITE, fg="#059669", font=("Segoe UI", 10, "bold"), selectcolor="#A7F3D0", activebackground=WHITE).pack(side="left")

tk.Label(card, text="Enter Hemoglobin Level (g/dL)", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=BRIGHT_PURPLE).pack(anchor="w", pady=(5, 0))
tk.Label(card, text="Men: 14-18  |  Women: 12-16  |  Children: 11-16", font=("Segoe UI", 10, "bold"), bg=WHITE, fg=BRIGHT_BLUE).pack(anchor="w", pady=(2, 12))

hb_entry = tk.Entry(card, font=("Segoe UI", 16, "bold"), justify="center", relief="solid", bd=2, bg="#FFF7ED", fg="#7C2D12", highlightbackground=BRIGHT_ORANGE, highlightthickness=1)
hb_entry.pack(fill="x", pady=5)

# ---------- RESULT BOX - Colour Changes With Result ----------
result_frame = tk.Frame(card, bg=LIGHT_YELLOW_BG, padx=10, pady=10)
result_frame.pack(fill="x", pady=(15, 5))

result_label = tk.Label(result_frame, text="Status: Waiting for input ⏳", font=("Segoe UI", 11, "bold"), bg=LIGHT_YELLOW_BG, fg="#92400E", wraplength=320)
result_label.pack()

def on_check():
    try:
        category = selected.get()
        hb = float(hb_entry.get())
        message = check_hemoglobin(category, hb)
        # Normal = Green Box
        result_frame.config(bg=LIGHT_GREEN_BG)
        result_label.config(bg=LIGHT_GREEN_BG, text=f"Success: {message} ✅", fg=GREEN)
    except LowHemoglobin as e:
        # Low = Light Blue Box
        result_frame.config(bg=LIGHT_BLUE_BG)
        result_label.config(bg=LIGHT_BLUE_BG, text=f"Exception: {e} ↓", fg="#1D4ED8")
        messagebox.showerror("Low Hemoglobin", str(e))
    except HighHemoglobin as e:
        # High = Light Pink / Red Box
        result_frame.config(bg="#FEE2E2")
        result_label.config(bg="#FEE2E2", text=f"Exception: {e} ↑", fg=RED)
        messagebox.showerror("High Hemoglobin", str(e))
    except ValueError:
        result_frame.config(bg=LIGHT_PINK_BG)
        result_label.config(bg=LIGHT_PINK_BG, text="Invalid Input: Please enter a number. ⚠️", fg=RED)
        messagebox.showwarning("Invalid Input", "Please enter a valid number for Hb.")

def on_clear():
    hb_entry.delete(0, tk.END)
    result_frame.config(bg=LIGHT_YELLOW_BG)
    result_label.config(bg=LIGHT_YELLOW_BG, text="Status: Waiting for input ⏳", fg="#92400E")

# ---------- BRIGHT BUTTONS ----------
tk.Button(card, text="🔍  Check Hemoglobin", font=("Segoe UI", 12, "bold"), bg=BRIGHT_PINK, fg=WHITE, activebackground="#DB2777", activeforeground=WHITE, relief="flat", padx=20, pady=10, cursor="hand2", command=on_check).pack(fill="x", pady=(10, 8))
tk.Button(card, text="🧹  Clear", font=("Segoe UI", 11, "bold"), bg=BRIGHT_ORANGE, fg=WHITE, activebackground="#EA580C", activeforeground=WHITE, relief="flat", padx=20, pady=8, cursor="hand2", command=on_clear).pack(fill="x")

# ---------- BOTTOM BRIGHT LEGEND ----------
legend = tk.Frame(root, bg=WHITE, padx=12, pady=10, highlightbackground="#A78BFA", highlightthickness=1)
legend.pack(fill="x", padx=25, pady=5)

tk.Label(legend, text="🔵  Low  = Below Normal Range", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#2563EB").pack(anchor="w")
tk.Label(legend, text="🟢  Normal  = Within Range", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#059669").pack(anchor="w")
tk.Label(legend, text="🔴  High  = Above Normal Range", font=("Segoe UI", 10, "bold"), bg=WHITE, fg="#DC2626").pack(anchor="w")

tk.Label(root, text="If level is not within range, appropriate exception is thrown.", font=("Segoe UI", 9, "bold"), bg="#FBCFE8", fg=NAVY).pack(pady=5)

root.mainloop()