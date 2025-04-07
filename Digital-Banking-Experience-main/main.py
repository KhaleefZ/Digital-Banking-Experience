import mysql.connector
from tkinter import *
import tkinter.messagebox
import math, random
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mani@2133044",
    auth_plugin='mysql_native_password',
    database="bank"
)
cur = db.cursor()


def perform_transaction():
    sender_account_number = entry_sender_account.get()
    receiver_account_number = entry_receiver_account.get()
    amount = float(entry_amount.get())

    try:
        # Check if sender's account exists in the bank
        sql = "SELECT account_holder_name FROM acn WHERE account_number = %s"
        values = (sender_account_number,)

        cur.execute(sql, values)
        sender_row = cur.fetchone()

        if sender_row is None:
            messagebox.showerror("Error", "Sender's account does not exist in the bank.")
            return

        # Check if receiver's account exists in the bank
        sql = "SELECT account_holder_name FROM acn WHERE account_number = %s"
        values = (receiver_account_number,)

        cur.execute(sql, values)
        receiver_row = cur.fetchone()

        if receiver_row is None:
            messagebox.showerror("Error", "Receiver's account does not exist in the bank.")
            return

        # Perform the transaction
        # Reduce the amount from the sender's account
        sql = "UPDATE acn SET balance = balance - %s WHERE account_number = %s"
        values = (amount, sender_account_number)
        cur.execute(sql, values)

        # Add the amount to the receiver's account
        sql = "UPDATE acn SET balance = balance + %s WHERE account_number = %s"
        values = (amount, receiver_account_number)
        cur.execute(sql, values)

        messagebox.showinfo("Transaction Successful", "Transaction completed successfully.")

    except mysql.connector.Error as error:
        # Handle any errors that occurred during the transaction
        messagebox.showerror("Error", f"Error performing the transaction: {error}")

    finally:
        # Close the cursor and the database connection
        cur.close()


def show_transaction_history():
    account_number = entry_account_number.get()

    try:
        # Check if the account exists in the bank
        sql = "SELECT account_holder_name FROM acn WHERE account_number = %s"
        values = (account_number,)

        cur.execute(sql, values)
        account_row = cur.fetchone()

        if account_row is None:
            messagebox.showerror("Error", "Account does not exist in the bank.")
            return

        # Fetch the transaction history for the account
        sql = "SELECT * FROM transaction WHERE sender_account_number = %s OR receiver_account_number = %s"
        values = (account_number, account_number)

        cur.execute(sql, values)
        transaction_rows = cur.fetchall()

        # Display the transaction history in a message box
        history = "Transaction History:\n\n"
        for row in transaction_rows:
            transaction_id, sender_account, receiver_account, amount, date_time = row
            transaction_info = f"Transaction ID: {transaction_id}\nSender Account: {sender_account}\nReceiver Account: {receiver_account}\nAmount: {amount}\nDate & Time: {date_time}\n\n"
            history += transaction_info

        messagebox.showinfo("Transaction History", history)

    except mysql.connector.Error as error:
        # Handle any errors that occurred during fetching the transaction history
        messagebox.showerror("Error", f"Error fetching the transaction history: {error}")

    finally:
        # Close the cursor and the database connection
        cur.close()


def transactions():
    root = tk.Tk()
    root.title("Bank Transaction")

    global entry_sender_account
    global entry_receiver_account
    global entry_amount
    global entry_account_number

    # Create labels and entry fields for sender and receiver account numbers
    label_sender_account = tk.Label(root, text="Sender's Account Number:")
    label_sender_account.pack()
    entry_sender_account = tk.Entry(root)
    entry_sender_account.pack()

    label_receiver_account = tk.Label(root, text="Receiver's Account Number:")
    label_receiver_account.pack()
    entry_receiver_account = tk.Entry(root)
    entry_receiver_account.pack()

    # Create a label and an entry field for the transaction amount
    label_amount = tk.Label(root, text="Amount:")
    label_amount.pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    # Create a button to trigger the transaction
    button_perform_transaction = tk.Button(root, text="Perform Transaction", command=perform_transaction)
    button_perform_transaction.pack()

    # Create a separator
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    # Create labels and an entry field for account number to show transaction history
    label_account_number = tk.Label(root, text="Account Number:")
    label_account_number.pack()
    entry_account_number = tk.Entry(root)
    entry_account_number.pack()

    # Create a button to show transaction history
    button_show_history = tk.Button(root, text="Show Transaction History", command=show_transaction_history)
    button_show_history.pack()


