from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta  # Import timedelta

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
    date_time = db.Column(db.DateTime)  # Change the column type to DateTime

@app.route('/', methods=['GET', 'POST'])
def kaz13():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username')
        message_text = request.form.get('input_text')
        date_time_str = request.form.get('date_time')  # Get the date and time string

        words = message_text.split()
        num_words = len(words)
        num_chars = len(message_text)

        try:
            date_time_str = date_time_str + ':00'
            # Parse the date and time string into a datetime object
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            error_message = "Invalid date and time format."
            return render_template('index.html', error_message=error_message)

        if num_words > 10 or num_chars > 100:
            error_message = "You've reached the limit of 10 words or 100 characters."
        else:
            new_message = Message(user=username, message=message_text, num_words=num_words, num_chars=num_chars, date_time=date_time)
            start_time = int(date_time.timestamp())  
            db.session.add(new_message)
            db.session.commit()
            #return render_template('countdown.html', start_time=start_time)  #this do not show the parameter, maybe to consider for something
            return redirect(url_for('countdown', start_time=start_time))

    return render_template('index.html', error_message=error_message)



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

@app.route('/w13')  #to dipaly messages in real time 
def w13():
    return render_template('w13.html')

@app.route('/get_message', methods=['GET']) #   <-- w13.html
def get_message():
    current_time = datetime.now()
    print("Current Time:", current_time)
    # Query your database for the message where the time slot is within the next 10 minutes
    # Replace 'your_query' with the appropriate query to find the message
    message = db.session.query(Message).filter(Message.date_time > current_time -timedelta(minutes=10), Message.date_time <= current_time).first()
    if message:
        message_data = {
            'user': message.user,
            'message': message.message
        }
        print("Slot Time:", message.date_time)  # You can safely print message.date_time here
        return jsonify(message_data)
    else:
        return jsonify({'message': 'No message available for the next 10 minutes'})

@app.route('/countdown/<int:start_time>')
def countdown(start_time):
    #start_time = int(date_time.timestamp())
    return render_template('countdown.html', start_time=start_time)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
