# --------------------------------- Libraries --------------------------------#

import re
import os
import sys
import customtkinter as ctk  # pip install customtkinter
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
import database_connector as DB
import ML as ML
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------- TKinter Settings -----------------------------#

# General settings.
script_dir = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()

root.title("BookStore")
root.geometry('1200x700')


def on_close():
    print("Closing application...")
    root.destroy()
    sys.exit()


root.protocol("WM_DELETE_WINDOW", on_close)

# ----------------------------------------------------------------------------#

user_id_label = ctk.CTkLabel(root, text="", font=("Helvetica", 16))
user_id_label.pack()

# ----------------------------------------------------------------------------#

user_id_label = ctk.CTkLabel(root, text="", font=("Helvetica", 16))
user_id_label.place(x=860, y=30)  # Fixed position for user ID label

# ----------------------------------------------------------------------------#

# Top left logo settings.
logo_path = "ANTEIKU.png"
logo = ctk.CTkImage(light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path), size=(160, 160))
logo_label = ctk.CTkLabel(root, text="", image=logo).place(x=0, y=0)

# ----------------------------------------------------------------------------#

user_id = None
admin_id = None

cart = {}

# Search settings.
def search_books(search_query=None):
    global root

    if search_query is None:
        search_query = search_input.get()

    # Found is a list that contains all the books.
    found = DB.search_books(search_query)

    # Checking if any books were found.
    if found:

        # Creating a new window to display search results.
        # Using Toplevel instead of creating a new window to be able
        # to use images. (customtkinter feature)
        search_window = ctk.CTkToplevel(root)
        search_window.title("Search Results")
        search_window.geometry('800x650')

        # Label to display search query
        search_results_label = ctk.CTkLabel(
            search_window, text=f"Search Results for: {search_query}",
            font=("Helvetica", 16))
        search_results_label.pack(pady=20)

        image_refs = []  # List to store image paths.

        # Frame to contain search results
        results_frame = ctk.CTkFrame(search_window)
        results_frame.pack(padx=20, pady=10)

        def add_to_cart(isbn, quantity_entry):
            global cart
            book_info = next((book for book in found if book[0] == isbn), None)
            if book_info:
                quantity = int(quantity_entry.get())  # Get the quantity from the entry widget
                if admin_logged_in:
                    if isbn in cart:
                        cart[isbn]['quantity'] += quantity
                    else:
                        cart[isbn] = {'info': book_info, 'quantity': quantity}
                        result = DB.add_book_to_cart(isbn)
                    return

                if book_info[6] >= quantity:
                    if isbn in cart:
                        cart[isbn]['quantity'] += quantity
                    else:
                        cart[isbn] = {'info': book_info, 'quantity': quantity}
                        result = DB.add_book_to_cart(isbn)
                else:
                    messagebox.showerror("Out of Stock", "Not enough copies of the book in stock.")

        for book_info in found:
            # Frame for each book entry
            book_frame = ctk.CTkFrame(results_frame)
            book_frame.pack(pady=10, anchor="w")

            # Label to display book information
            book_label = ctk.CTkLabel(
                book_frame, text=f"ISBN: {book_info[0]}\n"
                                 f"Title: {book_info[1]}\n"
                                 f"Author: {book_info[2]}\n"
                                 f"Publisher: {book_info[3]}\n"
                                 f"Genre: {book_info[4]}\n"
                                 f"Price: {book_info[5]}\n",
                font=("Helvetica", 12), justify="left")

            cover_path = book_info[8]

            cover_photo = ctk.CTkImage(light_image=Image.open(cover_path),
                                       dark_image=Image.open(cover_path),
                                       size = (90, 110))

            cover_label = ctk.CTkLabel(book_frame, text="", image=cover_photo)
            cover_label.pack(side="right", padx=20)

            book_label.pack(pady=5, anchor="w")

            # Entry widget for displaying quantity
            quantity_entry = ctk.CTkEntry(book_frame, placeholder_text="1", justify="center", width=5)
            quantity_entry.insert(0, "1")  # Default quantity is 1
            quantity_entry.pack(side="left", padx=10)

            # Buttons for adjusting quantity
            increment_button = ctk.CTkButton(
                book_frame, text="+", command=lambda entry=quantity_entry: increment_quantity(entry))
            increment_button.pack(side="left")

            decrement_button = ctk.CTkButton(
                book_frame, text="-", command=lambda entry=quantity_entry: decrement_quantity(entry))
            decrement_button.pack(side="left")

            # Creating an Add to Cart button for each book.
            add_to_cart_button = ctk.CTkButton(
                book_frame, text="Add To Cart",
                command=lambda isbn=book_info[0], entry=quantity_entry: add_to_cart(isbn, entry))
            add_to_cart_button.pack(pady=5, anchor="w")

        search_window.mainloop()

    # Book not found message.
    else:
        messagebox.showinfo(
            "Search Results", "No items found matching your search.")


