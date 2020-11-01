import pusher
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'

pusher_client = pusher.Pusher(
  app_id='1097594',
  key='93c0c9a1854f98ead643',
  secret='9cceedbc3db379f3e8af',
  cluster='eu',
  ssl=True
)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():

    username = request.form.get('username')
    message = request.form.get('message')

    new_message = Message(username=username, message=message)
    db.session.add(new_message)
    db.session.commit()

    pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})


    return ''

if __name__ == '__main__':
    app.run(debug=True)

