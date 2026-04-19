from flask import Flask, render_template, request, redirect, url_for, flash
from jinja2 import DictLoader
from collections import deque
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_dental_clinic'

template_dict = {
    'base.html': r'''<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dental Clinic - programacion 2</title>
    <!-- Tailwind CSS (CDN for rapid prototyping) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0ea5e9',
                            600: '#0284c7',
                            700: '#0369a1',
                            900: '#0c4a6e',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="h-full flex flex-col font-sans text-slate-800 antialiased">
    
    <!-- Navbar -->
    <nav class="bg-brand-700 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center gap-2">
                        <!-- Tooth Icon SVG -->
                        <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                        <span class="text-white font-bold text-xl tracking-wide">programacion 2</span>
                    </div>
                    <div class="hidden md:block">
                        <div class="ml-10 flex items-baseline space-x-4">
                            <a href="{{ url_for('index') }}" class="text-brand-100 hover:bg-brand-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Home</a>
                            <a href="{{ url_for('register') }}" class="text-brand-100 hover:bg-brand-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Register Appointment</a>
                            <a href="{{ url_for('list_clients') }}" class="text-brand-100 hover:bg-brand-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Clients</a>
                            <a href="{{ url_for('agenda') }}" class="text-brand-100 hover:bg-brand-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Daily Queue</a>
                            <a href="{{ url_for('contingency') }}" class="text-brand-100 hover:bg-brand-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Urgent Stack</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 w-full">
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="mb-8 space-y-4">
                    {% for message in messages %}
                        <div class="flex items-center p-4 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 shadow-sm" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5 mr-3 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="font-medium">{{ message }}</span>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="p-6 sm:p-8">
                {% block content %}{% endblock %}
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 mt-auto">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <p class="text-center text-sm text-slate-500">
                &copy; 2026 programacion 2. All rights reserved.
            </p>
        </div>
    </footer>
</body>
</html>''',

    'index.html': r'''{% extends "base.html" %}

{% block content %}
<div class="border-b border-slate-200 pb-5 mb-8">
    <h2 class="text-2xl font-bold leading-7 text-slate-900 sm:text-3xl sm:truncate">Dashboard</h2>
    <p class="mt-2 max-w-4xl text-sm text-slate-500">Summary of the dental clinic operations.</p>
</div>

<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-10">
    <!-- Stat 1 -->
    <div class="bg-white overflow-hidden rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0 bg-brand-100 rounded-md p-3">
                    <svg class="h-6 w-6 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-sm font-medium text-slate-500 truncate">Total Clients</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-semibold text-slate-900">{{ total_clients }}</div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
    </div>

    <!-- Stat 2 -->
    <div class="bg-white overflow-hidden rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0 bg-emerald-100 rounded-md p-3">
                    <svg class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-sm font-medium text-slate-500 truncate">Total Income</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-semibold text-slate-900">${{ "{:,.2f}".format(total_income) }}</div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
    </div>

    <!-- Stat 3 -->
    <div class="bg-white overflow-hidden rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0 bg-rose-100 rounded-md p-3">
                    <svg class="h-6 w-6 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-sm font-medium text-slate-500 truncate">Pending Extractions</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-semibold text-slate-900">{{ extractions_count }}</div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="bg-slate-50 rounded-lg p-6 border border-slate-200">
    <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">Quick Access</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <a href="{{ url_for('register') }}" class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
            New Appointment
        </a>
        <a href="{{ url_for('list_clients') }}" class="inline-flex justify-center items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
            View Clients
        </a>
        <a href="{{ url_for('agenda') }}" class="inline-flex justify-center items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
            Daily Queue
        </a>
        <a href="{{ url_for('contingency') }}" class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-rose-700 bg-rose-100 hover:bg-rose-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500">
            Urgency Stack
        </a>
    </div>
</div>
{% endblock %}''',

    'register.html': r'''{% extends "base.html" %}

{% block content %}
<div class="max-w-3xl mx-auto">
    <div class="border-b border-slate-200 pb-5 mb-8 flex justify-between items-end">
        <div>
            <h2 class="text-2xl font-bold leading-7 text-slate-900">Register Client Appointment</h2>
            <p class="mt-2 text-sm text-slate-500">Enter the patient's data to add them to the clinic's queue.</p>
        </div>
        <!-- Backend test generator -->
        <form action="{{ url_for('generate_random') }}" method="POST" class="flex items-center space-x-2">
            <label for="count" class="text-sm font-medium text-slate-700">Generate:</label>
            <input type="number" id="count" name="count" min="1" max="100" value="5" class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-16 sm:text-sm border-slate-300 rounded-md p-1.5 border" required>
            <button type="submit" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-slate-600 hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500">
                <svg class="-ml-1 mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                Insert Random
            </button>
        </form>
    </div>

    <form method="POST" class="space-y-6">
        <div class="bg-slate-50 p-6 rounded-lg border border-slate-200">
            <h3 class="text-lg font-medium leading-6 text-slate-900 mb-4">Personal Information</h3>
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                
                <div class="sm:col-span-3">
                    <label for="id_card" class="block text-sm font-medium text-slate-700">ID Card</label>
                    <div class="mt-1">
                        <input type="text" id="id_card" name="id_card" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                </div>

                <div class="sm:col-span-3">
                    <label for="phone" class="block text-sm font-medium text-slate-700">Phone</label>
                    <div class="mt-1">
                        <input type="text" id="phone" name="phone" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                </div>

                <div class="sm:col-span-6">
                    <label for="name" class="block text-sm font-medium text-slate-700">Full Name</label>
                    <div class="mt-1">
                        <input type="text" id="name" name="name" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                </div>

                <div class="sm:col-span-6">
                    <label for="client_type" class="block text-sm font-medium text-slate-700">Client Type</label>
                    <div class="mt-1">
                        <select id="client_type" name="client_type" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border bg-white">
                            <option value="Private">Private</option>
                            <option value="EPS">EPS</option>
                            <option value="Prepaid">Prepaid</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-slate-50 p-6 rounded-lg border border-slate-200">
            <h3 class="text-lg font-medium leading-6 text-slate-900 mb-4">Appointment Details</h3>
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                
                <div class="sm:col-span-3">
                    <label for="attention_type" class="block text-sm font-medium text-slate-700">Attention Type</label>
                    <div class="mt-1">
                        <select id="attention_type" name="attention_type" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border bg-white" onchange="validateQuantity()">
                            <option value="Cleaning">Cleaning (Quantity: 1)</option>
                            <option value="Fillings">Fillings</option>
                            <option value="Extraction">Extraction</option>
                            <option value="Diagnosis">Diagnosis (Quantity: 1)</option>
                        </select>
                    </div>
                </div>

                <div class="sm:col-span-3">
                    <label for="quantity" class="block text-sm font-medium text-slate-700">Quantity</label>
                    <div class="mt-1">
                        <input type="number" id="quantity" name="quantity" min="1" value="1" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                    <p class="mt-1 text-xs text-slate-500" id="quantity-help">For cleaning and diagnosis, must be 1.</p>
                </div>

                <div class="sm:col-span-3">
                    <label for="appointment_date" class="block text-sm font-medium text-slate-700">Appointment Date</label>
                    <div class="mt-1">
                        <input type="date" id="appointment_date" name="appointment_date" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                </div>

                <div class="sm:col-span-3">
                    <label for="appointment_time" class="block text-sm font-medium text-slate-700">Appointment Time</label>
                    <div class="mt-1">
                        <input type="time" id="appointment_time" name="appointment_time" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border">
                    </div>
                </div>

                <div class="sm:col-span-3">
                    <label for="priority" class="block text-sm font-medium text-slate-700">Priority</label>
                    <div class="mt-1">
                        <select id="priority" name="priority" required class="shadow-sm focus:ring-brand-500 focus:border-brand-500 block w-full sm:text-sm border-slate-300 rounded-md p-2 border bg-white">
                            <option value="Normal">Normal</option>
                            <option value="Urgent">Urgent</option>
                        </select>
                    </div>
                </div>

            </div>
        </div>

        <div class="pt-5 flex justify-end">
            <a href="{{ url_for('index') }}" class="bg-white py-2 px-4 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 mr-3">
                Cancel
            </a>
            <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
                Register Client
            </button>
        </div>
    </form>
</div>

<script>
    // Logic to auto-adjust "quantity" constraints dynamically
    function validateQuantity() {
        const attention = document.getElementById('attention_type').value;
        const quantityInput = document.getElementById('quantity');
        const helpText = document.getElementById('quantity-help');
        
        if (attention === 'Cleaning' || attention === 'Diagnosis') {
            quantityInput.value = 1;
            quantityInput.setAttribute('readonly', true);
            quantityInput.classList.add('bg-slate-100', 'text-slate-500');
            helpText.classList.replace('text-slate-500', 'text-brand-600');
            helpText.innerText = `Fixed at 1 for ${attention}.`;
        } else {
            quantityInput.removeAttribute('readonly');
            quantityInput.classList.remove('bg-slate-100', 'text-slate-500');
            helpText.classList.replace('text-brand-600', 'text-slate-500');
            helpText.innerText = 'Can be greater than 1.';
        }
    }

    // Call once on load
    validateQuantity();

</script>
{% endblock %}''',

    'clients.html': r'''{% extends "base.html" %}

{% block content %}
<div class="sm:flex sm:items-center sm:justify-between border-b border-slate-200 pb-5 mb-8">
    <div>
        <h2 class="text-2xl font-bold leading-7 text-slate-900">Clients List</h2>
        <p class="mt-2 text-sm text-slate-500">List of all registered patients, sorted by amount to pay (highest to lowest).</p>
    </div>
</div>

<!-- Search Bar -->
<div class="mb-6 bg-slate-50 p-4 rounded-lg border border-slate-200">
    <form method="GET" class="flex items-end gap-4">
        <div class="flex-1 max-w-sm">
            <label for="id_card" class="block text-sm font-medium text-slate-700 mb-1">Search by ID Card</label>
            <div class="relative rounded-md shadow-sm">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
                <input type="text" name="id_card" id="id_card" value="{{ search_id }}" class="focus:ring-brand-500 focus:border-brand-500 block w-full pl-10 sm:text-sm border-slate-300 rounded-md p-2 border" placeholder="Enter ID card number">
            </div>
        </div>
        <button type="submit" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
            Search
        </button>
        {% if search_id %}
            <a href="{{ url_for('list_clients') }}" class="inline-flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
                Clear
            </a>
        {% endif %}
    </form>
</div>

<!-- Table -->
<div class="flex flex-col">
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
            <div class="shadow overflow-hidden border-b border-slate-200 sm:rounded-lg">
                <table class="min-w-full divide-y divide-slate-200">
                    <thead class="bg-slate-50">
                        <tr>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Patient</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">ID Card</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Attention</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Type/Priority</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date and Time</th>
                            <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">Value to Pay</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-slate-200">
                        {% for client in clients %}
                        <tr class="hover:bg-slate-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-slate-900">{{ client.name }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                                {{ client.id_card }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                    {% if client.attention_type == 'Extraction' %}bg-rose-100 text-rose-800
                                    {% elif client.attention_type == 'Cleaning' %}bg-emerald-100 text-emerald-800
                                    {% elif client.attention_type == 'Fillings' %}bg-blue-100 text-blue-800
                                    {% else %}bg-purple-100 text-purple-800{% endif %}">
                                    {{ client.attention_type }} ({{ client.quantity }})
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                                <div>{{ client.client_type }}</div>
                                <div class="text-xs {% if client.priority == 'Urgent' %}text-rose-600 font-bold{% endif %}">{{ client.priority }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                                {{ client.appointment_date }}<br>
                                <span class="text-xs text-slate-400">{{ client.appointment_time }}</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium text-slate-900">
                                ${{ "{:,.2f}".format(client.total_value) }}
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="6" class="px-6 py-10 text-center text-sm text-slate-500">
                                <svg class="mx-auto h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                                </svg>
                                <span class="block mt-2 font-medium">No clients found.</span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'contingency.html': r'''{% extends "base.html" %}

{% block content %}
<div class="sm:flex sm:items-center sm:justify-between border-b border-slate-200 pb-5 mb-8">
    <div>
        <h2 class="text-2xl font-bold leading-7 text-rose-700 flex items-center gap-2">
            <svg class="h-6 w-6 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Contingency: Urgent Extractions (Stack)
        </h2>
        <p class="mt-2 text-sm text-slate-500">Contingency plan. Attended by prioritizing the closest appointment date (Last in, first out adapted by date).</p>
    </div>
    <div class="mt-4 sm:mt-0">
        <form method="POST">
            <button type="submit" 
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white {% if stack %}bg-rose-600 hover:bg-rose-700{% else %}bg-slate-400 cursor-not-allowed{% endif %} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500"
                {% if not stack %}disabled{% endif %}>
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Attend Urgency
            </button>
        </form>
    </div>
</div>

<div class="bg-rose-50 rounded-lg p-6 border border-rose-200 shadow-inner">
    
    <div class="flex flex-col gap-3 relative">
        <!-- Visualization of a stack -->
        {% for client in stack %}
            <div class="bg-white rounded-lg shadow-md border-2 {% if loop.index == 1 %}border-rose-500 z-10 transform scale-100{% else %}border-rose-200 opacity-90 scale-95{% endif %} p-4 flex justify-between items-center transition-all">
                <div class="flex items-center gap-4">
                    <div class="flex-shrink-0">
                        {% if loop.index == 1 %}
                            <span class="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-bold bg-rose-100 text-rose-800 uppercase tracking-wider">
                                Top (Next)
                            </span>
                        {% else %}
                            <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-rose-100 text-rose-600 font-bold text-sm">
                                #{{ loop.index }}
                            </span>
                        {% endif %}
                    </div>
                    <div>
                        <h4 class="text-lg font-bold text-slate-900">{{ client.name }}</h4>
                        <p class="text-sm text-slate-500">ID: {{ client.id_card }}</p>
                    </div>
                </div>
                <div class="text-right">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 mb-1">
                        URGENT
                    </span>
                    <p class="text-sm font-medium text-slate-700 flex items-center justify-end">
                        <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Appt Date: {{ client.appointment_date }} {{ client.appointment_time }}
                    </p>
                </div>
            </div>
            
            {% if not loop.last %}
            <div class="absolute left-1/2 transform -translate-x-1/2 w-0.5 h-6 bg-rose-200 -z-10" style="top: {{ loop.index * 100 }}px"></div>
            {% endif %}
            
        {% else %}
            <div class="text-center py-10 bg-white rounded-lg border border-dashed border-rose-300">
                <svg class="mx-auto h-12 w-12 text-rose-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-rose-500 font-medium">No urgent extractions pending.</p>
                <p class="text-sm text-rose-400">The stack is empty.</p>
            </div>
        {% endfor %}
    </div>
    
</div>
{% endblock %}''',

    'agenda.html': r'''{% extends "base.html" %}

{% block content %}
<div class="sm:flex sm:items-center sm:justify-between border-b border-slate-200 pb-5 mb-8">
    <div>
        <h2 class="text-2xl font-bold leading-7 text-slate-900 flex items-center gap-2">
            <svg class="h-6 w-6 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Daily Queue
        </h2>
        <p class="mt-2 text-sm text-slate-500">Strict management ordered by Date and Time (Earliest first).</p>
    </div>
    <div class="mt-4 sm:mt-0">
        <form method="POST">
            <button type="submit" 
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white {% if queue %}bg-brand-600 hover:bg-brand-700{% else %}bg-slate-400 cursor-not-allowed{% endif %} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500"
                {% if not queue %}disabled{% endif %}>
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Call Next
            </button>
        </form>
    </div>
</div>

<div class="bg-white shadow overflow-hidden sm:rounded-md border border-slate-200">
    <ul class="divide-y divide-slate-200">
        {% for client in queue %}
        <li class="{% if loop.index == 1 %}bg-brand-50 border-l-4 border-brand-500{% else %}hover:bg-slate-50 border-l-4 border-transparent{% endif %} transition-colors">
            <div class="px-4 py-4 sm:px-6">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            {% if loop.index == 1 %}
                                <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-brand-100 text-brand-800 font-bold text-sm ring-2 ring-brand-500 ring-offset-2">1</span>
                            {% else %}
                                <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-slate-100 text-slate-500 font-medium text-sm">{{ loop.index }}</span>
                            {% endif %}
                        </div>
                        <div class="ml-4 truncate">
                            <p class="text-sm font-medium text-brand-600 truncate">{{ client.name }}</p>
                            <p class="text-sm text-slate-500 truncate">ID: {{ client.id_card }}</p>
                        </div>
                    </div>
                    <div class="ml-2 flex-shrink-0 flex flex-col items-end">
                        <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                            {{ client.attention_type }}
                        </p>
                        <p class="mt-2 text-sm text-slate-500 flex items-center">
                            <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {{ client.appointment_date }} at {{ client.appointment_time }}
                        </p>
                    </div>
                </div>
            </div>
        </li>
        {% else %}
        <li>
            <div class="px-4 py-12 sm:px-6 text-center text-slate-500">
                <svg class="mx-auto h-12 w-12 text-slate-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                The queue is empty. No patients waiting.
            </div>
        </li>
        {% endfor %}
    </ul>
</div>
{% endblock %}'''
}

app.jinja_loader = DictLoader(template_dict)

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