def increment_quantity(entry):
    current_value = int(entry.get())
    entry.delete(0, "end")
    entry.insert(0, str(current_value + 1))


def decrement_quantity(entry):
    current_value = int(entry.get())
    if current_value > 1:  # Ensure the quantity doesn't go below 1
        entry.delete(0, "end")
        entry.insert(0, str(current_value - 1))


search_input = ctk.CTkEntry(root, placeholder_text='Search', justify='center')
search_input.pack(pady=9)

search_icon_path = "search_icon.png"
search_icon = ctk.CTkImage(light_image=Image.open(search_icon_path),
                           dark_image=Image.open(search_icon_path),
                           size=(27, 27))

search_label = ctk.CTkLabel(root, text="", image=search_icon, cursor="hand2")
search_label.place(x=480, y=36)

search_label.bind("<Button-1>", lambda e: search_books())  # Clicking on the button to get input.
search_input.bind("<Return>", lambda e: search_books())  # Pressing enter to get input.


# ----------------------------------------------------------------------------#

def get_latest_books():
    return DB.get_latest_books()


def open_book_details(book):
    search_books(book[1])


def display_latest_books():
    latest_books = get_latest_books()

    if latest_books:
        latest_books_frame = ctk.CTkFrame(root)
        latest_books_frame.pack(pady=5)

        for book in latest_books:
            cover_path = book[8]
            cover_image = Image.open(cover_path)
            cover_image = cover_image.resize((90, 110), Image.LANCZOS)

            cover_photo = ImageTk.PhotoImage(cover_image)
            cover_ctk_image = ctk.CTkImage(light_image=cover_image,
                                           dark_image=cover_image,
                                           size=(100, 150))

            cover_label = ctk.CTkLabel(latest_books_frame, text="", image=cover_ctk_image, cursor="hand2")
            cover_label.pack(side="left", padx=10)
            cover_label.bind("<Button-1>", lambda e, book=book: open_book_details(book))
            
def display_popular_books():
    popular_books = ML.top3()
    
    if popular_books:
        popular_books_frame = ctk.CTkFrame(root)
        popular_books_frame.pack(pady=5)

        for book in popular_books:
            book = DB.get_book_details(book)
            cover_path = book[8]
            cover_image = Image.open(cover_path)
            cover_image = cover_image.resize((90, 110), Image.LANCZOS)

            cover_photo = ImageTk.PhotoImage(cover_image)
            cover_ctk_image = ctk.CTkImage(light_image=cover_image,
                                           dark_image=cover_image,
                                           size=(100, 150))

            cover_label = ctk.CTkLabel(popular_books_frame, text="", image=cover_ctk_image, cursor="hand2")
            cover_label.pack(side="left", padx=10)
            cover_label.bind("<Button-1>", lambda e, book=book: open_book_details(book))


# Front label settings.
latest_frame = ctk.CTkFrame(root)
latest_frame.pack(padx=100, pady=10)
welcome = ctk.CTkLabel(latest_frame, text="Our latest releases",
                       font=("Helvetica", 36, "bold")).pack(padx=200, pady=10)

display_latest_books()

# Front label settings.
latest_frame = ctk.CTkFrame(root)
latest_frame.pack(padx=100, pady=10)
welcome = ctk.CTkLabel(latest_frame, text="Most popular picks",
                       font=("Helvetica", 36, "bold")).pack(padx=210, pady=10)

