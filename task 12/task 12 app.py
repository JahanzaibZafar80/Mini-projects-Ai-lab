from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'secret_key123'

# Load model
model_rf = pickle.load(open('rf_model.pkl', 'rb'))

# Temporary in-memory user store
users = {}  # format: {'username': 'password'}

# ---------- GALLERY PAGE ----------
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# ---------- PREDICTION FORM PAGE ----------
@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

# ---------- PREDICT RESULT ----------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(request.form['carat']),
                float(request.form['cut']),
                float(request.form['color']),
                float(request.form['clarity']),
                float(request.form['depth']),
                float(request.form['table'])]
        final_input = np.array(data).reshape(1, -1)
        prediction = model_rf.predict(final_input)[0]
        prediction = round(prediction, 2)
        return render_template('result.html', price=prediction)
    except Exception as e:
        return render_template('result.html', price=f"Error: {str(e)}")

# ---------- LOGIN ROUTE ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('gallery'))
        else:
            error = "Password invalid or user not found!"
    return render_template('login.html', error=error)

# ---------- SIGNUP ROUTE ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists!")
            return redirect(url_for('signup'))
        users[username] = password
        flash("Account created successfully! Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

# ---------- FORGOT PASSWORD ROUTE ----------
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            message = f"Your password is: {users[username]}"
        else:
            message = "Username not found!"
    return render_template('forgot_password.html', message=message)

# ---------- HOME REDIRECT ----------
@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
