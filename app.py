from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

from models import db, User

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret_key_12345"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///users.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return redirect(url_for("signup"))


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already exists."

        # Generate Registration ID
        last_user = User.query.order_by(User.id.desc()).first()

        if last_user:
            registration_id = f"REG{last_user.id + 1001}"
        else:
            registration_id = "REG1001"

        new_user = User(
            email=email,
            password=password,
            registration_id=registration_id,
            status="Pending",
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("profile", user_id=new_user.id))

    return render_template("signup.html")


@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        user.full_name = request.form["fullname"]

        user.phone = request.form["phone"]

        user.address = request.form["address"]

        user.spouse = request.form["spouse"]

        user.next_of_kin = request.form["nextofkin"]

        user.bank_account = request.form["bankaccount"]

        user.place_of_retirement = request.form["placeofretirement"]

        db.session.commit()

        print("Profile saved!")
        print(user.full_name)
        print(user.phone)
        print(user.address)
        print(user.bank_account)
        print(user.place_of_retirement)

        return redirect(url_for("thanks"))

    return render_template("profile.html")


@app.route("/thanks")
def thanks():

    return render_template("thanks.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user is None:
            return "Email not found."

        if user.password != password:
            return "Incorrect password."

        return redirect(url_for("dashboard", user_id=user.id))

    return render_template("login.html")

@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):

    user = User.query.get_or_404(user_id)

    applicants = User.query.order_by(User.registration_id).all()

    return render_template(
        "dashboard.html",
        user=user,
        applicants=applicants
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