display_popular_books()

# ----------------------------------------------------------------------------#


# Cart button settings.

user_logged_in = False
admin_logged_in = False


def open_cart_window():
    global root

    def increment_cart_quantity(isbn, entry):
        global cart
        current_value = int(entry.get())
        new_value = current_value + 1
        entry.delete(0, "end")
        entry.insert(0, str(new_value))
        cart[isbn]['quantity'] = new_value

    def decrement_cart_quantity(isbn, entry):
        global cart
        current_value = int(entry.get())
        if current_value > 1:
            new_value = current_value - 1
            entry.delete(0, "end")
            entry.insert(0, str(new_value))
            cart[isbn]['quantity'] = new_value

    def remove_from_cart(isbn):
        global cart
        if isbn in cart:
            del cart[isbn]
            cart_window.destroy()  # Close the current cart window
            open_cart_window()  # Open a new cart window

    cart_window = ctk.CTkToplevel(root)
    cart_window.title("Cart")
    cart_window.geometry('600x600')

    items_label = ctk.CTkLabel(cart_window, text="Total Items",
                               font=("Helvetica", 20)).pack(pady=10)

    # Frame to contain cart items
    cart_frame = ctk.CTkFrame(cart_window)
    cart_frame.pack(padx=20, pady=10)

    for isbn, book_data in cart.items():
        book_info = book_data['info']
        quantity = book_data['quantity']

        book_frame = ctk.CTkFrame(cart_frame)
        book_frame.pack(pady=10, anchor="w")

        book_label = ctk.CTkLabel(
            book_frame, text=f"Title: {book_info[1]}\n"
                             f"Price: {book_info[5]}\n",
            font=("Helvetica", 12), justify="left")

        cover_path = book_info[8]

        cover_photo = ctk.CTkImage(light_image=Image.open(cover_path),
                                   dark_image=Image.open(cover_path),
                                   size=(90, 110))

        cover_label = ctk.CTkLabel(book_frame, text="", image=cover_photo)
        cover_label.pack(side="right", padx=20)

        book_label.pack(pady=5, anchor="w")

        # Entry widget for displaying quantity
        quantity_entry = ctk.CTkEntry(book_frame, justify="center", width=5)
        quantity_entry.insert(0, str(quantity))  # Set the current quantity
        quantity_entry.pack(side="left", padx=10)

        # Buttons for adjusting quantity
        increment_button = ctk.CTkButton(
            book_frame, text="+", command=lambda isbn=isbn, entry=quantity_entry: increment_cart_quantity(isbn, entry))
        increment_button.pack(side="left")

        decrement_button = ctk.CTkButton(
            book_frame, text="-", command=lambda isbn=isbn, entry=quantity_entry: decrement_cart_quantity(isbn, entry))
        decrement_button.pack(side="left")

        # Button to remove the item from cart
        remove_button = ctk.CTkButton(book_frame, text="Remove",
                                      command=lambda isbn=isbn: remove_from_cart(isbn))
        remove_button.pack(side="left", padx=10)

    def order_complete():
        global cart, user_logged_in, admin_logged_in

        if admin_logged_in:

            book_dict = {isbn: book_data['quantity'] for isbn, book_data in cart.items()}
            DB.transaction_buy(book_dict,admin_id)
            messagebox.showinfo(
                "Purchase Complete",
                "Books bought and added to stock successfully!")

        else:
            if not user_logged_in:
                messagebox.showinfo(
                    "Authentication Required",
                    "Please log in or sign up before placing an order!")
                open_profile()
            else:
                # Dictionary with book ISBNs and quantities
                book_dict = {isbn: book_data['quantity'] for isbn, book_data in cart.items()}

                # Send the transaction to the database
                DB.transaction_sell(book_dict, user_id)

                cart.clear()
                cart_window.destroy()
                messagebox.showinfo("Order Successful", "Your order was successful!")


    recommended_label = ctk.CTkLabel(cart_window, text="Recommended for you!",
                                  font=("Helvetica", 16))
    recommended_label.pack(pady=10)

    def display_recommendation():
        recommended_book = ML.recommendations(cart.keys())

        # dont ask me wtf im doing here man i dont know either hel;p
        rr = int(recommended_book)
        if rr < 10:
            strr = str(rr)
            recommended_book = "0"+strr

        if recommended_book:
            recommended_book_frame = ctk.CTkFrame(cart_window)
            recommended_book_frame.pack(pady=5)

            book = DB.get_book_details(recommended_book)

            cover_path = book[8]
            cover_image = Image.open(cover_path)
            cover_image = cover_image.resize((90, 110), Image.LANCZOS)

            cover_photo = ImageTk.PhotoImage(cover_image)
            cover_ctk_image = ctk.CTkImage(light_image=cover_image,
                                           dark_image=cover_image,
                                           size=(100, 150))

            cover_label = ctk.CTkLabel(recommended_book_frame, text="", image=cover_ctk_image, cursor="hand2")
            cover_label.pack(side="left", padx=10)
            cover_label.bind("<Button-1>", lambda e, book=book: open_book_details(book))



    display_recommendation()

    # Proceed to Purchase button
    proceed_button = ctk.CTkButton(cart_window, text="Proceed to Purchase",
                                   command=order_complete)
    proceed_button.pack(pady=20, side="bottom")

    cart_window.mainloop()


