from flask import Flask, render_template, request, redirect, url_for, flash
from collections import deque
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_dental_clinic'

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

@app.route('/')
def index():
    total_clients = len(clients)
    total_income = sum(c['total_value'] for c in clients)
    extractions_count = sum(1 for c in clients if c['attention_type'] == 'Extraction')
    
    return render_template('index.html', 
                           total_clients=total_clients, 
                           total_income=total_income, 
                           extractions_count=extractions_count)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id_card = request.form['id_card']
        name = request.form['name']
        phone = request.form['phone']
        client_type = request.form['client_type']
        attention_type = request.form['attention_type']
        quantity = int(request.form['quantity'])
        priority = request.form['priority']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        
        # Validation for quantity
        if attention_type in ['Cleaning', 'Diagnosis'] and quantity != 1:
            flash("For Cleaning and Diagnosis, the quantity must be exactly 1.")
            return redirect(url_for('register'))
        elif quantity <= 0:
            flash("The quantity must be greater than 0.")
            return redirect(url_for('register'))
            
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
            
        flash(f"Client {name} registered successfully. Total to pay: ${total_value:,.2f}")
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/generate_random', methods=['POST'])
def generate_random():
    try:
        count = int(request.form.get('count', 1))
    except ValueError:
        count = 1
        
    mock_names = ["John Smith", "Mary Johnson", "Charles Williams", "Anna Brown", "Luis Jones", "Laura Garcia", "George Miller", "Martha Davis", "Peter Rodriguez", "Helen Martinez", "Diana Hernandez", "Andrew Lopez", "Sophia Gonzalez"]
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
            
    flash(f"Successfully generated and registered {count} random clients.")
    return redirect(url_for('list_clients'))

@app.route('/clients')
def list_clients():
    search_id = request.args.get('id_card', '')
    
    # Sort descending by value
    sorted_clients = sorted(clients, key=lambda x: x['total_value'], reverse=True)
    
    if search_id:
        # Search by specific ID
        sorted_clients = [c for c in sorted_clients if c['id_card'] == search_id]
        
    return render_template('clients.html', clients=sorted_clients, search_id=search_id)

@app.route('/contingency', methods=['GET', 'POST'])
def contingency():
    if request.method == 'POST':
        if contingency_stack:
            attended_client = contingency_stack.pop()
            
            # Remove from daily queue if also present there
            if attended_client in daily_queue:
                daily_queue.remove(attended_client)
                
            flash(f"Urgency called from stack: {attended_client['name']} (ID: {attended_client['id_card']})")
        else:
            flash("The urgency stack is empty.")
        return redirect(url_for('contingency'))
        
    # The view shows the stack from top to bottom
    stack_view = list(reversed(contingency_stack))
    return render_template('contingency.html', stack=stack_view)

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        if daily_queue:
            attended_client = daily_queue.popleft()
            
            # Remove from contingency stack if also present there
            if attended_client in contingency_stack:
                contingency_stack.remove(attended_client)
                
            flash(f"Client called from queue: {attended_client['name']} (ID: {attended_client['id_card']})")
        else:
            flash("The daily queue is empty.")
        return redirect(url_for('agenda'))
        
    return render_template('agenda.html', queue=list(daily_queue))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
