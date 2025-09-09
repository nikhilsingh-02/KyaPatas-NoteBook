from enum import unique
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.sql import expression
# from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos_db"
# Corrected typo from MODIOFICATIONS to MODIFICATIONS
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "supersecret"
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # Increased password length to accommodate the hash
    password = db.Column(db.String(60), nullable=False)
    todos = db.relationship('Todo', lazy=True, backref='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __str__(self):
        return f"<Todo:{self.id} ({self.title})>"

    def __repr__(self):
        return f"<Todo:{self.id} ({self.title})>"

    @classmethod
    def search(cls, user_id, query):
        return Todo.query.filter(Todo.user_id == user_id).filter(
            func.lower(Todo.title).contains(query.lower()) |
            func.lower(Todo.description).contains(query.lower())
        ).all()


@app.route("/")
@app.route("/home")
@login_required
def index():
    todos = current_user.todos
    return render_template("index.html", todos=todos)


@app.route("/uncompleted")
@login_required
def uncompleted():
    todos = Todo.query.filter_by(user_id=current_user.id, is_done=False).all()
    return render_template("index.html", todos=todos)


@app.route("/completed")
@login_required
def completed():
    todos = Todo.query.filter_by(user_id=current_user.id, is_done=True).all()
    return render_template("index.html", todos=todos)


@app.route("/todo/<int:id>/toggle", methods=["POST"])
@login_required
def toggle_status(id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=id).first()
    if not todo:
        return render_template("not_found.html")
    # Simplified toggle logic
    todo.is_done = not todo.is_done
    db.session.commit()
    # Redirect instead of render_template after a POST request
    return redirect(url_for('index'))


@app.route("/todo", methods=["GET", "POST"])
@login_required
def create_todo():
    if request.method == "POST":
        todo = Todo(title=request.form.get("title"),
                    description=request.form.get("description"),
                    is_done=True if request.form.get("is_done") == "on" else False,
                    user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("todo_form.html")


@app.route("/todo/<int:id>", methods=["GET"])
@login_required
def get_todo(id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=id).first()
    if not todo:
        return render_template("not_found.html")
    return render_template("todo.html", todo=todo)


@app.route("/todo/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_todo(id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=id).first()
    if not todo:
        return render_template("not_found.html")
    if request.method == 'POST':
        todo.title = request.form.get("title")
        todo.description = request.form.get("description")
        todo.is_done = True if request.form.get("is_done") == "on" else False
        db.session.commit()
        return redirect(url_for("get_todo", id=id))
    return render_template("todo_form.html", todo=todo)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if not user or not user.check_password(request.form.get("password")):
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        if request.form.get('password') != request.form.get('confirm_password'):
            return redirect(url_for('register'))

        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == request.form.get('email')) |
            (User.username == request.form.get('username'))
        ).first()

        if existing_user:
            # Add a flash message here in the future for better UX
            print("User with this email or username already exists.")
            return redirect(url_for('register'))

        user = User(
            email=request.form.get('email'),
            username=request.form.get('username'),
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("register.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/todo/<int:id>/delete', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.filter_by(user_id=current_user.id, id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)