import math
import os
from datetime import datetime

# the text files have to be in the folder the program is run from
GEAR_FILE = "gear.txt"
PICKUP_FILE = "pickup_points.txt"
CUSTOMER_FILE = "customers.txt"
RENTAL_FILE = "rentals.txt"
REPORT_FILE = "reports.txt"

GEAR_TYPES = ["Shade", "Cooler", "Seating", "Audio"]
GEAR_STATUSES = ["Available", "Unavailable"]
PICKUP_STATUSES = ["Active", "Inactive"]
OPEN_STATUSES = ["Active", "Overdue"]
OVERDUE_LIMIT_MINUTES = 4 * 60
MAX_ID = 99999
MAX_UNITS = 9999
MAX_RATE = 1000

# extras 
MANAGER_PIN = "1234"
LATE_FEE = 10.00
STUDENT_DISCOUNT = 0.10
STUDENT_EMAIL = "@crimson.ua.edu"
GAME_DAY_RATE = 1.5

HOME_GAMES = ["09/05/2026", "09/19/2026", "10/31/2026", "11/14/2026", "11/21/2026"]


# record classes
class Gear:
    def __init__(self, gear_id, item, gear_type, hourly_rate, status, pickup_id, total_units, units_available):
        self._gear_id = gear_id
        self._item = item
        self._gear_type = gear_type
        self._hourly_rate = hourly_rate
        self._status = status
        self._pickup_id = pickup_id
        self._total_units = total_units
        self._units_available = units_available

    def get_id(self):
        return self._gear_id

    def set_id(self, gear_id):
        self._gear_id = gear_id

    def get_item(self):
        return self._item

    def set_item(self, item):
        self._item = item

    def get_type(self):
        return self._gear_type

    def set_type(self, gear_type):
        self._gear_type = gear_type

    def get_hourly_rate(self):
        return self._hourly_rate

    def set_hourly_rate(self, hourly_rate):
        self._hourly_rate = hourly_rate

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_pickup_id(self):
        return self._pickup_id

    def set_pickup_id(self, pickup_id):
        self._pickup_id = pickup_id

    def get_total_units(self):
        return self._total_units

    def set_total_units(self, total_units):
        self._total_units = total_units

    def get_units_available(self):
        return self._units_available

    def set_units_available(self, units_available):
        self._units_available = units_available

    def to_line(self):
        return (f"{self._gear_id}#{self._item}#{self._gear_type}#{self._hourly_rate:.2f}#{self._status}"
                f"#{self._pickup_id}#{self._total_units}#{self._units_available}")


class PickupPoint:
    def __init__(self, pickup_id, location, status, capacity, last_restocked):
        self._pickup_id = pickup_id
        self._location = location
        self._status = status
        self._capacity = capacity
        self._last_restocked = last_restocked

    def get_id(self):
        return self._pickup_id

    def set_id(self, pickup_id):
        self._pickup_id = pickup_id

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_capacity(self):
        return self._capacity

    def set_capacity(self, capacity):
        self._capacity = capacity

    def get_last_restocked(self):
        return self._last_restocked

    def set_last_restocked(self, last_restocked):
        self._last_restocked = last_restocked

    def to_line(self):
        return f"{self._pickup_id}#{self._location}#{self._status}#{self._capacity}#{self._last_restocked}"


class Customer:
    def __init__(self, email, first_name, last_name, phone, status):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._phone = phone
        self._status = status

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def get_phone(self):
        return self._phone

    def set_phone(self, phone):
        self._phone = phone

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def to_line(self):
        return f"{self._email}#{self._first_name}#{self._last_name}#{self._phone}#{self._status}"


