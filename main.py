from datetime import datetime

print("Welcome to Smart Complaint Analyzer!")
print("===== SMART COMPLAINT ANALYZER =====")
print("1. Register")
print("2. Login")

choice = input("Choose an option: ")

if choice == "1":
    print("New customer registration")

    customer_name = input("Enter your name: ")
    phone_number = input("Enter your phone number: ")
    password = input("Create your password: ")
    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        exit()

    with open("customers.txt", "a") as customer_file:
        customer_file.write(customer_name + "," + phone_number + "," + password + "\n")

    print("Registration successful!")

elif choice == "2":
    print("Customer login")

    phone_number = input("Enter your phone number: ")
    password = input("Enter your password: ")

    login_success = False
    customer_name = ""

    with open("customers.txt", "r") as customer_file:
        for line in customer_file:
            saved_details = line.strip().split(",")

            if len(saved_details) == 3:
                saved_name = saved_details[0]
                saved_phone = saved_details[1]
                saved_password = saved_details[2]

                if phone_number == saved_phone and password == saved_password:
                    customer_name = saved_name
                    login_success = True
                    break

    if not login_success:
        print("Incorrect phone number or password!")
        exit()

    print("Login successful!")

else:
    print("Invalid choice!")
    exit()

print("\n===== CUSTOMER DASHBOARD =====")
print("1. Submit a New Complaint")
print("2. Check Complaint Status")
print("3. View All Complaints")
print("4. Give Feedback About Our Website")

dashboard_choice = input("Choose an option: ")

if dashboard_choice == "1":
    complaint = input("Give a complaint: ")

    ticket_id = datetime.now().strftime("%Y%m%d%H%M%S")
    complaint_lower = complaint.lower()

    if "payment" in complaint_lower:
        category = "Payment"
    elif "order" in complaint_lower:
        category = "Order"
    elif "delivery" in complaint_lower or "arrived" in complaint_lower:
        category = "Delivery"
    else:
        category = "General"

    if "urgent" in complaint_lower or "not working" in complaint_lower:
        priority = "High"
    else:
        priority = "Normal"

    status = "Open"

    with open("complaints.txt", "a") as file:
        file.write(f"Ticket ID: {ticket_id}\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write(f"Complaint: {complaint}\n")
        file.write(f"Category: {category}\n")
        file.write(f"Priority: {priority}\n")
        file.write(f"Status: {status}\n")
        file.write("-------------------------\n")

    print("\n--- Complaint Submitted Successfully ---")
    print("Customer Name:", customer_name)
    print("Ticket ID:", ticket_id)
    print("Category:", category)
    print("Priority:", priority)
    print("Status:", status)

elif dashboard_choice == "2":
    search_id = input("Enter your Ticket ID: ")
    found = False

    with open("complaints.txt", "r") as file:
        for line in file:
            if search_id in line:
                found = True
                break

    if found:
        print("Complaint found!")
        print("Status: Open")
    else:
        print("Complaint not found!")

elif dashboard_choice == "3":
    print("\n--- All Saved Complaints ---")

    try:
        with open("complaints.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No complaints found yet.")

elif dashboard_choice == "4":
    feedback = input("Please share your feedback: ")

    with open("feedback.txt", "a") as file:
        file.write(feedback + "\n")

    print("Thank you! Your feedback has been saved.")

else:
    print("Invalid choice!")