import tkinter as tk
from tkinter import ttk
from diagnostics import Diagnostics

# Create the main application window
root = tk.Tk()
root.title("Medical Diagnostics")

# Set the window size
root.geometry("400x300")
bn = Diagnostics()

# Function to handle dropdown selection
def on_selection():
    disease, p_disease =bn.diagnose(asia_var.get(), smoking_var.get(), xray_var.get(), dyspnea_var.get())
    diagnosis = f"{disease} with chance {p_disease*100:.2f}%"
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, diagnosis)

# Variables to store dropdown selections
asia_var = tk.StringVar(value="NA")
smoking_var = tk.StringVar(value="NA")
xray_var = tk.StringVar(value="NA")
dyspnea_var = tk.StringVar(value="NA")

# Create labels and dropdowns for variables
ttk.Label(root, text="Visit to Asia").grid(row=0, column=0, padx=10, pady=10, sticky="w")
asia_dropdown = ttk.Combobox(root, textvariable=asia_var, values=["NA", "Yes", "No"], state="readonly")
asia_dropdown.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Smoking").grid(row=1, column=0, padx=10, pady=10, sticky="w")
smoking_dropdown = ttk.Combobox(root, textvariable=smoking_var, values=["NA", "Yes", "No"], state="readonly")
smoking_dropdown.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(root, text="Xray").grid(row=2, column=0, padx=10, pady=10, sticky="w")
xray_dropdown = ttk.Combobox(root, textvariable=xray_var, values=["NA", "Abnormal", "Normal"], state="readonly")
xray_dropdown.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(root, text="Dyspnea").grid(row=3, column=0, padx=10, pady=10, sticky="w")
dyspnea_dropdown = ttk.Combobox(root, textvariable=dyspnea_var, values=["NA", "Present", "Absent"], state="readonly")
dyspnea_dropdown.grid(row=3, column=1, padx=10, pady=10)


# Button to update the textbox based on dropdown selections
diagnose_button = ttk.Button(root, text="Diagnose", command=on_selection)
diagnose_button.grid(row=4, column=0, pady=10)

# Create a textbox
#ttk.Label(root, text="Diagnosis").grid(row=4, column=0, padx=10, pady=10, sticky="w")
textbox = tk.Text(root, height=1, width=35)
textbox.grid(row=4, column=1, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