cart_label = ctk.CTkLabel(
    root, text="Cart", font=("Helvetica", 22),
    cursor="hand2")
cart_label.place(x=1070, y=30)
cart_label.bind("<Button-1>", lambda e: open_cart_window())

cart_image_path = "cart.png"
cart_image = ctk.CTkImage(light_image=Image.open(cart_image_path),
                          dark_image=Image.open(
                              cart_image_path), size=(40, 40))
cart_image_label = ctk.CTkLabel(root, text="", image=cart_image)
cart_image_label.place(x=1120, y=25)


# ----------------------------------------------------------------------------#

# Contact us settings.
def open_contact_window():
    contact_window = ctk.CTk()
    contact_window.title("Contact Information")
    contact_window.geometry('330x170')

    email_label = ctk.CTkLabel(
        contact_window, text="Email: anteikubookstore@gmail.com",
        font=("Helvetica", 16)).pack(pady=10)

    telephone_label = ctk.CTkLabel(
        contact_window, text="Telephone: +30 12345678",
        font=("Helvetica", 16)).pack(pady=10)

    address_label = ctk.CTkLabel(
        contact_window, text="Address: Athens, Greece",
        font=("Helvetica", 16)).pack(pady=10)
    contact_window.mainloop()


contact_label = ctk.CTkLabel(root, text="Contact us!", font=("Helvetica", 22),
                             cursor="hand2")
contact_label.place(x=30, y=630)
contact_label.bind("<Button-1>", lambda e: open_contact_window())


# ----------------------------------------------------------------------------#

