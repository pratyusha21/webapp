from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skills.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    skills = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    skills = request.form['skills']
    new_user = User(name=name, skills=skills)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/users')
def users():
    all_users = User.query.all()
    users = []
    for user in all_users:
        users.append({'name': user.name, 'skills': user.skills})
    return jsonify(users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensuring this is within the app context
    app.run(debug=True, use_reloader=False)



