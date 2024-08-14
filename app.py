from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Rule
from sqlalchemy import desc
from rule_engine import create_rule, combine_rules, evaluate_rule
import logging
import os

app = Flask(__name__, static_folder=os.path.abspath('static'))
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_dummy_users():
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            user1 = User(username='dummy1')
            user1.set_password('password1')
            user2 = User(username='dummy2')
            user2.set_password('password2')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            print("Dummy users created successfully.")

create_dummy_users()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    leaderboard = User.query.order_by(desc(User.wins)).limit(10).all()
    rules = Rule.query.all()
    return render_template('index.html', leaderboard=leaderboard, rules=rules)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        profile_icon = request.form.get('profile_icon')
        current_user.profile_icon = profile_icon
        db.session.commit()
        flash('Profile updated successfully.', 'success')
    return render_template('profile.html', user=current_user)

@app.route('/create_rule', methods=['POST'])
def create_rule_route():
    try:
        data = request.json
        rule_name = data['name']
        rule_string = data['rule']

        # Create the rule AST
        rule_ast = create_rule(rule_string)

        # Save the rule to the database
        new_rule = Rule(name=rule_name, rule_string=rule_string)
        db.session.add(new_rule)
        db.session.commit()

        return jsonify({'message': 'Rule created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_route():
    try:
        data = request.json
        rule_id = data['rule_id']
        user_data = data['user_data']

        rule = Rule.query.get(rule_id)
        if not rule:
            return jsonify({'error': 'Rule not found'}), 404

        rule_ast = create_rule(rule.rule_string)
        result = evaluate_rule(rule_ast, user_data)

        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_route():
    try:
        data = request.json
        rule_ids = data['rule_ids']

        rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
        rule_strings = [rule.rule_string for rule in rules]

        combined_ast = combine_rules(rule_strings)

        # For simplicity, we're returning the string representation of the combined AST
        # In a real application, you might want to save this combined rule or process it further
        return jsonify({'combined_rule': str(combined_ast)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
