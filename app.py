from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)

# Temporary database using a dictionary
users_db = {}  # Format: { "email": {"name": "User", "password": "hashed_password"} }

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if email in users_db:
            return "Email already exists."

        users_db[email] = {"name": name, "password": password}
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_db.get(email)
        if user and bcrypt.check_password_hash(user["password"], password):
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=users_db[session['user_email']]['name'])

# Career paths with corresponding HTML page names
career_pages = {
    "ai engineer": "ai.html",
    "teacher": "teacher.html",
    "pilot": "pilot.html",
    "doctor": "doctor.html",
    "scientist": "scientist.html",
    "ias officer": "ias.html"
}

@app.route('/career_counsel', methods=['GET', 'POST'])
def career_counsel():
    if request.method == 'POST':  # Ensure it processes the form submission
        career = request.form.get('career', '').strip().lower()  # Get career input

        if career in career_pages:
            return redirect(url_for('career_page', career_name=career))  # Redirect to correct career page
        else:
            return render_template('error.html', message="Career path not found!")

    return render_template('career_counsel.html')  # Load the form initially


# Dynamic route for career pages
@app.route('/career/<career_name>')
def career_page(career_name):
    if career_name in career_pages:
        return render_template(career_pages[career_name])
    else:
        return render_template('error.html', message="Career page not available.")

# Career Path Page
@app.route('/career_path')
def career_path():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('career_path.html')
@app.route('/course_recommendations', methods=['GET', 'POST'])
def course_recommendations():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    preference = request.form.get('preference', '').strip() if request.method == 'POST' else ''
    return render_template('course_recommendations.html', preference=preference)

@app.route('/job_market_trends', methods=['GET', 'POST'])
def job_market_trends():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    career = request.form.get('career', '').strip() if request.method == 'POST' else ''
    return render_template('job_market_trends.html', career=career)

@app.route('/career_exploration')
def career_exploration():
    return render_template('career_exploration.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)