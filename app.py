from flask import Flask, render_template, request, redirect, url_for,session
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = 'bubblecat'
# Step 2: Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bubblecatog@gmail.com'         # <--- Replace this
app.config['MAIL_PASSWORD'] = 'tksi yftp omms ptpf'       # <--- Replace this with App Password
app.config['MAIL_DEFAULT_SENDER'] = 'bubblecatog@gmail.com'   # <--- Replace this

mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/second')
def second_page():
    return render_template('second.html')

@app.route('/food')
def food_page():
    return render_template('food.html')

@app.route('/roam')
def roam_page():
    return render_template('roam.html')

@app.route('/activities')
def activities_page():
    return render_template('activities.html')

@app.route('/schedule', methods=['GET', 'POST'])
def date_schedule():
    # Get the user's choice (food, activity, or roam)
    user_choice = session.get('food_choice', None) or session.get('activity_choice', None) or session.get('roam_choice', None)

    if request.method == 'POST':
        email = request.form['email']
        date = request.form['date']

        # Send email
        msg = Message("Date Scheduled 🎉", recipients=[email])
        msg.body = f"Hey! Your choice is {user_choice}. Your date has been scheduled for {date}. See you there!"
        mail.send(msg)

        return render_template('confirmation.html', email=email, date=date, user_choice=user_choice)
    
    return render_template('date_schedule.html', user_choice=user_choice)





@app.route('/select_activity', methods=['POST'])
def select_activity():
    session.pop('food_choice', None)  # Clear the previous food choice
    session.pop('roam_choice', None)  # Clear the previous roam choice
    activity_choice = request.form['activity_choice']
    session['activity_choice'] = activity_choice  # Store selected activity option in session
    return redirect(url_for('date_schedule'))  # Redirect to date scheduling page


@app.route('/select_food', methods=['POST'])
def select_food():
    session.pop('activity_choice', None)  # Clear the previous activity choice
    session.pop('roam_choice', None)  # Clear the previous roam choice
    food_choice = request.form['food_choice']
    session['food_choice'] = food_choice  # Store selected food option in session
    return redirect(url_for('date_schedule'))


@app.route('/select_roam', methods=['POST'])
def select_roam():
    session.pop('food_choice', None)  # Clear the previous food choice
    session.pop('activity_choice', None)  # Clear the previous activity choice
    roam_choice = request.form['roam_choice']
    session['roam_choice'] = roam_choice  # Store selected roam option in session
    return redirect(url_for('date_schedule'))  # Redirect to date scheduling page



if __name__ == '__main__':
    app.run(debug=True)