def profilePage():
    global root3
    root3 = Toplevel()
    root3.title("Profile Page")

    profile_text = Text(root3, width=50, height=25)
    profile_text.pack()
    usn = user_verify
    cur.execute("SELECT * FROM user WHERE username = %s", (usn,))
    data = cur.fetchone()

    if data:
        profile_text.insert(END, f"Username: {data[0]}\n")
        profile_text.insert(END, f"Account_no: {data[1]}\n")
        profile_text.insert(END, f"First Name: {data[2]}\n")
        profile_text.insert(END, f"Last Name: {data[3]}\n")
        profile_text.insert(END, f"Phone Number: {data[4]}\n")
        profile_text.insert(END, f"Email: {data[5]}\n")
        profile_text.insert(END, f"Gender: {data[6]}\n")
        profile_text.insert(END, f"Date of Birth: {data[7]}\n")
        profile_text.insert(END, f"Account Type: {data[8]}\n")
        profile_text.insert(END, f"Aadhar Number: {data[9]}\n")
        profile_text.insert(END, f"PAN Number: {data[10]}\n")
        profile_text.insert(END, f"Door Number: {data[11]}\n")
        profile_text.insert(END, f"Street: {data[12]}\n")
        profile_text.insert(END, f"Area: {data[13]}\n")
        profile_text.insert(END, f"District: {data[14]}\n")
        profile_text.insert(END, f"Pincode: {data[15]}\n")

    else:
        print("User with customer ID", y, "not found.")

    profile_text.configure(state='disabled')


def loancal():
    global root6
    root6 = Toplevel()
    root6.title("Loan Calculator")

    Label(root6, text="Loan Calculator", bg="grey", fg="black", font="bold", width=20).grid(row=0, columnspan=2,
                                                                                            pady=10)

    global Annual_Interest_Rate
    global Number_of_years
    global loan_amount
    global monthly_payment
    global total_payment

    Annual_Interest_Rate = StringVar()
    Number_of_years = StringVar()
    loan_amount = StringVar()
    monthly_payment = StringVar()
    total_payment = StringVar()

    Label(root6, text="Annual Interest Rate:", font="bold").grid(row=1, column=0, padx=10, sticky="e")
    Entry(root6, width=35, textvariable=Annual_Interest_Rate).grid(row=1, column=1)

    Label(root6, text="Number of Years:", font="bold").grid(row=2, column=0, padx=10, sticky="e")
    Entry(root6, width=35, textvariable=Number_of_years).grid(row=2, column=1)

    Label(root6, text="Loan Amount:", font="bold").grid(row=3, column=0, padx=10, sticky="e")
    Entry(root6, width=35, textvariable=loan_amount).grid(row=3, column=1)

    Label(root6, text="Monthly Payment:", font="bold").grid(row=4, column=0, padx=10, sticky="e")
    Entry(root6, width=35, textvariable=monthly_payment).grid(row=4, column=1)

    Label(root6, text="Total Payment:", font="bold").grid(row=5, column=0, padx=10, sticky="e")
    Entry(root6, width=35, textvariable=total_payment).grid(row=5, column=1)

    Button(root6, text='Calculate', width=20, bg='brown', fg='white', command=computePayment).grid(row=6, column=1,
                                                                                                   pady=10)


def computePayment():
    monthlyPayment = getMonthlyPayment(
        float(loan_amount.get()),
        float(Annual_Interest_Rate.get()) / 1200,
        int(Number_of_years.get()))

    monthly_payment.set(format(monthlyPayment, '10.2f'))
    total_payment.set(format(monthlyPayment * 12 * int(Number_of_years.get()), '10.2f'))


