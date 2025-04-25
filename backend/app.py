from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bdd-green'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définir les modèles SQLAlchemy
class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

class Admin(db.Model):
    __tablename__ = 'admins'
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True)
    user = db.relationship('User', backref=db.backref('admin', lazy=True))

class Quizz(db.Model):
    __tablename__ = 'quizz'
    id_quizz = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum('IT For Green', 'GreenIT'), nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id_question = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quizz_id = db.Column(db.Integer, db.ForeignKey('quizz.id_quizz'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer1 = db.Column(db.String(255), nullable=False)
    answer2 = db.Column(db.String(255), nullable=False)
    correct_answer_is_1 = db.Column(db.Boolean, nullable=False)
    quizz = db.relationship('Quizz', backref=db.backref('questions', lazy=True))

# Routes de base
@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/auth')
def authentification():
    return render_template('authentification.html')

@app.route('/jeu')
def jeu():
    return render_template('jeu.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/quizz')
def quizz():
    return render_template('quizz.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quizz.query.all()
    return jsonify([{'id': quiz.id_quizz, 'name': quiz.name, 'category': quiz.category} for quiz in quizzes])

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

if __name__ == '__main__':
    app.run(debug=True)
