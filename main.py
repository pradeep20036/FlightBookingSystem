
# ----------------------------------Supporting libraries and modules--------------------
import random
import datetime
import mysql.connector


# -------------------------------------FLIGHT BOOKING SYSTEM---------------------------------------
# OOPD Project 1
# Deepankar Kansal
# Pradeep Kumar

# -------------------------

# assuming the number of tickets as 100
tickets_available = 100


# connecting with the database
mydb = mysql.connector.connect(host="localhost", user="root", password="root", port="3306", database="oopd")

# creating an instance of database, all the operation on db will be performed using this reference.

mycursor = mydb.cursor()


# flight booking function
def flight_booking():

    choice=input("select your choice \n 1. Flight booking \n 2. Cancel booking\n")
    if choice=='1':
        amount,flight_no = flight_search()
        print("\n\nAmount to be paid:{0:d}".format(amount))
    #     after the ticket price is calculated
    # taking the user information and putting in pnr table

    # if choice 2 is entered then it will select cancel_booking() function
    elif choice=='2':
        cancel_booking()
    else:
        print("please enter a valid choice")
    # print(amount)

# function searches the flight by taking the valid inputs from the user
def flight_search():
    #     taking flight details
    src = input("Enter Source:")
    dest = input("Enter Destination:")
    d_date = input("Enter Departure Date(YYYY-MM-DD):")

    # executing the query to get all the available flight as per the requirement by the user

    mycursor.execute("select * from flight_info where source = '"+src+"' and destination = '"+dest+"' and departure_date = '"+d_date+"'")
    avl = []
    for db in mycursor:
        avl.append(db)

    # display available flights
    flight_no = available_flight(avl)
    amount = seatType(avl, flight_no)
    flg = input("Do you want Ancillaries to add (yes or no):")
    if (flg == 'yes'):
        amount = ancillaries(amount)

    # calling pnr function to take the user information once the flight is selected
    pnr(amount, flight_no)
    return amount,flight_no

# function to print all the available flights
def available_flight(avl):
    print("These are available flights:\n")
    check = 0
    for i in avl:
        print("Flight Number:")
        for j in i:
            check = 1
            print(j,end=" ")
        print("\n")
    if(check == 1):
        flight_no = input("Please select flight number you are comfortable with:")

    return flight_no

# supporting function to add the seat type and modify the ticket price
def seatType(avl, flight_no):
    seat = input("Please enter seat type \n(F for first class)\t(B for business class)\t(E for economy class):")
    amnt = 5000
    for i in avl:
        # print(i[len(i) - 1], flight_no)
        if(i[0] == flight_no):
            amnt = i[len(i) - 1]
            # print(1010)
            if (seat == 'F'):
                amnt = i[len(i) - 1] + 1000
            elif (seat == 'B'):
                amnt = i[len(i) - 1] + 500
                # print(amnt)
    return amnt

# supporting function to provide ancillaries addition
def ancillaries(amnt):
    bvg = input("Do you want Beverages to add (yes or no):")
    if(bvg == 'yes'):
        amnt += 250
    el = input("Do you want Extra luggage to add (yes or no):")
    if (el == 'yes'):
        amnt += 500
    intr = input("Do you want Internet service to add (yes or no):")
    if (intr == 'yes'):
        amnt += 350
    wsa = input("Do you want Wide Seat Area(yes or no):")
    if (wsa == 'yes'):
        amnt += 250

    return amnt


# function to take customer information and stores in the database

