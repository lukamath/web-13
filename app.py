from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message_app0.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    num_words = db.Column(db.Integer)
    num_chars = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unixtime = db.Column(db.Integer, unique=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

@app.route('/', methods=['GET', 'POST'])
def kaz13():
	error_message = None
    # Query the database for busy slots
	busy_slots = []
	
	if request.method == 'POST':
		username = request.form.get('username')
		message_text = request.form.get('input_text')
		date_time_str = request.form.get('date_time')
		words = message_text.split()
		num_words = len(words)
		num_chars = len(message_text)

		start_time = None  # Define start_time here

		try:
			date_time_str = date_time_str + ':00'
			date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
		except ValueError:
			error_message = "Invalid date and time format."
			return render_template('index.html', error_message=error_message, busy_slots=busy_slots)

		if num_words > 10 or num_chars > 100:
			error_message = "You've reached the limit of 10 words or 100 characters."
		else:
			# Check if a slot with the same unixtime already exists
			existing_slot = Slot.query.filter_by(unixtime=start_time).first()
			if existing_slot:
				error_message = "The selected time slot is already taken."
			else:
				new_message = Message(user=username, message=message_text, num_words=num_words, num_chars=num_chars, date_time=date_time)
				db.session.add(new_message)
				db.session.commit()

				start_time = date_time.timestamp()  # Define start_time here

				# Create a new slot for the selected time
				new_slot = Slot(unixtime=start_time, message_id=new_message.id)
				db.session.add(new_slot)
				db.session.commit()

				return redirect(url_for('countdown', start_time=start_time))
		
	# Get the busy slots from the database
	busy_slots = Slot.query.all()

	return render_template('index.html', error_message=error_message, busy_slots=busy_slots)

@app.route('/api/messages/<username>', methods=['GET'])
def get_messages(username):
    user_messages = Message.query.filter_by(user=username).all()
    messages = [{'user': message.user, 'message': message.message, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'date_time': message.date_time} for message in user_messages]
    return jsonify(messages)

@app.route('/api/messages/all', methods=['GET'])
def get_all_messages():
    all_messages = Message.query.all()
    messages = [{'user': message.user, 'message': message.message, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'date_time': message.date_time} for message in all_messages]
    return jsonify(messages)

@app.route('/messages')
def display_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', messages=messages)

@app.route('/w13')
def w13():
    return render_template('w13.html')

@app.route('/get_message', methods=['GET'])
def get_message():
    current_time = datetime.now()
    print("Current Time:", current_time)
    message = db.session.query(Message).filter(Message.date_time > current_time - timedelta(minutes=10), Message.date_time <= current_time).first()
    if message:
        message_data = {
            'user': message.user,
            'message': message.message
        }
        print("Slot Time:", message.date_time)
        return jsonify(message_data)
    else:
        return jsonify({'message': 'No message available for the next 10 minutes'})

@app.route('/countdown/<int:start_time>')
def countdown(start_time):
    # Calculate the remaining time
    current_time = int(datetime.now().timestamp())
    remaining_time = start_time - current_time

    # Check if the countdown has expired
    if remaining_time <= 0:
        return redirect(url_for('w13'))

    return render_template('countdown.html', start_time=start_time)

@app.route('/api/taken_slots', methods=['GET'])
def get_taken_slots():
    taken_slots = Slot.query.all()
    return jsonify([{"unixtime": slot.unixtime} for slot in taken_slots])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)