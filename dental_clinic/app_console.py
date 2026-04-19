import os
from collections import deque
from datetime import datetime, timedelta
import random

# Data structures in memory
clients = []
daily_queue = deque()
contingency_stack = []

# Pricing logic based on provided table
base_fees = {
    'Private': 80000,
    'EPS': 5000,
    'Prepaid': 30000
}

attention_fees = {
    'Private': {
        'Cleaning': 60000,
        'Fillings': 80000,
        'Extraction': 100000,
        'Diagnosis': 50000
    },
    'EPS': {
        'Cleaning': 0,
        'Fillings': 40000,
        'Extraction': 40000,
        'Diagnosis': 0
    },
    'Prepaid': {
        'Cleaning': 0,
        'Fillings': 10000,
        'Extraction': 10000,
        'Diagnosis': 0
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dashboard():
    clear_screen()
    total_clients = len(clients)
    total_income = sum(c['total_value'] for c in clients)
    extractions_count = sum(1 for c in clients if c['attention_type'] == 'Extraction')
    
    print("\n" + "="*40)
    print(" " * 14 + "DASHBOARD")
    print("="*40)
    print(f"Total Clients:       {total_clients}")
    print(f"Total Income:        ${total_income:,.2f}")
    print(f"Pending Extractions: {extractions_count}")
    print("="*40)
    input("\nPress Enter to continue...")

def register_client():
    clear_screen()
    print("\n--- Register Client Appointment ---")
    id_card = input("ID Card: ")
    name = input("Full Name: ")
    phone = input("Phone: ")
    
    # Client Type
    while True:
        print("\nClient Types: 1. Private, 2. EPS, 3. Prepaid")
        c_choice = input("Select Client Type (1-3): ")
        if c_choice == '1': client_type = 'Private'; break
        elif c_choice == '2': client_type = 'EPS'; break
        elif c_choice == '3': client_type = 'Prepaid'; break
        else: print("Invalid option.")

    # Attention Type
    while True:
        print("\nAttention Types: 1. Cleaning, 2. Fillings, 3. Extraction, 4. Diagnosis")
        a_choice = input("Select Attention Type (1-4): ")
        if a_choice == '1': attention_type = 'Cleaning'; break
        elif a_choice == '2': attention_type = 'Fillings'; break
        elif a_choice == '3': attention_type = 'Extraction'; break
        elif a_choice == '4': attention_type = 'Diagnosis'; break
        else: print("Invalid option.")

    # Quantity
    if attention_type in ['Cleaning', 'Diagnosis']:
        quantity = 1
        print(f"Quantity fixed at 1 for {attention_type}.")
    else:
        while True:
            try:
                quantity = int(input(f"Quantity for {attention_type} (> 0): "))
                if quantity > 0:
                    break
                print("Must be greater than 0.")
            except ValueError:
                print("Enter a valid number.")

    # Priority
    while True:
        print("\nPriorities: 1. Normal, 2. Urgent")
        p_choice = input("Select Priority (1-2): ")
        if p_choice == '1': priority = 'Normal'; break
        elif p_choice == '2': priority = 'Urgent'; break
        else: print("Invalid option.")

    appointment_date = input("\nAppointment Date (YYYY-MM-DD): ")
    appointment_time = input("Appointment Time (HH:MM): ")
    
    # Calculation
    base_value = base_fees.get(client_type, 0)
    attention_value = attention_fees.get(client_type, {}).get(attention_type, 0)
    total_value = base_value + (attention_value * quantity)
    
    client = {
        'id_card': id_card,
        'name': name,
        'phone': phone,
        'client_type': client_type,
        'attention_type': attention_type,
        'quantity': quantity,
        'priority': priority,
        'appointment_date': appointment_date,
        'appointment_time': appointment_time,
        'total_value': total_value,
        'timestamp': datetime.now()
    }
    
    clients.append(client)
    daily_queue.append(client)
    
    # Sort FIFO queue by date and time (earliest first)
    temp_queue = sorted(list(daily_queue), key=lambda x: (x['appointment_date'], x['appointment_time']))
    daily_queue.clear()
    daily_queue.extend(temp_queue)
    
    if attention_type == 'Extraction' and priority == 'Urgent':
        contingency_stack.append(client)
        # Sort the stack so that the closest date and time is at the END (top of the stack)
        contingency_stack.sort(key=lambda x: (x['appointment_date'], x['appointment_time']), reverse=True)
        
    print(f"\n[SUCCESS] Client {name} registered successfully.")
    print(f"Total to pay: ${total_value:,.2f}")
    input("\nPress Enter to continue...")

def generate_random_clients():
    clear_screen()
    print("\n--- Generate Random Clients ---")
    try:
        count_input = input("How many random clients to generate? (default 5): ")
        count = int(count_input) if count_input.strip() else 5
    except ValueError:
        count = 5
        
    mock_names = ["John Smith", "Mary Johnson", "Charles Williams", "Anna Brown", "Luis Jones", "Laura Garcia", "George Miller", "Martha Davis", "Peter Rodriguez", "Helen Martinez", "Diana Hernandez", "Andrew Lopez"]
    client_types = ["Private", "EPS", "Prepaid"]
    attention_types = ["Cleaning", "Fillings", "Extraction", "Diagnosis"]
    priorities = ["Normal", "Urgent"]
    
    for _ in range(count):
        name = random.choice(mock_names) + " " + str(random.randint(1, 100))
        id_card = str(random.randint(10000000, 999999999))
        phone = "3" + str(random.randint(0, 999999999)).zfill(9)
        client_type = random.choice(client_types)
        attention_type = random.choice(attention_types)
        priority = random.choice(priorities)
        
        if attention_type in ['Cleaning', 'Diagnosis']:
            quantity = 1
        else:
            quantity = random.randint(1, 4)
            
        random_days = random.randint(1, 30)
        appointment_date = (datetime.now() + timedelta(days=random_days)).strftime('%Y-%m-%d')
        appointment_time = f"{random.randint(8, 17):02d}:{random.choice(['00', '15', '30', '45'])}"
        
        base_value = base_fees.get(client_type, 0)
        attention_value = attention_fees.get(client_type, {}).get(attention_type, 0)
        total_value = base_value + (attention_value * quantity)
        
        client = {
            'id_card': id_card,
            'name': name,
            'phone': phone,
            'client_type': client_type,
            'attention_type': attention_type,
            'quantity': quantity,
            'priority': priority,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'total_value': total_value,
            'timestamp': datetime.now()
        }
        
        clients.append(client)
        daily_queue.append(client)
        
        if attention_type == 'Extraction' and priority == 'Urgent':
            contingency_stack.append(client)
            contingency_stack.sort(key=lambda x: (x['appointment_date'], x['appointment_time']), reverse=True)
            
    # Sort FIFO queue by date and time (earliest first)
    temp_queue = sorted(list(daily_queue), key=lambda x: (x['appointment_date'], x['appointment_time']))
    daily_queue.clear()
    daily_queue.extend(temp_queue)
            
    print(f"\n[SUCCESS] Successfully generated and registered {count} random clients.")
    input("\nPress Enter to continue...")

def list_clients():
    clear_screen()
    print("\n--- Clients List ---")
    search_id = input("Search by ID Card (leave blank for all): ").strip()
    
    # Sort descending by value
    sorted_clients = sorted(clients, key=lambda x: x['total_value'], reverse=True)
    
    if search_id:
        sorted_clients = [c for c in sorted_clients if c['id_card'] == search_id]
        
    if not sorted_clients:
        print("\nNo clients found.")
    else:
        print("\n{:<22} | {:<12} | {:<18} | {:<12} | {:<18} | {:<12}".format(
            "Name", "ID Card", "Attention (Qty)", "Type/Priority", "Date & Time", "Total"
        ))
        print("-" * 105)
        for c in sorted_clients:
            attention_str = f"{c['attention_type']} ({c['quantity']})"
            type_prio_str = f"{c['client_type']}/{c['priority']}"
            datetime_str = f"{c['appointment_date']} {c['appointment_time']}"
            print("{:<22} | {:<12} | {:<18} | {:<12} | {:<18} | ${:,.2f}".format(
                c['name'][:22], c['id_card'], attention_str, type_prio_str, datetime_str, c['total_value']
            ))
            
    input("\nPress Enter to continue...")

def manage_agenda():
    clear_screen()
    print("\n--- Daily Queue (Agenda) ---")
    
    if not daily_queue:
        print("\nThe daily queue is empty.")
    else:
        print("\nNext patients in queue (Earliest First):")
        print("\n{:<5} | {:<22} | {:<12} | {:<15} | {:<18}".format(
            "Pos", "Name", "ID Card", "Attention", "Date & Time"
        ))
        print("-" * 80)
        for i, c in enumerate(daily_queue, 1):
            datetime_str = f"{c['appointment_date']} {c['appointment_time']}"
            print("{:<5} | {:<22} | {:<12} | {:<15} | {:<18}".format(
                i, c['name'][:22], c['id_card'], c['attention_type'], datetime_str
            ))
            
        print("\nOptions:")
        print("1. Call Next Patient (Pop First)")
        print("2. Back to Menu")
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            attended_client = daily_queue.popleft()
            # Remove from contingency stack if also present there
            if attended_client in contingency_stack:
                contingency_stack.remove(attended_client)
            print(f"\n[!] Called from queue: {attended_client['name']} (ID: {attended_client['id_card']})")
        
    input("\nPress Enter to continue...")

def manage_contingency():
    clear_screen()
    print("\n--- Contingency Stack (Urgent Extractions) ---")
    
    if not contingency_stack:
        print("\nThe contingency stack is empty. No urgent extractions pending.")
    else:
        stack_view = list(reversed(contingency_stack))
        print("\nUrgent Stack (Top is closest appointment date):")
        print("\n{:<5} | {:<22} | {:<12} | {:<18}".format(
            "Pos", "Name", "ID Card", "Date & Time"
        ))
        print("-" * 65)
        for i, c in enumerate(stack_view, 1):
            datetime_str = f"{c['appointment_date']} {c['appointment_time']}"
            pos_label = "TOP" if i == 1 else str(i)
            print("{:<5} | {:<22} | {:<12} | {:<18}".format(
                pos_label, c['name'][:22], c['id_card'], datetime_str
            ))
            
        print("\nOptions:")
        print("1. Attend Urgent Extraction (Pop Top)")
        print("2. Back to Menu")
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            attended_client = contingency_stack.pop()
            # Remove from daily queue if also present there
            if attended_client in daily_queue:
                daily_queue.remove(attended_client)
            print(f"\n[!] Attended from urgent stack: {attended_client['name']} (ID: {attended_client['id_card']})")
            
    input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print("\n" + "="*45)
        print(" " * 8 + "DENTAL CLINIC SYSTEM (CLI MODE)")
        print("="*45)
        print("1. Dashboard")
        print("2. Register Client Appointment")
        print("3. Generate Random Clients (For Testing)")
        print("4. View Clients List & Search")
        print("5. Manage Daily Queue (FIFO Agenda)")
        print("6. Manage Contingency Stack (Urgencies)")
        print("7. Exit")
        print("="*45)
        
        choice = input("\nSelect an option (1-7): ")
        
        if choice == '1':
            show_dashboard()
        elif choice == '2':
            register_client()
        elif choice == '3':
            generate_random_clients()
        elif choice == '4':
            list_clients()
        elif choice == '5':
            manage_agenda()
        elif choice == '6':
            manage_contingency()
        elif choice == '7':
            print("\nExiting system... Goodbye!\n")
            break
        else:
            print("\nInvalid option. Press Enter to try again.")
            input()

if __name__ == '__main__':
    main()