def pnr(amount,flight_no):
    print("Enter details below")
    name = input("Name:")
    gen = input("Gender:")
    dob = input("Date of birth(YYYY-MM-DD):")
    contact = input("Contact number:")
    email = input("E-Mail ID:")

    # query to insert the information in the database"Insert into pnr values("
    qry = +contact+"','"+email+"','"+name+"','"+gen+"','"+dob+"')"
    try:
        mycursor.execute(qry)
    except:
        print("Please enter valid credentials!")
        return
    # calling the payment function after taking the customer information
    ticket_id = payment(amount, contact)

    # ticket_id used to print in the ticket

    # code to get the flight information to print in the ticket
    mycursor.execute("select * from flight_info where flight_no='"+flight_no+"'")
    avl = []
    for db in mycursor:
        avl.append(db)

    tup = avl[0]
    str = [""]*6
    j=0
    for i in tup:
        str[j] = i
        j+=1

    source = str[1]
    destination = str[2]
    dt = str[3]
    d_date = dt.strftime('%Y-%m-%d')
    # print(type(ticket_id))

    ticket_booked(flight_no, source, destination, d_date, ticket_id, name, contact, email)

# function to handle the payment made by the user
def payment(amount,contact):

    while(1):
        print("Enter your card number")
        card_number=input()
        if(len(card_number)==16):
            break
        else:
            print("Length must be 16!")
    while (1):
        print("Enter your CVV")
        cvv = input()
        if (len(cvv) == 3):
            break
        else:
            print("Length must be 3!")
    while (1):
        print("Enter OTP")
        otp = input()
        if (len(otp) == 6):
            break
        else:
            print("Invalid OTP!")

    ticket_id=random.randrange(1, 1000, 1)

    confirmation(ticket_id, contact, amount)
    return ticket_id

# function for the payment confirmation and putting the record in the payment table
def confirmation(ticket_id, contact, amount):
    qry = "Insert into payment values(" + str(ticket_id) + ",'" + contact + "'," + str(amount) + ")"
    mycursor.execute(qry)

    print("Payment successfull")
    return ticket_id

# function to print the ticket booked
def ticket_booked(flight_no, source, destination, d_date, ticket_id, name, contact, email):
    print("\n\nYour Ticket is Booked")

    print("------------------------------------------------------")
    #     generate ticket
    print("Flight Number:'" + flight_no +"'")
    print("Flight From '"+source+"' Destination '"+destination+"'")
    print("Departure Date:'" + d_date + "'")
    print("Ticket ID: {0:d}".format(ticket_id))
    print("Name of person:'"+name+"'")
    print("contact Number:'" + contact +"'")
    print("Email id:'" + email +"'")

    print("------------------------------------------------------")

# 1 flight_booking
# 2 cancel_booking

# function enable cancel booking
def cancel_booking():
    t_id = int(input("Enter your Ticket ID:"))
    check_booking(t_id)

# function to check if the booking is valid or not by taking t_id as parameter
def check_booking(t_id):
    qry = "select * from payment where ticket_id = "+str(t_id)

    mycursor.execute(qry)
    booking = []
    flag = 0
    amnt = 0
    for data in mycursor:
        flag = 1
        amnt = data[2]

    if (flag == 1):
        refund_processing(amnt,t_id)
    else:
        no_such_booking()

# function to process the refund if any.
def refund_processing(amnt, t_id):
    print("\n\n----------------------------------")
    print("Your amount of {0:d} will be refunded shortly...".format(amnt))
    # removing the booking from the table
    remove_booking(t_id)
    ticket_canceled()
    print("--------------------------------------")

# supporting function
def no_such_booking():
    print("\n\n----------------------------------")
    print("No Such Booking!!!\nPlease check your Ticket ID...")
    print("--------------------------------------")

# function to remove_booking if existed as per the mentioned t_id given.
def remove_booking(t_id):
    qry = "delete from payment where ticket_id = " + str(t_id)
    check = mycursor.execute(qry)
    print("Booking Removed...")

# supporting function
def ticket_canceled():
    print("\nYour ticket has canceled successfully...")

def upi_payment():
    print("payment code need to be added here")
    print("payment is successfully using UPI")

# -------------------------------------------------------------------------------------------

# Calling the flight_booking function which is handling all other cases of the system
flight_booking()

# command to commit the changes made in the database instance to the original database.
mydb.commit()


# ............................End of the code.............................................


