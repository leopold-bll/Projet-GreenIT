from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from hashlib import sha256

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bdd-green'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#config pour login
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
#sess.init_app(app)
db = SQLAlchemy(app)


#config flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Définir les modèles SQLAlchemy
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return str(self.id_user)

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

@app.route('/jeu/<int:quizz_id>', methods=['GET', 'POST'])
@login_required
def jeu(quizz_id):
        # on récupère le quiz ou 404
    quizz = Quizz.query.get_or_404(quizz_id)

    if request.method == 'POST':
        # (…votre logique de scoring…)
        total = len(quizz.questions)
        correct = 0
        for q in quizz.questions:
            choix = request.form.get(f"q{q.id_question}")
            if (choix == '1' and q.correct_answer_is_1) or (choix == '2' and not q.correct_answer_is_1):
                correct += 1
        current_user.score += correct
        db.session.commit()
        # on renvoie le même template mais avec score et total
        return render_template('jeu.html', quizz=quizz, score=correct, total=total)

    # GET : on envoie juste le quiz pour affichage
    return render_template('jeu.html', quizz=quizz)

@app.route('/profile')
@login_required
def profile():
    # current_user est déjà l'utilisateur connecté grâce à Flask-Login
    return render_template('profile.html', user=current_user)


@app.route('/quizz')
def quizz():
    quizzes = Quizz.query.all()
    print("DEBUG – quizzes en base :", quizzes)
    return render_template('quizz.html', quizzes=quizzes)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quizz.query.all()
    return jsonify([{'id': quiz.id_quizz, 'name': quiz.name, 'category': quiz.category} for quiz in quizzes])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logique de connexion
        username = request.form['username']
        password = request.form['password']
        passwordH = (sha256(password.encode("utf-8"))).hexdigest()
        user = User.query.filter_by(username=username).first()
        if user and user.password == passwordH:
            login_user(user)
            return redirect(url_for('accueil'))
        else:
            flash('Identifiants invalides.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifiez si le nom d'utilisateur ou l'email existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Cette adresse e-mail est déjà utilisée.')
            return render_template('register.html')

        # Hacher le mot de passe
        hashed_password = (sha256(password.encode("utf-8"))).hexdigest()
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/classement', methods=['GET'])
def classement():
    users = User.query.order_by(User.score.desc()).all()
    return render_template('classement.html', users=users)

#pour l'ADMIN DASHBOARD
@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    # Vérifiez si l'utilisateur actuel est un admin
    if not current_user.admin:
        flash('Accès non autorisé.')
        return redirect(url_for('accueil'))

    users = User.query.all()
    return render_template('dashboard-admin.html', users=users)

@app.route('/admin/create-user', methods=['POST'])
@login_required
def create_user():
    if not current_user.admin:
        flash('Accès non autorisé.')
        return redirect(url_for('accueil'))

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash('Nom d\'utilisateur ou email déjà utilisé.')
        return redirect(url_for('admin_dashboard'))

    hashed_password = (sha256(password.encode("utf-8"))).hexdigest()
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Utilisateur créé avec succès.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update-user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.admin:
        flash('Accès non autorisé.')
        return redirect(url_for('accueil'))

    user = User.query.get_or_404(user_id)
    user.username = request.form['username']
    user.email = request.form['email']
    if request.form['password']:
        user.password = (sha256(request.form['password'].encode("utf-8"))).hexdigest()
    db.session.commit()
    flash('Utilisateur mis à jour avec succès.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.admin:
        flash('Accès non autorisé.')
        return redirect(url_for('accueil'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès.')
    return redirect(url_for('admin_dashboard'))




if __name__ == '__main__':
    app.run(debug=True)