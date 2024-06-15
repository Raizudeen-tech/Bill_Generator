import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import webbrowser

BILL_NUMBER_FILE = "bill_number.txt"

# Load the bill number from file
def load_bill_number():
    if os.path.exists(BILL_NUMBER_FILE):
        with open(BILL_NUMBER_FILE, "r") as file:
            return int(file.read())
    return 1

# Save the bill number to file
def save_bill_number(bill_number):
    with open(BILL_NUMBER_FILE, "w") as file:
        file.write(str(bill_number))

# Initialize the bill number
bill_number = load_bill_number()

def generate_bill():
    global bill_number

    # Get the values from the input fields
    student_name = student_name_var.get()
    admission_number = admission_number_var.get()
    grade = grade_var.get()
    monthly_fee = monthly_fee_var.get()
    book_fee = book_fee_var.get() or "0"
    admission_fee = admission_fee_var.get() or "0"
    fees_due = fees_due_var.get() or "0"
    paid_amount = paid_amount_var.get()
    year = year_var.get()
    month = month_var.get()

    # Check if required fields are filled
    if not student_name or not admission_number or not grade or not monthly_fee or not paid_amount or not year or not month:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Convert fee values to float
    monthly_fee = float(monthly_fee)
    book_fee = float(book_fee)
    admission_fee = float(admission_fee)
    fees_due = float(fees_due)
    paid_amount = float(paid_amount)

    total_amount = monthly_fee + book_fee + admission_fee + fees_due
    balance = total_amount - paid_amount
    
    bill_number += 1  # Increment bill number
    save_bill_number(bill_number)  # Save updated bill number

    save_pdf(admission_number, student_name, grade, monthly_fee, book_fee, admission_fee, fees_due, total_amount, paid_amount, balance, year, month)
    messagebox.showinfo("Bill Generated", f"Bill for {student_name} has been generated and saved as PDF.")
    open_pdf(admission_number, grade)

def save_pdf(admission_number, student_name, grade, monthly_fee, book_fee, admission_fee, fees_due, total_amount, paid_amount, balance, year, month):
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    bill_directory = os.path.join(desktop, 'bill')

    # Create directory structure
    directory = os.path.join(bill_directory, str(year), month, f"Grade {grade}")
    os.makedirs(directory, exist_ok=True)
    
    # File path for the PDF
    file_path = os.path.join(directory, f"{admission_number}.pdf")
    
    # Create PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Draw header
    c.setFont("Helvetica", 18)
    c.drawCentredString(4.25 * inch, 9.75 * inch, "Nappinai Matriculation School")
    c.setFont("Helvetica", 12)
    c.drawCentredString(4.25 * inch, 9.5 * inch, "No 15, Ranganatha Swamy 1st Street, Lakshmipuram, Chrompet, Chennai - 44")
    c.line(0.5 * inch, 9.4 * inch, 7.9 * inch, 9.4 * inch)

    # Student and bill details
    c.drawString(0.5 * inch, 9.1 * inch, f"Admission Number: {admission_number}")
    c.drawString(0.5 * inch, 8.9 * inch, f"Student Name: {student_name}")
    c.drawString(0.5 * inch, 8.7 * inch, f"Grade: {grade}")
    c.drawString(0.5 * inch, 8.5 * inch, f"Year: {year}")
    c.drawString(0.5 * inch, 8.3 * inch, f"Month: {month}")
    c.drawRightString(7.9 * inch, 9.1 * inch, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawRightString(7.9 * inch, 8.9 * inch, f"Bill Number: {bill_number - 1}")
    c.line(0.5 * inch, 8.2 * inch, 7.9 * inch, 8.2 * inch)

    # Fee details
    c.drawString(0.5 * inch, 8.0 * inch, "Fees Details")
    c.drawString(0.5 * inch, 7.8 * inch, "Monthly Fees:")
    c.drawRightString(7.9 * inch, 7.8 * inch, f"Rs. {monthly_fee:.2f}")
    c.drawString(0.5 * inch, 7.6 * inch, "Book Fee:")
    c.drawRightString(7.9 * inch, 7.6 * inch, f"Rs. {book_fee:.2f}")
    c.drawString(0.5 * inch, 7.4 * inch, "Admission Fee:")
    c.drawRightString(7.9 * inch, 7.4 * inch, f"Rs. {admission_fee:.2f}")
    c.drawString(0.5 * inch, 7.2 * inch, "Fees Due:")
    c.drawRightString(7.9 * inch, 7.2 * inch, f"Rs. {fees_due:.2f}")
    c.line(0.5 * inch, 7.0 * inch, 7.9 * inch, 7.0 * inch)
    c.drawString(0.5 * inch, 6.8 * inch, "Total Amount:")
    c.drawRightString(7.9 * inch, 6.8 * inch, f"Rs. {total_amount:.2f}")
    c.drawString(0.5 * inch, 6.6 * inch, "Paid Amount:")
    c.drawRightString(7.9 * inch, 6.6 * inch, f"Rs. {paid_amount:.2f}")
    c.drawString(0.5 * inch, 6.4 * inch, "Balance:")
    c.drawRightString(7.9 * inch, 6.4 * inch, f"Rs. {balance:.2f}")

    # Finalize and save the PDF
    c.showPage()
    c.save()

def open_pdf(admission_number, grade):
    # Open the PDF in the default browser
    now = datetime.now()
    month = now.strftime("%B")
    directory = os.path.join(str(year_var.get()), month_var.get(), f"Grade {grade}")
    file_path = os.path.join(directory, f"{admission_number}.pdf")
    webbrowser.open_new(f"file://{os.path.realpath(file_path)}")

# Create the main window
root = tk.Tk()
root.title("School Fee Bill Generator: ")
root.geometry("400x520")  # Set window size

# Create StringVar variables for user input
student_name_var = tk.StringVar()
admission_number_var = tk.StringVar()
grade_var = tk.StringVar()
monthly_fee_var = tk.StringVar()
book_fee_var = tk.StringVar()
admission_fee_var = tk.StringVar()
fees_due_var = tk.StringVar()
paid_amount_var = tk.StringVar()
year_var = tk.StringVar()
month_var = tk.StringVar()

# Year and month options
now = datetime.now()
current_year = now.year
current_month = now.strftime("%B")
years = list(range(current_year - 5, current_year + 6))
months = [
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
]

# Create and place labels and entry fields
fields = [
    ("Student Name *", student_name_var),
    ("Admission Number *", admission_number_var),
    ("Grade *", grade_var),
    ("Monthly Fee *", monthly_fee_var),
    ("Book Fee", book_fee_var),
    ("Admission Fee", admission_fee_var),
    ("Fees Due", fees_due_var),
    ("Paid Amount *", paid_amount_var),
    ("Year *", year_var),
    ("Month *", month_var),
]

for i, (label, var) in enumerate(fields):
    if label == "Grade *":
        ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=(10, 5), sticky="w")
        grade_options = ["LKG", "UKG", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        ttk.Combobox(root, textvariable=var, values=grade_options).grid(row=i, column=1, padx=10, pady=(10, 5), sticky="ew")
    elif label in ["Year *", "Month *"]:
        ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=(10, 5), sticky="w")
        ttk.Combobox(root, textvariable=var, values=years if label == "Year *" else months).grid(row=i, column=1, padx=10, pady=(10, 5), sticky="ew")
    else:
        ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5, sticky="ew")

# Create and place the generate bill button
ttk.Button(root, text="Generate Bill", command=generate_bill).grid(row=len(fields), columnspan=2, pady=20)

# Start the GUI event loop
root.mainloop()