def getMonthlyPayment(loan_amount, monthlyInterestRate, Number_of_years):
    monthlyPayment = loan_amount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (Number_of_years * 12))
    return monthlyPayment


def clear():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    textcomment.delete("1.0", tk.END)
    tkinter.messagebox.showinfo(title='Clear', message='Form cleared successfully.')


def submit():
    name = entry_name.get()
    email = entry_email.get()
    comment = textcomment.get("1.0", tk.END)

    print('Name: {}'.format(name))
    print('Email: {}'.format(email))
    print('Comment: {}'.format(comment))

    tkinter.messagebox.showinfo(title='Submit', message='Thank you for your feedback. Comments submitted successfully.')

    clear()


def feedback_form():
    root = Toplevel()
    root.title("Feedback Form")

    frame_header = ttk.Frame(root)
    frame_header.pack()
    header_label = ttk.Label(frame_header, text='Feedback Form', font=('Arial', 24))
    header_label.grid(row=0, column=1)
    message_label = ttk.Label(frame_header, text='Let us know what you think', font=('Arial', 10))
    message_label.grid(row=1, column=1)

    frame_content = ttk.Frame(root)
    frame_content.pack()

    namelabel = ttk.Label(frame_content, text='Name')
    namelabel.grid(row=0, column=0, padx=5, sticky='sw')
    global entry_name
    entry_name = ttk.Entry(frame_content, width=18, font=('Arial', 14))
    entry_name.grid(row=1, column=0)

    emaillabel = ttk.Label(frame_content, text='Email')
    emaillabel.grid(row=0, column=1, sticky='sw')
    global entry_email
    entry_email = ttk.Entry(frame_content, width=18, font=('Arial', 14))
    entry_email.grid(row=1, column=1)

    commentlabel = ttk.Label(frame_content, text='Comment', font=('Arial', 10))
    commentlabel.grid(row=2, column=0, sticky='sw')
    global textcomment
    textcomment = tk.Text(frame_content, width=55, height=10)
    textcomment.grid(row=3, column=0, columnspan=2)
    textcomment.config(wrap='word')

    submit_button = ttk.Button(frame_content, text='Submit', command=submit)
    submit_button.grid(row=4, column=0, sticky='e')

    clear_button = ttk.Button(frame_content, text='Clear', command=clear)
    clear_button.grid(row=4, column=1, sticky='w')


def customernum():
    global y
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP = ""
    for i in range(11):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


y = customernum()
print("Customer ID:", y)


def userinsert():
    un = username.get()
    ci = y
    fn = Fn.get()
    ln = Ln.get()
    pnm = pn.get()
    Em = em.get()
    G = var.get()
    b = da.get()
    act = t.get()
    adn = an.get()
    pa = Pn.get()
    Dn = dn.get()
    St = st.get()
    A = a.get()
    Ds = ds.get()
    Pc = pc.get()
    cur.execute(
        "insert into user(username,customer_id,First_Name,Last_Name,Ph_No,Email,Gender,DOB,Account_type,Aadhar_num,Pan_num,Door_no,Street,Area,District,Pincode)values('" + un + "'," + ci + ",'" + fn + "','" + ln + "','" + pnm + "','" + Em + "','" + G + "','" + b + "','" + act + "','" + adn + "','" + pa + "'," + Dn + ",'" + St + "','" + A + "','" + Ds + "'," + Pc + ")")
    db.commit()


