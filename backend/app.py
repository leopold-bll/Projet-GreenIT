import os
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)

# -----------------------------------------------------------------------------
# App Configuration
# -----------------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

# Database URI: use Render’s DATABASE_URL in prod, fallback to local MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://bddgreen_user:PmwuIWbI2ixkkuILLbHPKyeH7PRZpVGv@dpg-d07850ali9vc73f2g510-a/bddgreen'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key from env (Render) or dev fallback
app.secret_key = os.environ.get('SECRET_KEY', 'super secret key')

# -----------------------------------------------------------------------------
# Extensions Initialization
# -----------------------------------------------------------------------------
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id_user  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50),  unique=True, nullable=False)
    email    = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score    = db.Column(db.Integer, nullable=False, default=0)

    @property
    def is_admin(self):
        return bool(self.admin)

    def get_id(self):
        return str(self.id_user)

class Admin(db.Model):
    __tablename__ = 'admins'
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True)
    user    = db.relationship('User', backref=db.backref('admin', lazy=True))

class Quizz(db.Model):
    __tablename__ = 'quizz'
    id_quizz = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name     = db.Column(db.String(100), nullable=False)
    # Named enum for PostgreSQL compatibility
    category = db.Column(
        db.Enum('IT For Green', 'GreenIT', name='quiz_category_enum'),
        nullable=False
    )

class Question(db.Model):
    __tablename__ = 'question'
    id_question         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quizz_id            = db.Column(db.Integer, db.ForeignKey('quizz.id_quizz'), nullable=False)
    question            = db.Column(db.Text,    nullable=False)
    answer1             = db.Column(db.String(255), nullable=False)
    answer2             = db.Column(db.String(255), nullable=False)
    correct_answer_is_1 = db.Column(db.Boolean, nullable=False)
    quizz               = db.relationship('Quizz', backref=db.backref('questions', lazy=True))

# -----------------------------------------------------------------------------
# Ensure tables exist at startup
# -----------------------------------------------------------------------------
with app.app_context():
    db.create_all()

# -----------------------------------------------------------------------------
# Flask-Login user loader
# -----------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd      = request.form['password']
        user     = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, pwd):
            login_user(user)
            return redirect(request.args.get('next') or url_for('accueil'))
        flash('Identifiants invalides.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        pwd      = request.form['password']
        # Unique checks
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Nom d’utilisateur ou email déjà utilisé.', 'error')
            return render_template('register.html')
        hashed = generate_password_hash(pwd, method='sha256')
        db.session.add(User(username=username, email=email, password=hashed))
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil'))

@app.route('/quizz')
@login_required
def quizz():
    quizzes = Quizz.query.all()
    return render_template('quizz.html', quizzes=quizzes)

@app.route('/jeu/<int:quizz_id>', methods=['GET', 'POST'])
@login_required
def jeu(quizz_id):
    quizz = Quizz.query.get_or_404(quizz_id)
    if request.method == 'POST':
        total   = len(quizz.questions)
        correct = 0
        for q in quizz.questions:
            choix = request.form.get(f"q{q.id_question}")
            if (choix == '1' and q.correct_answer_is_1) or (choix == '2' and not q.correct_answer_is_1):
                correct += 1
        current_user.score += correct
        db.session.commit()
        return render_template('jeu.html', quizz=quizz, score=correct, total=total)
    return render_template('jeu.html', quizz=quizz)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email    = request.form['email']
        new_pwd = request.form.get('password')
        if new_pwd:
            current_user.password = generate_password_hash(new_pwd, method='sha256')
        db.session.commit()
        flash('Profil mis à jour !', 'success')
        return redirect(url_for('profile'))
    users = current_user.is_admin and User.query.all() or []
    return render_template('profile.html', user=current_user, users=users)

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('accueil'))
    users = User.query.all()
    return render_template('dashboard-admin.html', users=users)

@app.route('/admin/create-user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('admin_dashboard'))
    username = request.form['username']
    email    = request.form['email']
    pwd      = request.form['password']
    if User.query.filter((User.username==username)|(User.email==email)).first():
        flash('Nom d’utilisateur ou email déjà utilisé.', 'error')
        return redirect(url_for('admin_dashboard'))
    hashed = generate_password_hash(pwd, method='sha256')
    db.session.add(User(username=username, email=email, password=hashed))
    db.session.commit()
    flash('Utilisateur créé.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update-user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('admin_dashboard'))
    user = User.query.get_or_404(user_id)
    user.username = request.form['username']
    user.email    = request.form['email']
    new_pwd       = request.form.get('password')
    if new_pwd:
        user.password = generate_password_hash(new_pwd, method='sha256')
    db.session.commit()
    flash('Utilisateur mis à jour.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('admin_dashboard'))
    user = User.query.get_or_404(user_id)
    if user.id_user == current_user.id_user:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/classement')
def classement():
    users = User.query.order_by(User.score.desc()).all()
    return render_template('classement.html', users=users)

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
