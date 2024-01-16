import json
import tkinter as tk
from tkinter import filedialog, messagebox

def transform_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    transformed_data = {'idioms': []}
    idioms = data.get('idioms', [])

    for i in range(0, len(idioms) - 1, 2):  # Ensure we don't go out of range
        if 'phrase' in idioms[i] and 'context' in idioms[i+1]:
            phrase = idioms[i]['phrase']
            context = idioms[i+1]['context']
            transformed_data['idioms'].append({'phrase': phrase, 'context': context})

    with open(output_file, 'w') as f:
        json.dump(transformed_data, f)

    messagebox.showinfo("Success", "File was successfully converted and saved.")

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    input_file = filedialog.askopenfilename(title="Select input file", filetypes=[("JSON files", "*.json")])
    output_file = filedialog.asksaveasfilename(title="Select output file", defaultextension=".json", filetypes=[("JSON files", "*.json")])

    if input_file and output_file:  # Check if files were selected
        transform_json(input_file, output_file)

if __name__ == "__main__":
    select_files()