def userdet():
    window = Toplevel()
    rootf = Frame(window)
    rootf1 = Frame(window)
    window.title("Registration form")
    label = Label(rootf, text="Create Account", width=20, font=("bold", 18))
    label.grid(row=0, columnspan=7)

    global Fn
    global Ln
    global pn
    global em
    global var
    global da
    global t
    global an
    global Pn
    global dn
    global st
    global a
    global ds
    global pc

    FName = Label(rootf, text="FirstName", width=20, font=("bold", 10))
    FName.grid(row=1, column=0, pady=10)

    Fn = Entry(rootf)
    Fn.grid(row=1, column=1)

    LName = Label(rootf, text="LastName", width=20, font=("bold", 10))
    LName.grid(row=2, column=0, pady=7)

    Ln = Entry(rootf)
    Ln.grid(row=2, column=1)

    Pno = Label(rootf, text="Phone Number", width=20, font=("bold", 10))
    Pno.grid(row=3, column=0, pady=7)

    pn = Entry(rootf)
    pn.grid(row=3, column=1)

    Mail = Label(rootf, text="Email", width=20, font=("bold", 10))
    Mail.grid(row=4, column=0, pady=7)

    em = Entry(rootf)
    em.grid(row=4, column=1)

    Gender = Label(rootf, text="Gender", width=20, font=("bold", 10))
    Gender.grid(row=5, column=0, pady=7)
    var = StringVar()
    Radiobutton(rootf, text="Male", variable=var, value="Male").grid(row=5, column=1)
    Radiobutton(rootf, text="Female", variable=var, value="Female").grid(row=5, column=2)

    dob = Label(rootf, text="DOB", width=20, font=("bold", 10))
    dob.grid(row=6, column=0, pady=7)

    da = StringVar()
    cal = DateEntry(rootf, variable=da, background="magenta3", foreground="white", bd=2)
    cal.grid(row=6, column=1)

    at = Label(rootf, text="Account Type", width=20, font=("bold", 10))
    at.grid(row=7, column=0, pady=7)

    t = StringVar()
    t.set("--Select--")
    e5 = OptionMenu(rootf, t, "Savings", "Current")
    e5.grid(row=7, column=1)

    adh = Label(rootf, text="Aadhar Number", width=20, font=("bold", 10))
    adh.grid(row=8, column=0, pady=7)

    an = Entry(rootf)
    an.grid(row=8, column=1)

    pan = Label(rootf, text="Pan Number", width=20, font=("bold", 10))
    pan.grid(row=9, column=0, pady=10)

    Pn = Entry(rootf)
    Pn.grid(row=9, column=1)

    label_0 = Label(rootf1, text="Address details", width=20, font=("bold", 18))
    label_0.grid(row=0, columnspan=5, padx=30)
    dno = Label(rootf1, text="Door No", width=20, font=("bold", 10))
    dno.grid(row=1, column=0, pady=7)
    dn = Entry(rootf1)
    dn.grid(row=1, column=1)
    Street = Label(rootf1, text="Street", width=20, font=("bold", 10))
    Street.grid(row=2, column=0, pady=7)
    st = Entry(rootf1)
    st.grid(row=2, column=1)
    area = Label(rootf1, text="Area", width=20, font=("bold", 10))
    area.grid(row=3, column=0, pady=7)
    a = Entry(rootf1)
    a.grid(row=3, column=1)
    district = Label(rootf1, text="District", width=20, font=("bold", 10))
    district.grid(row=4, column=0, pady=7)
    ds = Entry(rootf1)
    ds.grid(row=4, column=1)
    pincode = Label(rootf1, text="Pincode", width=20, font=("bold", 10))
    pincode.grid(row=5, column=0, pady=7)
    pc = Entry(rootf1)
    pc.grid(row=5, column=1)
    state = Label(rootf1, text="State", width=20, font=("bold", 10))
    state.grid(row=6, column=0, pady=7)
    st = Entry(rootf1)
    st.grid(row=6, column=1)

    def msg():
        tkinter.messagebox.showinfo("Message", "Account created Successfully! Re - login to use your account!.")

    Button(rootf1, text='Submit', width=20, bg='brown', fg='white', command=lambda: [userinsert(), msg()]).grid(row=7,
                                                                                                                columnspan=6,
                                                                                                                pady=10)
    Button(rootf1, text='Login', width=20, bg='brown', fg='white', command=lambda: [window.destroy(), login()]).grid(
        row=8, columnspan=6,
        pady=7)
    rootf.grid(row=0, column=0, padx=100)
    rootf1.grid(row=0, column=1, padx=200)