# User settings. (Log in - Sign up)
def open_profile():
    # Validation functions.
    # Phone, Street Number -> Digits.
    # Email -> example@something.something format.
    validate_phone = lambda new_value: new_value.isdigit() or new_value == ""
    validate_street_number = lambda new_value: new_value.isdigit() or new_value == ""
    validate_email = lambda email: re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

    def signup_user():

        # Getting all data from the text boxes.
        name = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        country = country_entry.get()
        city = city_entry.get()
        street = street_entry.get()
        street_number = street_number_entry.get()
        postal_code = postal_code_entry.get()

        email = email_entry.get()
        if not validate_email(email):
            messagebox.showerror(
                "Invalid Email", "Please enter a valid email address.")
            return

        phone = phone_entry.get()
        if not phone.isdigit():
            messagebox.showerror(
                "Invalid Phone Number",
                "Phone number should contain only numbers.")
            return

        # Data base call. Signing user up.
        result = DB.signup_user(
            name, username, password, country, city, street, street_number,
            postal_code, phone, email)

        if result == "Username already in use":
            messagebox.showerror(
                "Signup Failed",
                "Username already in use. Please choose another username.")
        elif result == "Email already in use":
            messagebox.showerror(
                "Signup Failed",
                "Email already in use. Please choose another email.")
        else:
            messagebox.showinfo(
                "Sign Up Successful", "Your account has been created!")
            back_to_menu()

        back_to_menu()

    def login_user():

        global user_logged_in, user_id, admin_logged_in
        # these need to be strings, incase someone has only a numerical password
        # receiving an integer number will make the validation check give
        # a false negative
        username = username_entry.get()
        password = password_entry.get()

        # Data base call. Checking if credentials are valid.
        user_id = DB.login_user(username, password)

        if user_id == -1:
            messagebox.showerror(
                "Login Failed",
                "Username not found. Please check your username.")
        elif user_id == -2:
            messagebox.showerror(
                "Login Failed", "Invalid password. Please check your password.")
        else:
            messagebox.showinfo(
                "Login Successful", "You have been logged in!")
            username = DB.return_user(user_id)  # Get the username from the user ID

            user_id_label.configure(text=f"{username}", font=("Helvetica", 22),
                                    cursor="hand2")  # Updating label (it has been created already).

            user_window.destroy()
            user_logged_in = True  # User is now logged in
            admin_logged_in = False

    def login_admin():
        global admin_logged_in, admin_id, user_logged_in

        username = username_entry.get()
        password = password_entry.get()

        # Data base call. Checking if credentials are valid.
        admin_id = DB.login_admin(username, password)

        if admin_id == -1:
            messagebox.showerror(
                "Login Failed",
                "Username not found. Please check your username.")
        elif admin_id == -2:
            messagebox.showerror(
                "Login Failed",
                "Invalid password. Please check your password.")
        else:
            messagebox.showinfo(
                "Login Successful",
                "You have been logged in!")
            username = DB.return_admin(admin_id)  # Get the username from the admin ID
            user_id_label.configure(text=f"{username}", font=("Helvetica", 22))
            user_id_label.place(x=860, y=30)
            show_statistics_button = ctk.CTkButton(root, text="Show Statistics", cursor="hand2", command=show_statistics)
            show_statistics_button.place(x=1040, y=630)
            user_window.destroy()
            admin_logged_in = True
            user_logged_in = False


    def show_statistics():
        
        def clear_statistics_window():
            # Destroy all widgets in the statistics window
            for widget in statistics_window.winfo_children():
                widget.destroy()
                
        def back_to_statistics_menu():
            clear_statistics_window()
            show_statistics_buttons()
            
        def show_sale_stats():
            clear_statistics_window()

            income_data = DB.income_last_month()
            days = [entry[0].strftime('%d') for entry in income_data]
            sales = [entry[1] for entry in income_data]

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
            ax.plot(days, sales, marker='o', color='white')
            ax.set_title("LAST MONTH'S SALES", color='white')
            ax.set_xlabel('DAY', color='white')
            ax.set_ylabel('TOTAL SALES', color='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.grid(True, color='gray')

            canvas = FigureCanvasTkAgg(fig, master=statistics_window)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, side="top", fill="both", expand=True)

            back_button = ctk.CTkButton(statistics_window, text="Back", fg_color="Red", command=back_to_statistics_menu)
            back_button.pack(pady=20, side="bottom")
            
        def show_stats_per_genre():
            global plot_init
            plot_init = True

            clear_statistics_window()

            # Showing a matplotlib chart per genre...
            def show_genre_graph(genre):
                global plot_init

                # Deleting the existing plot to make a new one!
                if plot_init == False:
                    ax.clear()

                genre_data = DB.genre_statistics(genre)
                days = [entry[0].strftime('%d') for entry in genre_data]
                sales = [entry[1] for entry in genre_data]

                ax.plot(days, sales, marker='o', color='white')
                ax.set_title(f'SALES FOR {genre}', color='white')
                ax.set_xlabel('DAY', color='white')
                ax.set_ylabel('TOTAL SALES', color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.grid(True, color='gray')

                canvas.draw()

                plot_init = False # Ensuring that there has been at least one plot printed.

            def on_genre_selected():
                genre = genre_combo.get()
                if genre:
                    show_genre_graph(genre)

            # Combobox.
            combo_label = ctk.CTkLabel(statistics_window, text="Pick a genre.", font=("Helvetica", 20))
            combo_label.pack(pady=30)

            genres = ["Literature", "Manga", "Poems"]
            genre_combo = ctk.CTkComboBox(statistics_window, values=genres, height=34, width=240)
            genre_combo.pack(pady=10)

            genre_button = ctk.CTkButton(statistics_window, text="Select genre", command=on_genre_selected)
            genre_button.pack(pady=20)

            # Initialising the matplotlib figure here.
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')

            canvas = FigureCanvasTkAgg(fig, master=statistics_window)
            canvas.get_tk_widget().pack(pady=10, side="top", fill="both", expand=True)

            # Returning to genre selection.
            def back_to_statistics_menu():
                clear_statistics_window()
                show_statistics_buttons()

            # Back button.
            back_button = ctk.CTkButton(statistics_window, text="Back", fg_color="Red", command=back_to_statistics_menu)
            back_button.pack(pady=20, side="bottom")
            
        def show_commonly_bought():
            clear_statistics_window()

            # thank u panagh
            top_books = ML.top20()
            bottom_books = ML.bottom20()

            main_frame = ctk.CTkFrame(statistics_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Top 20 frame.
            top_frame = ctk.CTkFrame(main_frame)
            top_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

            top_label = ctk.CTkLabel(top_frame, text="Top 20 Combinations", font=("Helvetica", 16))
            top_label.pack(pady=10)

            top_left_frame = ctk.CTkFrame(top_frame, width=490, height=350)
            top_left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

            top_right_frame = ctk.CTkFrame(top_frame, width=490, height=350)
            top_right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

            # Left.
            for idx, book in enumerate(top_books[:10], start=1):
                isbn_list = [isbn for isbn in book]
                isbn_label = ctk.CTkLabel(top_left_frame, text=f"{idx}. {', '.join(isbn_list)}", font=("Helvetica", 12))
                isbn_label.pack(anchor="w", padx=10, pady=5)

            # Right.
            for idx, book in enumerate(top_books[10:], start=11):
                isbn_list = [isbn for isbn in book]
                isbn_label = ctk.CTkLabel(top_right_frame, text=f"{idx}. {', '.join(isbn_list)}", font=("Helvetica", 12))
                isbn_label.pack(anchor="w", padx=10, pady=5)

            # Bottom 20 frame.
            bottom_frame = ctk.CTkFrame(main_frame)
            bottom_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

            bottom_label = ctk.CTkLabel(bottom_frame, text="Bottom 20 Combinations", font=("Helvetica", 16))
            bottom_label.pack(pady=10)

            bottom_left_frame = ctk.CTkFrame(bottom_frame, width=490, height=350)
            bottom_left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

            bottom_right_frame = ctk.CTkFrame(bottom_frame, width=490, height=350)
            bottom_right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

            # Left.
            for idx, book in enumerate(bottom_books[:10], start=1):
                isbn_list = [isbn for isbn in book]
                isbn_label = ctk.CTkLabel(bottom_left_frame, text=f"{idx}. {', '.join(isbn_list)}", font=("Helvetica", 12))
                isbn_label.pack(anchor="w", padx=10, pady=5)

            # Right.
            for idx, book in enumerate(bottom_books[10:], start=11):
                isbn_list = [isbn for isbn in book]
                isbn_label = ctk.CTkLabel(bottom_right_frame, text=f"{idx}. {', '.join(isbn_list)}", font=("Helvetica", 12))
                isbn_label.pack(anchor="w", padx=10, pady=5)

            back_button = ctk.CTkButton(statistics_window, text="Back", fg_color="Red", command=back_to_statistics_menu)
            back_button.pack(pady=20, side="bottom")

        def show_statistics_buttons():
            
            select_label = ctk.CTkLabel(
            statistics_window, text="Please select an option.",
            font=("Helvetica", 16))
            select_label.pack(pady=30)
            
            sale_stats_button = ctk.CTkButton(statistics_window, text="Sale stats",
                                            command=lambda: show_sale_stats())
            sale_stats_button.pack(pady=10)

            stats_per_genre_button = ctk.CTkButton(statistics_window, text="Stats per genre",
                                                command=lambda: show_stats_per_genre())
            stats_per_genre_button.pack(pady=10)

            commonly_bought_button = ctk.CTkButton(statistics_window, text="Commonly bought",
                                                command=lambda: show_commonly_bought())
            commonly_bought_button.pack(pady=10)
            
        statistics_window = ctk.CTk()
        statistics_window.title("Statistics")
        statistics_window.geometry('1000x700')
            
        show_statistics_buttons()

        statistics_window.mainloop()
        

    def back_to_menu():

        for widget in user_window.winfo_children():
            widget.destroy()
        build_main_menu()

    def login():

        global username_entry
        global password_entry

        # Clearing previous data.
        for widget in user_window.winfo_children():
            widget.destroy()

        username_label = ctk.CTkLabel(user_window, text="Username",
                                      font=("Helvetica", 16))
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(user_window)
        username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(user_window, text="Password",
                                      font=("Helvetica", 16))
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(user_window, show="*")  # Hiding the password.
        password_entry.pack(pady=5)

        login_button = ctk.CTkButton(user_window, text="Login",
                                     command=login_user)
        login_button.pack(pady=10)

        back_button = ctk.CTkButton(
            user_window, text="Back", fg_color="Red", command=back_to_menu)
        back_button.pack(pady=5)

    def admin():

        global username_entry
        global password_entry

        # Clearing previous data.
        for widget in user_window.winfo_children():
            widget.destroy()

        username_label = ctk.CTkLabel(user_window, text="Username",
                                      font=("Helvetica", 16))
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(user_window)
        username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(user_window, text="Password",
                                      font=("Helvetica", 16))
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(user_window, show="*")  # Hiding the password.
        password_entry.pack(pady=5)

        login_button = ctk.CTkButton(user_window, text="Login",
                                     command=login_admin)
        login_button.pack(pady=10)

        back_button = ctk.CTkButton(
            user_window, text="Back", fg_color="Red", command=back_to_menu)
        back_button.pack(pady=5)

    def signup():

        # Creating global variables for each needed field.
        global name_entry, username_entry, password_entry
        global country_entry, city_entry
        global street_entry, street_number_entry, postal_code_entry
        global phone_entry, email_entry

        # Clearing previous data.
        for widget in user_window.winfo_children():
            widget.destroy()

        # Checking for valid phone number and street number values.
        validation_phone = user_window.register(validate_phone)
        validation_street_number = user_window.register(validate_street_number)

        fields = [
            ("Name", "name_entry"),
            ("Username", "username_entry"),
            ("Password", "password_entry"),
            ("Country", "country_entry"),
            ("City", "city_entry"),
            ("Street", "street_entry"),
            ("Street Number", "street_number_entry"),
            ("Postal Code", "postal_code_entry"),
            ("Phone", "phone_entry"),
            ("Email", "email_entry")
        ]

        # Working with frames to make the fields be left and right.
        left_frame = ctk.CTkFrame(user_window)
        left_frame.pack(side=ctk.LEFT, padx=20, pady=20)

        right_frame = ctk.CTkFrame(user_window)
        right_frame.pack(side=ctk.RIGHT, padx=20, pady=20)

        # Using a for loop instead of manually adding every single field necessary.
        for i, (label_text, entry_var) in enumerate(fields):
            parent_frame = left_frame if i % 2 == 0 else right_frame

            label = ctk.CTkLabel(
                parent_frame, text=label_text, font=("Helvetica", 16))
            label.pack(pady=5)

            if label_text in ["Phone", "Street Number"]:
                entry = ctk.CTkEntry(
                    parent_frame, validate="key",
                    validatecommand=(
                        validation_phone if label_text == "Phone" else validation_street_number, '%P'))
            elif label_text == "Password":
                entry = ctk.CTkEntry(parent_frame, show="*")
            else:
                entry = ctk.CTkEntry(parent_frame)

            entry.pack(pady=5)
            globals()[entry_var] = entry

        signup_button = ctk.CTkButton(
            user_window, text="Sign Up", command=signup_user)
        signup_button.pack(pady=10)

        back_button = ctk.CTkButton(
            user_window, text="Back", fg_color="Red", command=back_to_menu)
        back_button.pack(pady=10)

    def build_main_menu():
        select_label = ctk.CTkLabel(
            user_window, text="Please select an option.",
            font=("Helvetica", 16))
        select_label.pack(pady=30)

        login_button = ctk.CTkButton(
            user_window, text="Log In", command=login)
        login_button.pack(pady=10)

        signup_button = ctk.CTkButton(
            user_window, text="Sign Up", command=signup)
        signup_button.pack(pady=10)

        admin_button = ctk.CTkButton(
            user_window, text="Admin", fg_color="Blue", command=admin)
        admin_button.pack(pady=10)

    user_window = ctk.CTk()
    user_window.title("Profile")
    user_window.geometry('450x450')

    build_main_menu()
    user_window.mainloop()


# ----------------------------------------------------------------------------#

# Past transactions function for when the username on the top right is clicked.
def showTransactions():
    global user_id  # Access the user_id variable
    global root
    if user_id:  # If no user has been logged in they won't see this :).

        transactions = DB.customer_transactions(user_id)  # Accessing from DB.

        past_transactions_window = ctk.CTkToplevel(root)
        past_transactions_window.title("Past Transactions")
        past_transactions_window.geometry('550x500')

        transactions_label = ctk.CTkLabel(
            past_transactions_window, text="Past Transactions:", font=("Helvetica", 16))
        transactions_label.pack(pady=10)

        transactions_frame = ctk.CTkFrame(past_transactions_window)
        transactions_frame.pack(fill="y", expand=True, padx=10, pady=10)

        # Creating the canvas to be able to scroll through the past transactions.
        canvas = ctk.CTkCanvas(transactions_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Adding a scrollbar in case of a lot of purchases.
        scrollbar = ctk.CTkScrollbar(transactions_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Linking the scrollbar to the canvas.
        inner_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for i, transaction in enumerate(transactions, start=1):

            # Book details for each book purchased printed based on the isbn.
            for book_isbn in transaction:

                # Frame for each book entry.
                book_frame = ctk.CTkFrame(inner_frame)
                book_frame.pack(pady=10, anchor="w")
                book_details = DB.get_book_details(book_isbn)

                if book_details:

                    book_info_label = ctk.CTkLabel(
                        book_frame,
                        text=f"ISBN: {book_details[0]}\n"
                             f"Title: {book_details[1]}\n"
                             f"Author: {book_details[2]}\n"
                             f"Publisher: {book_details[3]}\n"
                             f"Genre: {book_details[4]}\n"
                             f"Price: {book_details[5]}\n",
                        font=("Helvetica", 12), justify="left")

                    # Cover image
                    cover_path = book_details[8]
                    cover_photo = ctk.CTkImage(light_image=Image.open(cover_path),
                                               dark_image=Image.open(cover_path),
                                               size=(90, 110))
                    cover_label = ctk.CTkLabel(book_frame, text="", image=cover_photo)
                    cover_label.pack(side="right", padx=20, anchor="e")

                    book_info_label.pack(pady=5, anchor="w")
        past_transactions_window.mainloop()


user_id_label.bind("<Button-1>", lambda e: showTransactions())

# ----------------------------------------------------------------------------#


profile_label = ctk.CTkLabel(
    root, text="User", font=("Helvetica", 22), cursor="hand2")
profile_label.place(x=960, y=30)
profile_label.bind("<Button-1>", lambda e: open_profile())

profile_image_path = "profile.png"
profile_image = ctk.CTkImage(
    light_image=Image.open(profile_image_path),
    dark_image=Image.open(profile_image_path), size=(27, 27))
profile_image_label = ctk.CTkLabel(root, text="", image=profile_image)
profile_image_label.place(x=1020, y=30)

root.mainloop()


# ----------------------------------------------------------------------------#


# Main Shopping Interface Function
def open_main_shopping_interface():
    # Create a new window for the main shopping interface
    main_window = ctk.CTk()
    main_window.title("Bookstore")
    main_window.geometry('800x600')

    welcome_label = ctk.CTkLabel(
        main_window, text="Welcome to Anteiku!", font=("Helvetica", 22))
    welcome_label.pack(pady=20)

    main_window.mainloop()


# ----------------------------------------------------------------------------#


root.mainloop()

# ----------------------------------------------------------------------------#