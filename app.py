from flask import Flask, render_template, jsonify
from helper import Helper

app = Flask(__name__)
helper = Helper()
helper.firebase_auth()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/messages')
def get_messages():
    messages = Helper.get_all_messages()
    return jsonify(messages)


if __name__ == '__main__':
    app.run()