def atmblock1():
    root7 = Toplevel()
    root7.geometry("1200x800")
    root7.title("")
    Label(root7, text="Block ATM Form", bg="grey", fg="black", font="bold", width=300).pack()
    desiredamt = Label(root7,
                       text="1.If you have misplaced or lost your State Bank ATM cum Debit Card, you can block the card using this functionality.",
                       font="bold")
    desiredamt.place(x=120, y=100)
    ani = Label(root7,
                text="2.Before proceeding ahead, please ensure that you have registered your mobile number with the Bank. ",
                font="bold")
    ani.place(x=120, y=160)
    passw = Label(root7,
                  text="3.If Mobile No. & Account No. are valid, you will receive an OTP on your registered mobile. ",
                  font="bold")
    passw.place(x=120, y=220)
    passw = Label(root7,
                  text="4.Enter the OTP received on your mobile. All cards issued in the account will be displayed (partially masked).",
                  font="bold")
    passw.place(x=120, y=280)
    passw = Label(root7, text="5.Please select the card number you want to block and click on submit button.",
                  font="bold")
    passw.place(x=120, y=340)
    cau = Label(root7, text="6.Caution! Once a card is blocked, you cannot unblock it online.", font="bold")
    cau.place(x=120, y=340)
    Button(root7, text='Next Step', width=20, bg='brown', fg='white',
           command=lambda: [root7.destroy(), atmblock2()]).place(x=500, y=430)


def insertblock():
    an = Accountnumber.get()
    ctr = Country.get()
    Regn = Registeredno.get()
    cur.execute(
        "insert into atm_blocks(Account_no,Country,Registered_no) values (" + an + ",'" + ctr + "'," + Regn + ")")
    db.commit()


def atmblock2():
    global root11
    root11 = Toplevel()
    root11.geometry("1200x800")
    root11.title("Block ATM Card form")
    Label(root11, text="Block ATM Card", bg="grey", fg="black", font="bold", width=300).pack()
    Label(root11, text="Once card is blocked, you can't unlock it online.").pack()

    global Accountnumber
    global Country
    global Registeredno

    accountno = Label(root11, text="Account Number ", font="bold")
    accountno.place(x=460, y=100)

    Accountnumber = Entry(root11, width=35)
    Accountnumber.place(x=720, y=105, width=100)

    count = Label(root11, text="Country ", font="bold")
    count.place(x=460, y=160)

    Country = Entry(root11, width=35)
    Country.place(x=720, y=165, width=100)

    regno = Label(root11, text="Registered Mobile Number", font="bold")
    regno.place(x=460, y=220)

    Registeredno = Entry(root11, width=35)
    Registeredno.place(x=720, y=225, width=100)

    def onClick():
        tkinter.messagebox.showinfo("Message", "Your request has been done shortly.")

    Button(root11, text='Submit', width=20, bg='brown', fg='white', command=lambda: [onClick(), insertblock()]).place(
        x=460, y=290)
    Button(root11, text='Back', width=20, bg='brown', fg='white', command=root11.destroy).place(x=660, y=290)


def loaninsert():
    dl = e1.get()
    ai = e2.get()
    p = purpose.get()
    acn = e4.get()
    mn = e6.get()
    cur.execute(
        "insert into loande(Desiredloanamount,annualincome,purpose,accountno,mobileno) values(" + dl + "," + ai + ",'" + p + "'," + acn + "," + mn + ")")
    db.commit()


