import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_half_page(pdf, page_num, half='top'):
    page = pdf.load_page(page_num)
    width, height = page.rect.width, page.rect.height
    if half == 'top':
        clip_rect = fitz.Rect(0, 0, width, height / 2)
    else:
        clip_rect = fitz.Rect(0, height / 2, width, height)
    
    new_pdf = fitz.open()
    new_page = new_pdf.new_page(width=width, height=height / 2)
    new_page.show_pdf_page(fitz.Rect(0, 0, width, height / 2), pdf, page_num, clip=clip_rect)
    
    return new_pdf

def create_combined_page(top_half_pdf, bottom_half_pdf, width, height):
    combined_pdf = fitz.open()
    new_page = combined_pdf.new_page(width=width, height=height)
    new_page.show_pdf_page(fitz.Rect(0, 0, width, height / 2), top_half_pdf, 0)
    new_page.show_pdf_page(fitz.Rect(0, height / 2, width, height), bottom_half_pdf, 0)
    return combined_pdf

def insert_combined_pages(input_pdf_path, output_pdf_path):
    pdf = fitz.open(input_pdf_path)
    output_pdf = fitz.open()
    for i in range(len(pdf) - 1):
        output_pdf.insert_pdf(pdf, from_page=i, to_page=i)
        bottom_half_pdf = extract_half_page(pdf, i, half='bottom')
        top_half_pdf = extract_half_page(pdf, i + 1, half='top')
        width, height = pdf[i].rect.width, pdf[i].rect.height
        combined_page_pdf = create_combined_page(top_half_pdf, bottom_half_pdf, width, height)
        output_pdf.insert_pdf(combined_page_pdf)
    output_pdf.insert_pdf(pdf, from_page=len(pdf) - 1, to_page=len(pdf) - 1)
    output_pdf.save(output_pdf_path)

def import_pdf():
    input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if input_file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, input_file)

def export_pdf():
    if not input_entry.get():
        messagebox.showerror("Error", "Please import a PDF file first.")
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_file:
        insert_combined_pages(input_entry.get(), output_file)
        messagebox.showinfo("Success", "PDF has been processed and saved successfully!")

# Setup tkinter GUI
root = tk.Tk()
root.title("ScoreFlip")

input_label = tk.Label(root, text="Import PDF:")
input_label.pack(pady=5)

input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)

import_button = tk.Button(root, text="Import PDF", command=import_pdf)
import_button.pack(pady=5)

export_button = tk.Button(root, text="Download PDF", command=export_pdf)
export_button.pack(pady=5)

root.mainloop()
