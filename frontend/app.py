from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_BASE_URL = "http://backend:8000"

def get_categories():
    categories_response = requests.get(f'{API_BASE_URL}/api/v1/accommodations/categories/all')

    try:
        categories = categories_response.json()
    except:
        categories = []
    return categories

# Function to get accommodations by category
def get_accommodations_by_category(category):
    response = requests.get(f'{API_BASE_URL}/api/v1/accommodations/category/{category}')
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
# Route to home page
@app.route('/')
def home():
    page = 'home'
    
    category = request.args.get('category', default=None)

    try:
        if category:
            accommodations = get_accommodations_by_category(category)
        else:
            response = requests.get(f'{API_BASE_URL}/api/v1/accommodations')
            accommodations = response.json()
    except:
        accommodations = []

    categories = get_categories()

    return render_template('home.html', page=page, accommodations=accommodations, categories=categories)

# Route to display the insert data entry form
@app.route('/add-new-place', methods=['GET'])
def add_new_place_page():
    page = 'add'
    categories = get_categories()
    return render_template('add-page.html', page=page, categories=categories)

# Route to send the registration form data to the API
@app.route('/insert', methods=['POST'])
def add_new_place():
    category = request.form['category']
    city = request.form['city']
    address = request.form['address']
    price_per_night = request.form['price_per_night']
    owner = request.form['owner']

    payload = {
        'category': category,
        'city': city,
        'address': address, 
        'price_per_night': price_per_night,  
        'owner': owner,  
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/accommodations', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('home'))
    else:
        return "Erro ao adicionar nova locação.", 500

# Route to display the accommodation edit form
@app.route('/update/<int:accommodation_id>', methods=['GET'])
def update_accommodation_form(accommodation_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/accommodations/{accommodation_id}")
    
    if response.status_code == 200:
        return render_template('edit-page.html', accommodation=response.json())
    
    return "Acomodação não encontrada", 404

# Route to send the accommodation edit form data to the API
@app.route('/update/<int:accommodation_id>', methods=['POST'])
def update_accommodation(accommodation_id):
    category = request.form['category']
    city = request.form['city']
    address = request.form['address']
    price_per_night = request.form['price_per_night']
    owner = request.form['owner']

    payload = {
        'category': category,
        'city': city,  
        'address': address,  
        'price_per_night': price_per_night, 
        'owner': owner 
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/accommodations/{accommodation_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('home'))
    else:
        return "Erro ao atualizar a locação", 500
    
# Route to delete accommodation
@app.route('/delete/<int:accommodation_id>', methods=['POST'])
def delete_accommodation(accommodation_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/accommodations/{accommodation_id}")
    
    if response.status_code == 200:
        return redirect(url_for('home'))
    else:
        return "Erro ao excluir acomodação", 500

#Route to reset the accommodation database
@app.route('/accommodation/reset-database', methods=['GET'])
def reset_database_accommodation():
    response = requests.delete(f"{API_BASE_URL}/api/v1/accommodations")
    
    if response.status_code == 200:
        return redirect(url_for('home')) 
    else:
        return "Erro ao resetar o database", 500
    
# ----------------- Booking -----------------

#Route to diplay bookings
@app.route('/booking')
def booking_page():
    page = 'booking'
    response = requests.get(f'{API_BASE_URL}/api/v1/bookings')

    try:
        bookings = response.json()
    except:
        bookings = []

    return render_template('booking-page.html', page=page, bookings=bookings)

# Route to display the reservation data entry form
@app.route('/book-accommodation/<int:accommodation_id>', methods=['GET'])
def book_accommodation(accommodation_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/accommodations/{accommodation_id}")
    
    if response.status_code == 200:
        return render_template('book-accommodation.html', accommodation=response.json())
    
    return "Acomodação não encontrada", 404

# Route to send the booking form data to the API
@app.route('/booking/insert', methods=['POST'])
def insert_booking():
    accommodation_id = request.form['accommodation_id']
    city = request.form['city']
    name = request.form['name']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    checkin_time = request.form['checkin_time']  # Recebe apenas a hora (HH:MM)
    checkout_time = request.form['checkout_time']  # Recebe apenas a hora (HH:MM)

    checkin = datetime.fromisoformat(f"{checkin}T{checkin_time}")
    checkout = datetime.fromisoformat(f"{checkout}T{checkout_time}")

    payload = {
        'accommodation_id': accommodation_id,
        'city': city,
        'name': name,
        'checkin': checkin.isoformat(), 
        'checkout': checkout.isoformat()
    }

    response = requests.post(f"{API_BASE_URL}/api/v1/bookings", json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('booking_page'))  # Redireciona para a página principal
    elif response.status_code == 400:
        response = requests.get(f"{API_BASE_URL}/api/v1/accommodations/{accommodation_id}")
        # Caso o código de resposta seja 400, retorna uma mensagem com o erro
        error_message = response.json().get('error', 'A data escolhida não está disponível. Por favor inserir nova data.')
        return render_template('book-accommodation.html', error_message=error_message, accommodation=response.json())
    else:
        return "Erro ao realizar reserva", 500
    
# Route to display the booking edit form
@app.route('/booking/update/<int:booking_id>', methods=['GET'])
def update_booking_form(booking_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/bookings/{booking_id}")

    if response.status_code == 200:
        return render_template('edit-booking-page.html', booking=response.json())
    return "Reserva não encontrada", 404

# Route to send the booking edit form data to the API
@app.route('/booking/update/<int:booking_id>', methods=['POST'])
def update_booking(booking_id):
    name = request.form['name']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    checkin_time = request.form['checkin_time']  # Receives only the time (HH:MM)
    checkout_time = request.form['checkout_time']  # Receives only the time (HH:MM)

    # Merge date and time
    checkin = datetime.fromisoformat(f"{checkin}T{checkin_time}")
    checkout = datetime.fromisoformat(f"{checkout}T{checkout_time}")

    payload = {
        'name': name,
        'checkin': checkin.isoformat(), 
        'checkout': checkout.isoformat()
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/bookings/{booking_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('booking_page')) 
    else:
        return "Erro ao atualizar a locação", 500
    

# Route to delete booking
@app.route('/booking/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/bookings/{booking_id}")
    
    if response.status_code == 200:
        return redirect(url_for('booking_page'))
    else:
        return "Erro ao excluir reserva", 500
   
#Route to reset the booking database
@app.route('/booking/reset-database', methods=['GET'])
def reset_database_booking():
    response = requests.delete(f"{API_BASE_URL}/api/v1/bookings")
    
    if response.status_code == 200:
        return redirect(url_for('booking_page')) 
    else:
        return "Erro ao resetar o banco de dados", 500
    
    
if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')