def loanwindow():
    root7 = Toplevel()
    root7.geometry("450x500")
    root7.title("Loan application form")
    Label(root7, text="Loan application", bg="grey", fg="black", font="bold", width=300).pack()

    global e1
    global e2
    global purpose
    global e4
    global menu
    global e6

    desiredamt = Label(root7, text="Desired Amount ", font="bold")
    desiredamt.place(x=80, y=130)

    e1 = Entry(root7, width=35)
    e1.place(x=240, y=130, width=150)

    ani = Label(root7, text="Annual Income ", font="bold")
    ani.place(x=80, y=180)

    e2 = Entry(root7, width=35)
    e2.place(x=240, y=180, width=150)

    purs = Label(root7, text="Purpose of loan", font="bold")
    purs.place(x=80, y=230)

    purpose = StringVar()
    purpose.set("--Select--")
    e3 = OptionMenu(root7, purpose, "Home loan", "Auto loan", "Educational loan", "Personal loan",
                    "Loan against securities")
    e3.pack()
    e3.place(x=240, y=230, width=150)

    passw = Label(root7, text="Account Number ", font="bold")
    passw.place(x=80, y=280)

    e4 = Entry(root7, width=35)
    e4.place(x=240, y=280, width=150)

    passw = Label(root7, text="Mobile Number", font="bold")
    passw.place(x=80, y=330)

    e6 = Entry(root7, width=35)
    e6.place(x=240, y=330, width=150)

    def onClick():
        tkinter.messagebox.showinfo("Message", "Your request has been raised successfully.")

    Button(root7, text='Apply', command=lambda: [onClick(), loaninsert()], width=10, bg='brown', fg='white').place(
        x=140,
        y=430)
    Button(root7, text='Back', command=root7.destroy, width=10, bg='brown', fg='white').place(x=250, y=430)


def uinputs():
    global primary
    global options1
    global options2
    global primDD
    global secDD
    global root16
    global secOpt
    primary = [
        'Raise Request',
        'Raise Complaint'
    ]

    options1 = [
        'Decreased Claim Processing'
    ]
    options2 = [
        'MSME Customer',
        'Prepaid Customer',
        'FastTag Customer',
        'Digital Payment'
    ]

    secondary = options1

    root16 = Toplevel(root)
    root16.geometry('500x300')
    root16.title("Customer Request and Complaint")

    rrc = Label(root16, text="Raise Request/Complain", font="bold")
    rrc.place(x=10, y=150)
    primDD = StringVar()
    primDD.set("---Select---")
    primOpt = OptionMenu(root16, primDD, *primary)
    primOpt.pack()
    primOpt.place(x=280, y=95, width=200)

    if primDD.get() == 'Raise Request':
        secondary = options1
    elif primDD.get() == 'Raise Complaint':
        secondary = options2

    rrct = Label(root16, text="Raise Request/Complain Types", font="bold")
    rrct.place(x=10, y=100)
    secDD = StringVar()
    secDD.set("---Select---")
    secOpt = OptionMenu(root16, secDD, *secondary)
    secOpt.pack()
    secOpt.place(x=280, y=145, width=200)
    Button(root16, text='Submit', command=onClick, width=20, bg='brown', fg='white').place(x=150, y=200)
    primDD.trace("w", change_optionmenu2)


def change_optionmenu2(*args):
    if primDD.get() == "Raise Request":
        new_options = options1
    elif primDD.get() == "Raise Complaint":
        new_options = options2
    else:
        new_options = ["Not coded in"]
    secDD.set('')
    secOpt['menu'].delete(0, 'end')
    for choice in new_options:
        secOpt['menu'].add_command(label=choice, command=tkinter._setit(secDD, choice))
    secDD.set(new_options[0])


def onClick():
    tkinter.messagebox.showinfo("Info", "Your request/complaint has been raised successfully.")


def userregistration():
    global root3
    root3 = Toplevel()
    root3.title("Registration Portal")
    root3.geometry("300x300")
    global username
    global password
    Label(root3, text="Sign up", bg="grey", fg="black", font="bold", width=300).pack()
    username = StringVar()
    password = StringVar()
    Label(root3, text="").pack()
    Label(root3, text="Username", font="bold").pack()
    Entry(root3, textvariable=username).pack()
    Label(root3, text="").pack()
    Label(root3, text="Password").pack()
    Entry(root3, textvariable=password, show="*").pack()
    Label(root3, text="").pack()
    Button(root3, text="Next", command=add_newuser).pack()
    Label(root3, text="Already user ?").pack()
    Button(root3, text="Sign in", font="bold", command=lambda: [root3.destroy(), login()]).pack()


