Manager PIN: 1234 which is asked before the Manager Menu and Reports (imporant)
Extras
Manager PIN - the Manager Menu and Reports ask for the PIN first. After 3 wrong tries it goes back to the main menu.
Overdue fee at return - a $10.00 late fee is added when gear comes back after the 4 hour limit. It shows on the receipt.
Game-day pricing - a rental that starts on a home-game Saturday costs 1.5x the hourly rate. The dates are in HOME_GAMES at the top of app.py.
Student discount - customers with a @crimson.ua.edu email get 10% off (tyler and maya in customers.txt).
Save reports to a text file - after any report you can save it. Each saved report is added to the end of reports.txt with the date and time.
My own ideas that i put in code:
Multi-day returns - ending a rental asks for the return date (Enter keeps the rental date), so gear can come back after midnight or days later and every hour still counts.
Revenue report total - the revenue report shows the total of all completed rentals.
Gear safety checks - gear can't be removed while units are rented out, total units can't be set below the units rented out, and a removed gear ID is never given to new gear so old rentals don't point at the wrong item.
Inactive customers can still sign in to browse and see their history, they just can't start a rental.
Overdue updates by itself - every time the main menu shows, any rental out more than 4 hours is marked Overdue and saved.
Overdue report shows time out in days, hours and minutes.
