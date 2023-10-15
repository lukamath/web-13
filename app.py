from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
            # Parse the date and time string into a datetime object
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            error_message = "Invalid date and time format."
            return render_template('index.html', error_message=error_message)

        if num_words > 10 or num_chars > 100:
            error_message = "You've reached the limit of 10 words or 100 characters."
        else:
            new_message = Message(user=username, message=message_text, num_words=num_words, num_chars=num_chars, date_time=date_time)
            db.session.add(new_message)
            db.session.commit()

    return render_template('index.html', error_message=error_message)

#

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