def add_newuser():
    username_info = username.get()
    password_info = password.get()
    if username_info == "":
        error_destroy()
    elif password_info == "":
        error_destroy()
    else:
        sql = "insert into userlogin (username,password)values(%s,%s)"
        t = (username_info, password_info)
        cur.execute(sql, t)
        db.commit()
        Label(root3, text="").pack()
        userdet()


def create_bank_interface():
    global vp_image, tran_image, cal_image, loan_image, lock_image, bc_image, lp_image, mc_image, cs_image, fb_image
    root2 = Toplevel()
    root2.geometry("1700x1200")
    root2.title("DIGITAL BANKING EXPERIENCE")

    heading_label = Label(root2, text="DIGITAL BANKING EXPERIENCE", font=("Arial", 24, "bold"), anchor="center")
    heading_label.grid(row=0, columnspan=5, pady=20)

    vp = Image.open("Images/profile.png")
    vp = vp.resize((200, 200), Image.LANCZOS)
    vp_image = ImageTk.PhotoImage(vp)
    l1 = Label(root2, image=vp_image)
    l1.grid(row=1, column=0, padx=20, pady=20)
    submit1 = Button(root2, text="View Profile", command=profilePage)
    submit1.grid(row=2, column=0, padx=20)

    tran = Image.open("Images/Transaction.png")
    tran = tran.resize((200, 200), Image.LANCZOS)
    tran_image = ImageTk.PhotoImage(tran)
    l2 = Label(root2, image=tran_image)
    l2.grid(row=1, column=1, padx=20, pady=20)

    submit2 = Button(root2, text="Transaction", command=transactions)
    submit2.grid(row=2, column=1, padx=20)

    cal = Image.open("Images/loan_calculator.png")
    cal = cal.resize((200, 200), Image.LANCZOS)
    cal_image = ImageTk.PhotoImage(cal)
    l3 = Label(root2, image=cal_image)
    l3.grid(row=1, column=2, padx=20, pady=20)

    submit3 = Button(root2, text="Loan Calculator", command=loancal)
    submit3.grid(row=2, column=2, padx=20)

    loan = Image.open("Images/Loan_application.jpeg")
    loan = loan.resize((200, 200), Image.LANCZOS)
    loan_image = ImageTk.PhotoImage(loan)
    l4 = Label(root2, image=loan_image)
    l4.grid(row=1, column=3, padx=20, pady=20)

    submit4 = Button(root2, text="Loan Application", command=loanwindow)
    submit4.grid(row=2, column=3, padx=20)

    lock = Image.open("Images/locker.jpeg")
    lock = lock.resize((200, 200), Image.LANCZOS)
    lock_image = ImageTk.PhotoImage(lock)
    l5 = Label(root2, image=lock_image)
    l5.grid(row=3, column=0, padx=20, pady=20)

    submit5 = Button(root2, text="Locker Details", command=lockwid)
    submit5.grid(row=4, column=0, padx=20)

    bc = Image.open("Images/block_atm.jpg")
    bc = bc.resize((200, 200), Image.LANCZOS)
    bc_image = ImageTk.PhotoImage(bc)
    l6 = Label(root2, image=bc_image)
    l6.grid(row=3, column=1, padx=20, pady=20)

    submit6 = Button(root2, text="Block ATM", command=atmblock1)
    submit6.grid(row=4, column=1, padx=20)

    lp = Image.open("Images/request.jpg")
    lp = lp.resize((200, 200), Image.LANCZOS)
    lp_image = ImageTk.PhotoImage(lp)
    l7 = Label(root2, image=lp_image)
    l7.grid(row=3, column=2, padx=20, pady=20)

    submit7 = Button(root2, text="Raise Request/Complaint", command=uinputs)
    submit7.grid(row=4, column=2, padx=20)

    fb = Image.open("Images/feedback.jpg")
    fb = fb.resize((200, 200), Image.LANCZOS)
    fb_image = ImageTk.PhotoImage(fb)
    l10 = Label(root2, image=fb_image)
    l10.grid(row=3, column=3, padx=20, pady=20)

    submit10 = Button(root2, text="Feedback", command=feedback_form)
    submit10.grid(row=4, column=3, padx=20)

    lg = Image.open("Images/logout.png")
    lg = lg.resize((200, 200), Image.LANCZOS)
    lg_image = ImageTk.PhotoImage(lg)
    l11 = Label(root2, image=lg_image)
    l11.grid(row=1, column=4, rowspan=3, padx=20, pady=20)

    d = Button(root2, text="Logout", command=root2.destroy)
    d.grid(row=3, column=4, rowspan=2, padx=20, pady=20)