class Rental:
    def __init__(self, rental_id, email, gear_id, pickup_id, date, start, end, cost, status):
        self._rental_id = rental_id
        self._email = email
        self._gear_id = gear_id
        self._pickup_id = pickup_id
        self._date = date
        self._start = start
        self._end = end
        self._cost = cost
        self._status = status

    def get_id(self):
        return self._rental_id

    def set_id(self, rental_id):
        self._rental_id = rental_id

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_gear_id(self):
        return self._gear_id

    def set_gear_id(self, gear_id):
        self._gear_id = gear_id

    def get_pickup_id(self):
        return self._pickup_id

    def set_pickup_id(self, pickup_id):
        self._pickup_id = pickup_id

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._date = date

    def get_start(self):
        return self._start

    def set_start(self, start):
        self._start = start

    def get_end(self):
        return self._end

    def set_end(self, end):
        self._end = end

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    # every started hour counts as a full hour 08:30 to 11:45 is 195 minutes, 195 / 60 = 3.25, rounded up to 4 hours
    def calculate_cost(self, returned, hourly_rate):
        hours = math.ceil(self.minutes_out(returned) / 60)
        return hours, round(hours * hourly_rate, 2)

    # minutes from the start of the rental until now (or until it came back)
    def minutes_out(self, now):
        started = datetime.strptime(f"{self._date} {self._start}", "%m/%d/%Y %H:%M")
        return int((now - started).total_seconds() // 60)

    def to_line(self):
        cost = "N/A"
        if self._cost is not None:
            cost = f"{self._cost:.2f}"
        return (f"{self._rental_id}#{self._email}#{self._gear_id}#{self._pickup_id}#{self._date}"
                f"#{self._start}#{self._end}#{cost}#{self._status}")


# everything is loaded once here then every change saves right away
def main():
    gear_list = load_gear()
    pickup_points = load_pickup_points()
    customers = load_customers()
    rentals = load_rentals()
    while True:
        update_overdue(rentals)
        print_menu("Tide Tailgate Main Menu", ["Customer Menu", "Manager Menu", "Reports", "Exit"])
        choice = input("Enter a choice (1-4): ").strip()
        if choice == "1":
            customer = sign_in(customers)
            if customer is None:
                pause()
            else:
                customer_menu(customer, gear_list, pickup_points, rentals)
        elif choice == "2":
            if check_pin():
                manager_menu(gear_list, pickup_points, customers, rentals)
        elif choice == "3":
            if check_pin():
                reports_menu(gear_list, pickup_points, rentals)
        elif choice == "4":
            print("Thanks for using Tide Tailgate. Roll Tide!")
            break
        else:
            print("Invalid choice. Enter 1-4.")


# input checks each one keeps asking until the input is good
def int_in_range(prompt, low, high):
    while True:
        try:
            number = int(input(prompt))
            if low <= number <= high:
                return number
            else:
                print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def float_in_range(prompt, low, high):
    while True:
        try:
            number = float(input(prompt))
            if low <= number <= high:
                return number
            else:
                print(f"Please enter a number between {low:.2f} and {high:.2f}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# a # would break the file format
def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            print("This can't be blank.")
        elif "#" in text:
            print("This can't contain a # sign.")
        else:
            return text


def get_option(prompt, options):
    while True:
        answer = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        for option in options:
            if answer == option.lower():
                return option
        print(f"Invalid entry. Choose {', '.join(options)}.")


def get_yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


# strptime throws a ValueError for times like 25:00 or 9:75
def get_time(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%H:%M").strftime("%H:%M")
        except ValueError:
            print("Invalid time. Enter a time in HH:MM format, 00:00 to 23:59.")


# pressing Enter gives back the default date if there is one
def get_date(prompt, default=None):
    while True:
        text = input(prompt).strip()
        if text == "" and default:
            return default
        try:
            return datetime.strptime(text, "%m/%d/%Y").strftime("%m/%d/%Y")
        except ValueError:
            print("Invalid date. Enter a real date in MM/DD/YYYY format.")


def pause():
    input("\nPress Enter to continue...")
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# heading lines are returned so the reports can print them and save them
def heading(title):
    return [f"\n{title}", "=" * 26]


def print_heading(title):
    print_lines(heading(title))


def print_lines(lines):
    for line in lines:
        print(line)


def print_menu(title, options):
    print_heading(title)
    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")


def read_records(file_name):
    try:
        with open(file_name, encoding="utf-8") as file:
            records = []
            for line in file:
                line = line.strip()
                if line != "":
                    records.append(line.split("#"))
            return records
    except FileNotFoundError:
        print(f"Could not find {file_name}. Starting with no records.")
        return []


# each line was split on # and the parts go into a new object lists are sorted by ID so binary_search works on them
def load_gear():
    gear_list = []
    for parts in read_records(GEAR_FILE):
        gear_list.append(Gear(int(parts[0]), parts[1], parts[2], float(parts[3]), parts[4],
                              int(parts[5]), int(parts[6]), int(parts[7])))
    sort_by_id(gear_list)
    return gear_list


def load_pickup_points():
    points = []
    for parts in read_records(PICKUP_FILE):
        points.append(PickupPoint(int(parts[0]), parts[1], parts[2], int(parts[3]), parts[4]))
    sort_by_id(points)
    return points


def load_customers():
    customers = []
    for parts in read_records(CUSTOMER_FILE):
        customers.append(Customer(parts[0], parts[1], parts[2], parts[3], parts[4]))
    return customers


def load_rentals():
    rentals = []
    for parts in read_records(RENTAL_FILE):
        # rentals that are still out have N/A for the cost
        cost = None
        if parts[7] != "N/A":
            cost = float(parts[7])
        rentals.append(Rental(int(parts[0]), parts[1], int(parts[2]), int(parts[3]), parts[4],
                              parts[5], parts[6], cost, parts[8]))
    sort_by_id(rentals)
    return rentals


def save_file(file_name, records):
    with open(file_name, "w", encoding="utf-8") as file:
        for record in records:
            file.write(record.to_line() + "\n")


# bubble sort 
def sort_by_id(records):
    for i in range(len(records) - 1):
        for j in range(len(records) - 1 - i):
            if records[j].get_id() > records[j + 1].get_id():
                temp = records[j]
                records[j] = records[j + 1]
                records[j + 1] = temp


# binary search
def binary_search(records, target_id):
    low = 0
    high = len(records) - 1
    while low <= high:
        middle = (low + high) // 2
        middle_id = records[middle].get_id()
        if middle_id == target_id:
            return records[middle]
        elif middle_id < target_id:
            low = middle + 1
        else:
            high = middle - 1
    return None


# asks for an ID and finds the record with binary search
def choose_record(records, prompt, name):
    record = binary_search(records, int_in_range(prompt, 1, MAX_ID))
    if record is None:
        print(f"{name} not found.")
    return record


# new IDs are one more than the highest ID
def next_id(records):
    highest = 0
    for record in records:
        if record.get_id() > highest:
            highest = record.get_id()
    return highest + 1


# a removed gear ID can still be in rentals.txt, so new gear never reuses one
def next_gear_id(gear_list, rentals):
    new_id = next_id(gear_list)
    for rental in rentals:
        if rental.get_gear_id() >= new_id:
            new_id = rental.get_gear_id() + 1
    return new_id


def find_customer(customers, email):
    for customer in customers:
        if customer.get_email().lower() == email.lower():
            return customer
    return None


# rentals that are Active or Overdue, only one customer's if an email is given
def open_rentals(rentals, email=None):
    still_out = []
    for rental in rentals:
        if rental.get_status() in OPEN_STATUSES:
            if email is None or rental.get_email().lower() == email.lower():
                still_out.append(rental)
    return still_out


# counted from the rentals, because Unavailable gear can have 0 available with none rented
def units_rented(gear, rentals):
    count = 0
    for rental in open_rentals(rentals):
        if rental.get_gear_id() == gear.get_id():
            count += 1
    return count


# any Active rental out longer than 4 hours becomes Overdue
def update_overdue(rentals):
    now = datetime.now()
    changed = False
    for rental in rentals:
        if rental.get_status() == "Active" and rental.minutes_out(now) > OVERDUE_LIMIT_MINUTES:
            rental.set_status("Overdue")
            changed = True
    if changed:
        save_file(RENTAL_FILE, rentals)


def item_name(gear_list, gear_id):
    gear = binary_search(gear_list, gear_id)
    if gear is None:
        return "Removed gear"
    return gear.get_item()


def location_name(pickup_points, pickup_id):
    point = binary_search(pickup_points, pickup_id)
    if point is None:
        return "Unknown"
    return point.get_location()


# :<26 pads the text to 26 characters so the columns line up
def show_gear_table(gear_list, pickup_points):
    print(f"\n{'ID':<5}{'Item':<26}{'Type':<9}{'Rate':>7}  {'Location':<27}{'Status':<13}{'Available':>9}")
    print("-" * 96)
    for gear in gear_list:
        print(f"{gear.get_id():<5}{gear.get_item():<26}{gear.get_type():<9}${gear.get_hourly_rate():>6.2f}  "
              f"{location_name(pickup_points, gear.get_pickup_id()):<27}{gear.get_status():<13}"
              f"{gear.get_units_available():>9}")


# returns the lines instead of printing them so the reports can save them too
def rental_table(rentals, gear_list):
    lines = [f"\n{'ID':<5}{'Email':<24}{'Item':<26}{'Date':<12}{'Start':<7}{'End':<7}{'Cost':>9}  {'Status':<10}",
             "-" * 100]
    for rental in rentals:
        cost = "N/A"
        if rental.get_cost() is not None:
            cost = f"${rental.get_cost():.2f}"
        lines.append(f"{rental.get_id():<5}{rental.get_email():<24}{item_name(gear_list, rental.get_gear_id()):<26}"
                     f"{rental.get_date():<12}{rental.get_start():<7}{rental.get_end():<7}{cost:>9}  {rental.get_status()}")
    return lines


def show_rental_table(rentals, gear_list):
    print_lines(rental_table(rentals, gear_list))


def show_pickup_table(pickup_points):
    print(f"\n{'ID':<5}{'Location':<26}{'Status':<10}{'Capacity':>8}  {'Last Restocked':<14}")
    print("-" * 65)
    for point in pickup_points:
        print(f"{point.get_id():<5}{point.get_location():<26}{point.get_status():<10}"
              f"{point.get_capacity():>8}  {point.get_last_restocked():<14}")


def sign_in(customers):
    print_heading("Customer Sign In")
    customer = find_customer(customers, get_text("Enter your email: "))
    if customer is None:
        print("No customer found with that email.")
        return None
    print(f"Welcome, {customer.get_first_name()} {customer.get_last_name()}!")
    # inactive customers can still look around and see their history
    if customer.get_status() != "Active":
        print("Your account is inactive, so you can't start a rental.")
    return customer


def customer_menu(customer, gear_list, pickup_points, rentals):
    while True:
        print_menu(f"Customer Menu - {customer.get_first_name()}",
                   ["Browse available gear", "Search gear", "Start a rental", "End a rental",
                    "View rental history", "Back to main menu"])
        choice = input("Enter a choice (1-6): ").strip()
        if choice == "1":
            browse_gear(gear_list, pickup_points)
        elif choice == "2":
            search_gear(gear_list, pickup_points)
        elif choice == "3":
            start_rental(customer, gear_list, pickup_points, rentals)
        elif choice == "4":
            end_rental(customer, gear_list, rentals)
        elif choice == "5":
            view_history(customer, rentals, gear_list)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Enter 1-6.")
            continue
        pause()


def browse_gear(gear_list, pickup_points):
    available = []
    for gear in gear_list:
        if gear.get_status() == "Available" and gear.get_units_available() > 0:
            available.append(gear)
    if available:
        show_gear_table(available, pickup_points)
    else:
        print("No gear is available right now.")


def search_gear(gear_list, pickup_points):
    print("Search by: 1. Type  2. Name")
    matches = []
    if int_in_range("Enter a choice (1-2): ", 1, 2) == 1:
        gear_type = get_option("Type", GEAR_TYPES)
        for gear in gear_list:
            if gear.get_type() == gear_type:
                matches.append(gear)
    else:
        text = get_text("Name contains: ").lower()
        for gear in gear_list:
            if text in gear.get_item().lower():
                matches.append(gear)
    if matches:
        show_gear_table(matches, pickup_points)
    else:
        print("No gear found.")


def start_rental(customer, gear_list, pickup_points, rentals):
    if customer.get_status() != "Active":
        print("Only Active customers can rent gear.")
        return
    browse_gear(gear_list, pickup_points)
    gear = choose_record(gear_list, "\nEnter the gear ID to rent: ", "Gear")
    if gear is None:
        return
    if gear.get_status() != "Available":
        print(f"{gear.get_item()} is unavailable.")
        return
    if gear.get_units_available() < 1:
        print(f"No units of {gear.get_item()} are available right now.")
        return
    point = binary_search(pickup_points, gear.get_pickup_id())
    if point is None or point.get_status() != "Active":
        print(f"{gear.get_item()} is at an inactive pickup point, so it can't be rented right now.")
        return
    date = get_date("Rental date (MM/DD/YYYY): ")
    start = get_time("Start time (HH:MM): ")
    rental = Rental(next_id(rentals), customer.get_email(), gear.get_id(), point.get_id(),
                    date, start, "N/A", None, "Active")
    rentals.append(rental)
    gear.set_units_available(gear.get_units_available() - 1)
    save_file(GEAR_FILE, gear_list)
    save_file(RENTAL_FILE, rentals)
    print(f"Rental {rental.get_id()} started: {gear.get_item()} from {point.get_location()} "
          f"on {date} at {start}.")


# used by both the customer and manager menus
def close_rental(rental, gear_list, rentals):
    gear = binary_search(gear_list, rental.get_gear_id())
    if gear is None:
        print("The gear for this rental no longer exists.")
        return
    # asking for the return date lets a rental go past midnight or last more than a day
    while True:
        end_date = get_date(f"Return date (MM/DD/YYYY, Enter for {rental.get_date()}): ", rental.get_date())
        end = get_time("End time (HH:MM): ")
        returned = datetime.strptime(f"{end_date} {end}", "%m/%d/%Y %H:%M")
        if rental.minutes_out(returned) > 0:
            break
        print(f"The return has to be after the start ({rental.get_date()} at {rental.get_start()}).")
    rate = gear.get_hourly_rate()
    extras = []
    # extra: game-day pricing on home-game Saturdays
    if rental.get_date() in HOME_GAMES:
        rate = round(rate * GAME_DAY_RATE, 2)
        extras.append(f"Game day: ${gear.get_hourly_rate():.2f} x {GAME_DAY_RATE} = ${rate:.2f} an hour")
    hours, cost = rental.calculate_cost(returned, rate)
    # extra: student discount for crimson.ua.edu emails
    if rental.get_email().lower().endswith(STUDENT_EMAIL):
        discount = round(cost * STUDENT_DISCOUNT, 2)
        cost = cost - discount
        extras.append(f"Student discount: -${discount:.2f}")
    # extra: late fee when the gear comes back after the 4 hour limit
    if rental.minutes_out(returned) > OVERDUE_LIMIT_MINUTES:
        cost = cost + LATE_FEE
        extras.append(f"Late fee: +${LATE_FEE:.2f}")
    rental.set_end(end)
    rental.set_cost(round(cost, 2))
    rental.set_status("Completed")
    if gear.get_units_available() < gear.get_total_units():
        gear.set_units_available(gear.get_units_available() + 1)
    save_file(GEAR_FILE, gear_list)
    save_file(RENTAL_FILE, rentals)
    end_text = end
    if end_date != rental.get_date():
        end_text = f"{end} on {end_date}"
    print_receipt(gear.get_item(), rental.get_start(), end_text, hours, rate, extras, rental.get_cost())


# extras holds the game day recepits
def print_receipt(item, start, end, hours, rate, extras, cost):
    print_heading("Rental Complete")
    print(f"Gear: {item}")
    print(f"Start: {start}")
    print(f"End: {end}")
    if hours == 1:
        print(f"Billed: 1 hour x ${rate:.2f}")
    else:
        print(f"Billed: {hours} hours x ${rate:.2f}")
    for line in extras:
        print(line)
    print(f"Cost: ${cost:.2f}")


def end_rental(customer, gear_list, rentals):
    mine = open_rentals(rentals, customer.get_email())
    if not mine:
        print("You have no rentals to end.")
        return
    show_rental_table(mine, gear_list)
    rental = binary_search(rentals, int_in_range("\nEnter the rental ID to end: ", 1, MAX_ID))
    if rental not in mine:
        print("That isn't one of your open rentals.")
        return
    close_rental(rental, gear_list, rentals)


def view_history(customer, rentals, gear_list):
    history = []
    for rental in rentals:
        if rental.get_email().lower() == customer.get_email().lower():
            history.append(rental)
    if history:
        show_rental_table(history, gear_list)
    else:
        print("No rentals yet.")


# extra: the manager menu and reports both ask for the manager PIN first
def check_pin():
    for _ in range(3):
        if input("Manager PIN: ").strip() == MANAGER_PIN:
            return True
        print("Wrong PIN.")
    print("Too many wrong tries.")
    pause()
    return False


def manager_menu(gear_list, pickup_points, customers, rentals):
    while True:
        print_menu("Manager Menu",
                   ["Add a gear item", "Remove a gear item", "Edit a gear item", "Add a pickup point",
                    "Edit a pickup point", "Change pickup point status", "Mark a rental completed",
                    "Add a customer", "Edit customer info", "Deactivate a customer", "Back to main menu"])
        choice = input("Enter a choice (1-11): ").strip()
        if choice == "1":
            add_gear(gear_list, pickup_points, rentals)
        elif choice == "2":
            remove_gear(gear_list, pickup_points, rentals)
        elif choice == "3":
            edit_gear(gear_list, pickup_points, rentals)
        elif choice == "4":
            add_pickup_point(pickup_points)
        elif choice == "5":
            edit_pickup_point(pickup_points)
        elif choice == "6":
            change_pickup_status(pickup_points)
        elif choice == "7":
            complete_rental(gear_list, rentals)
        elif choice == "8":
            add_customer(customers)
        elif choice == "9":
            edit_customer(customers)
        elif choice == "10":
            deactivate_customer(customers)
        elif choice == "11":
            break
        else:
            print("Invalid choice. Enter 1-11.")
            continue
        pause()


def get_pickup_id(pickup_points):
    show_pickup_table(pickup_points)
    while True:
        pickup_id = int_in_range("\nPickup ID: ", 1, MAX_ID)
        if binary_search(pickup_points, pickup_id):
            return pickup_id
        print("No pickup point has that ID.")


def add_gear(gear_list, pickup_points, rentals):
    item = get_text("Item name: ")
    gear_type = get_option("Type", GEAR_TYPES)
    rate = float_in_range("Hourly rate: ", 0.01, MAX_RATE)
    status = get_option("Status", GEAR_STATUSES)
    pickup_id = get_pickup_id(pickup_points)
    total = int_in_range("Total units: ", 1, MAX_UNITS)
    gear = Gear(next_gear_id(gear_list, rentals), item, gear_type, rate, status, pickup_id, total, total)
    gear_list.append(gear)
    save_file(GEAR_FILE, gear_list)
    print(f"Added gear {gear.get_id()}: {item}, {total} of {total} units available.")


def remove_gear(gear_list, pickup_points, rentals):
    show_gear_table(gear_list, pickup_points)
    gear = choose_record(gear_list, "\nGear ID to remove: ", "Gear")
    if gear is None:
        return
    rented = units_rented(gear, rentals)
    if rented > 0:
        print(f"Can't remove {gear.get_item()}, it still has {rented} rented out.")
        return
    gear_list.remove(gear)
    save_file(GEAR_FILE, gear_list)
    print(f"Removed {gear.get_item()}.")


def edit_gear(gear_list, pickup_points, rentals):
    show_gear_table(gear_list, pickup_points)
    gear = choose_record(gear_list, "\nGear ID to edit: ", "Gear")
    if gear is None:
        return
    print(f"Editing {gear.get_item()}")
    print("1. Name  2. Type  3. Rate  4. Status  5. Pickup point  6. Total units")
    field = int_in_range("Field to change (1-6): ", 1, 6)
    if field == 1:
        gear.set_item(get_text("New name: "))
    elif field == 2:
        gear.set_type(get_option("New type", GEAR_TYPES))
    elif field == 3:
        gear.set_hourly_rate(float_in_range("New hourly rate: ", 0.01, MAX_RATE))
    elif field == 4:
        gear.set_status(get_option("New status", GEAR_STATUSES))
    elif field == 5:
        gear.set_pickup_id(get_pickup_id(pickup_points))
    else:
        # rented units stay rented, so available is the new total minus those
        rented = units_rented(gear, rentals)
        total = int_in_range("New total units: ", 0, MAX_UNITS)
        if total < rented:
            print(f"Can't set total units below the {rented} rented out.")
            return
        gear.set_total_units(total)
        gear.set_units_available(total - rented)
    save_file(GEAR_FILE, gear_list)
    print("Gear updated.")
    show_gear_table([gear], pickup_points)


def add_pickup_point(pickup_points):
    location = get_text("Location: ")
    status = get_option("Status", PICKUP_STATUSES)
    capacity = int_in_range("Capacity: ", 1, MAX_UNITS)
    restocked = get_date("Last restocked date (MM/DD/YYYY): ")
    point = PickupPoint(next_id(pickup_points), location, status, capacity, restocked)
    pickup_points.append(point)
    save_file(PICKUP_FILE, pickup_points)
    print(f"Added pickup point {point.get_id()}: {location}.")


def edit_pickup_point(pickup_points):
    show_pickup_table(pickup_points)
    point = choose_record(pickup_points, "\nPickup ID to edit: ", "Pickup point")
    if point is None:
        return
    print(f"Editing {point.get_location()}")
    print("1. Location  2. Capacity  3. Last restocked date")
    field = int_in_range("Field to change (1-3): ", 1, 3)
    if field == 1:
        point.set_location(get_text("New location: "))
    elif field == 2:
        point.set_capacity(int_in_range("New capacity: ", 1, MAX_UNITS))
    else:
        point.set_last_restocked(get_date("New last restocked date (MM/DD/YYYY): "))
    save_file(PICKUP_FILE, pickup_points)
    print("Pickup point updated.")


def change_pickup_status(pickup_points):
    show_pickup_table(pickup_points)
    point = choose_record(pickup_points, "\nPickup ID: ", "Pickup point")
    if point is None:
        return
    if point.get_status() == "Active":
        point.set_status("Inactive")
    else:
        point.set_status("Active")
    save_file(PICKUP_FILE, pickup_points)
    print(f"{point.get_location()} is now {point.get_status()}.")


def complete_rental(gear_list, rentals):
    still_out = open_rentals(rentals)
    if not still_out:
        print("There are no open rentals.")
        return
    show_rental_table(still_out, gear_list)
    rental = binary_search(rentals, int_in_range("\nRental ID to complete: ", 1, MAX_ID))
    if rental not in still_out:
        print("That rental isn't open.")
        return
    close_rental(rental, gear_list, rentals)


def add_customer(customers):
    email = get_text("Email: ").lower()
    while "@" not in email or " " in email:
        print("Enter a valid email with an @ and no spaces.")
        email = get_text("Email: ").lower()
    if find_customer(customers, email):
        print("That email is already used by another customer.")
        return
    first_name = get_text("First name: ")
    last_name = get_text("Last name: ")
    phone = get_text("Phone: ")
    customers.append(Customer(email, first_name, last_name, phone, "Active"))
    save_file(CUSTOMER_FILE, customers)
    print(f"Added {first_name} {last_name} as an Active customer.")


# email can't be changed because rentals are linked by email
def edit_customer(customers):
    customer = find_customer(customers, get_text("Customer email: "))
    if customer is None:
        print("Customer not found.")
        return
    print(f"Editing {customer.get_first_name()} {customer.get_last_name()}")
    print("1. First name  2. Last name  3. Phone")
    field = int_in_range("Field to change (1-3): ", 1, 3)
    if field == 1:
        customer.set_first_name(get_text("New first name: "))
    elif field == 2:
        customer.set_last_name(get_text("New last name: "))
    else:
        customer.set_phone(get_text("New phone: "))
    save_file(CUSTOMER_FILE, customers)
    print("Customer updated.")


def deactivate_customer(customers):
    customer = find_customer(customers, get_text("Customer email: "))
    if customer is None:
        print("Customer not found.")
        return
    if customer.get_status() == "Inactive":
        print("That customer is already inactive.")
        return
    customer.set_status("Inactive")
    save_file(CUSTOMER_FILE, customers)
    print(f"{customer.get_first_name()} {customer.get_last_name()} is now Inactive.")


# every report returns a list of lines the menu prints them and can save them
def reports_menu(gear_list, pickup_points, rentals):
    while True:
        print_menu("Reports", ["Daily rentals", "Gear currently out", "Overdue rentals",
                               "Most popular gear", "Revenue", "Back to main menu"])
        choice = input("Enter a choice (1-6): ").strip()
        if choice == "1":
            lines = daily_rentals_report(rentals, gear_list)
        elif choice == "2":
            lines = gear_out_report(rentals, gear_list)
        elif choice == "3":
            lines = overdue_report(rentals, gear_list)
        elif choice == "4":
            lines = popular_gear_report(rentals, gear_list)
        elif choice == "5":
            lines = revenue_report(rentals, gear_list, pickup_points)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Enter 1-6.")
            continue
        print_lines(lines)
        if get_yes_or_no("\nSave this report to reports.txt? (yes/no): "):
            save_report(lines)
        pause()


# extra: saved reports are added to the end of reports.txt with the time they were saved
def save_report(lines):
    with open(REPORT_FILE, "a", encoding="utf-8") as file:
        file.write(f"Saved {datetime.now().strftime('%m/%d/%Y %H:%M')}\n")
        for line in lines:
            file.write(line + "\n")
        file.write("\n")
    print("Report saved to reports.txt.")


def daily_rentals_report(rentals, gear_list):
    date = get_date("Date (MM/DD/YYYY): ")
    matches = []
    for rental in rentals:
        if rental.get_date() == date:
            matches.append(rental)
    lines = heading(f"Rentals on {date}")
    if matches:
        return lines + rental_table(matches, gear_list)
    return lines + [f"No rentals on {date}."]


def gear_out_report(rentals, gear_list):
    lines = heading("Gear Currently Out")
    out = open_rentals(rentals)
    if out:
        return lines + rental_table(out, gear_list)
    return lines + ["No gear is out right now."]


def overdue_report(rentals, gear_list):
    now = datetime.now()
    lines = heading("Overdue Rentals")
    lines.append(f"\n{'ID':<5}{'Email':<24}{'Item':<26}{'Date':<12}{'Start':<7}{'Time Out':>14}")
    lines.append("-" * 88)
    found = False
    for rental in open_rentals(rentals):
        minutes = rental.minutes_out(now)
        if minutes > OVERDUE_LIMIT_MINUTES:
            found = True
            # 1440 minutes in a day, 60 in an hour
            time_out = f"{minutes // 1440}d {minutes // 60 % 24}h {minutes % 60:02d}m"
            lines.append(f"{rental.get_id():<5}{rental.get_email():<24}{item_name(gear_list, rental.get_gear_id()):<26}"
                         f"{rental.get_date():<12}{rental.get_start():<7}{time_out:>14}")
    if not found:
        lines.append("No rentals are overdue.")
    return lines


def popular_gear_report(rentals, gear_list):
    # count the rentals for each item then sort the [count, item] pairs so the biggest count is first
    pairs = []
    for gear in gear_list:
        count = 0
        for rental in rentals:
            if rental.get_gear_id() == gear.get_id():
                count += 1
        pairs.append([count, gear.get_item()])
    pairs.sort(reverse=True)
    lines = heading("Most Popular Gear")
    lines.append(f"\n{'Rank':<6}{'Item':<26}{'Rentals':>7}")
    lines.append("-" * 39)
    for rank, pair in enumerate(pairs, start=1):
        lines.append(f"{rank:<6}{pair[1]:<26}{pair[0]:>7}")
    return lines


# only completed rentals have a cost
def revenue_report(rentals, gear_list, pickup_points):
    lines = heading("Revenue by Gear Item")
    for gear in gear_list:
        money = 0.0
        for rental in rentals:
            if rental.get_status() == "Completed" and rental.get_gear_id() == gear.get_id():
                money += rental.get_cost()
        lines.append(f"{gear.get_item():<26}${money:>9.2f}")
    lines += heading("Revenue by Pickup Point")
    # every rental has a pickup point, so adding these up gives the total
    total = 0.0
    for point in pickup_points:
        money = 0.0
        for rental in rentals:
            if rental.get_status() == "Completed" and rental.get_pickup_id() == point.get_id():
                money += rental.get_cost()
        total += money
        lines.append(f"{point.get_location():<26}${money:>9.2f}")
    lines.append("-" * 36)
    lines.append(f"{'Total':<26}${total:>9.2f}")
    return lines


#starts code
main()