def error_destroy():
    root.destroy()


def failed():
    tkinter.messagebox.showerror("Invalid", "Invalid Details!!!")


def login_verify():
    global user_verify
    user_verify = username_verify.get()
    pas_verify = password_verify.get()
    print("The Username entered is:", user_verify)
    print("The Password entered is:", pas_verify)
    sql = "SELECT * FROM userlogin WHERE username = %s AND password = %s"
    cur.execute(sql, [user_verify, pas_verify])
    results = cur.fetchall()
    if results:
        create_bank_interface()
    else:
        failed()


def login():
    global root
    global username_verify
    global password_verify
    root = Tk()
    root.title("Login Portal")
    root.geometry("300x300")

    Label(root, text="Log-in account", bg="grey", fg="black", font="bold", width=300).pack()

    username_verify = StringVar()
    password_verify = StringVar()

    Label(root, text="Username ", font="bold").place(x=50, y=30)
    Entry(root, width=35, textvariable=username_verify).place(x=140, y=30, width=100)

    Label(root, text="Password ", font="bold").place(x=50, y=60)
    Entry(root, width=35, textvariable=password_verify).place(x=140, y=60, width=100)

    Button(root, text="Login", command=login_verify).place(x=110, y=100, width=70)
    Button(root, text="Cancel", command=root.destroy).place(x=110, y=130, width=70)
    Button(root, text="New user ?", command=userregistration).place(x=110, y=160, width=70)


def retrieve_columns():
    state = state_label.get()
    district = district_label.get()
    pincode = pincode_label.get()

    try:
        cur.execute(
            "SELECT branch_code, branch_name, branch_address FROM branch_lock WHERE state = %s AND district = %s AND pincode = %s",
            (state, district, pincode))

        rows = cur.fetchall()

        result_label.config(text="")

        if rows:
            for row in rows:
                result_label.config(text=result_label.cget(
                    "text") + f"\nBranch Code: {row[0]}, Branch Name: {row[1]}, Branch Address: {row[2]}")
        else:
            result_label.config(text="No matching records found.")

    except mysql.connector.Error as error:
        print("Error retrieving data from MySQL table:", error)

    finally:
        cur.close()
        db.close()


def lockwid():
    window = Toplevel()
    window.title("View Locker")
    window.geometry("1200x800")
    Label(window, text="View Locker Details", bg="grey", fg="black", font="bold", width=300).pack()

    global state_label
    global district_label
    global pincode_label
    global result_label

    sta = Label(window, text="State ", font="bold")
    sta.place(x=525, y=160)
    state_label = Entry(window, width=35)
    state_label.place(x=615, y=165, width=100)

    dis = Label(window, text="District ", font="bold")
    dis.place(x=510, y=220)
    district_label = Entry(window, width=35)
    district_label.place(x=615, y=225, width=100)

    pin = Label(window, text="Pincode ", font="bold")
    pin.place(x=505, y=280)
    pincode_label = Entry(window, width=35)
    pincode_label.place(x=615, y=285, width=100)

    retrieve_button = Button(window, text="Search", command=retrieve_columns)
    retrieve_button.place(x=520, y=340, width=70)
    d = Button(window, text="Back", command=window.destroy)
    d.place(x=610, y=340, width=70)

    result_label = Label(window)
    result_label.place(x=250, y=380)


login()
