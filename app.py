from flask import Flask, render_template, request, make_response, redirect, url_for, session
from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-random-secret-key"


# -------------------------
# Database configuration
# -------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///martyrs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Martyr database model
# -------------------------

class Martyr(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Basic information
    name = db.Column(db.String(200), nullable=False)

    birthplace = db.Column(db.String(200))

    category = db.Column(db.String(100))

    birth_date = db.Column(db.String(50))

    death_date = db.Column(db.String(50))

    # Biography
    short_biography = db.Column(db.Text)

    biography = db.Column(db.Text)

    # Image
    image = db.Column(db.String(300))

    # Submission information
    submitted_by = db.Column(db.String(200))

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )
class DailyAssignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    visitor_id = db.Column(
        db.String(100),
        nullable=False
    )

    assigned_date = db.Column(
        db.String(20),
        nullable=False
    )

    martyr_id = db.Column(
        db.Integer,
        nullable=False
    )

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(300),
        nullable=False
    )

# -------------------------
# Admin Page
# -------------------------

@app.route("/create-admin")
def create_admin():

    existing_admin = Admin.query.first()

    if existing_admin:
        return "Admin account already exists!"

    password = "admin123"

    new_admin = Admin(
        username="admin",
        password_hash=generate_password_hash(password)
    )

    db.session.add(new_admin)
    db.session.commit()

    return "Admin account created successfully!"

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and check_password_hash(
            admin.password_hash,
            password
        ):

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pending_martyrs = Martyr.query.filter_by(
        status="pending"
    ).all()

    approved_martyrs = Martyr.query.filter_by(
        status="approved"
    ).all()

    return render_template(
        "admin_dashboard.html",
        pending_martyrs=pending_martyrs,
        approved_martyrs=approved_martyrs
    )

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))

@app.route("/admin/approve/<int:martyr_id>", methods=["POST"])
def approve_martyr(martyr_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    martyr = Martyr.query.get_or_404(martyr_id)

    martyr.status = "approved"

    db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/reject/<int:martyr_id>", methods=["POST"])
def reject_martyr(martyr_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    martyr = Martyr.query.get_or_404(martyr_id)

    martyr.status = "rejected"

    db.session.commit()

    return redirect(url_for("admin_dashboard"))


@app.route("/add-test")
def add_test():

    existing_martyr = Martyr.query.filter_by(
        name="Test Martyr"
    ).first()

    if existing_martyr:
        return "Test martyr already exists!"

    test_martyr = Martyr(
        name="Test Martyr",
        birthplace="Tehran, Iran",
        category="War Martyr",
        birth_date="1990",
        death_date="2020",
        short_biography="This is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsum",
        biography="This is a longer biography that we will replace with real information later.",
        image="test.jpg",
        status="approved"
    )

    db.session.add(test_martyr)
    db.session.commit()

    return "Test martyr added successfully!"

@app.route("/add-more-tests")
def add_more_tests():

    martyrs = [
        Martyr(
            name="Second Test Martyr",
            birthplace="Shiraz, Iran",
            category="Religious Martyr",
            birth_date="1985",
            death_date="2018",
            short_biography="A second test martyr.",
            biography="This is a test biography.",
            image="test2.jpg",
            status="approved"
        ),

        Martyr(
            name="Third Test Martyr",
            birthplace="Isfahan, Iran",
            category="Historical Martyr",
            birth_date="1978",
            death_date="2015",
            short_biography="A third test martyr.",
            biography="This is another test biography.",
            image="test3.jpg",
            status="approved"
        )
    ]

    for martyr in martyrs:
        existing = Martyr.query.filter_by(
            name=martyr.name
        ).first()

        if not existing:
            db.session.add(martyr)

    db.session.commit()
    

    return "More test martyrs added!"

@app.route("/add-4th-test")
def add_4th_test():

    existing_martyr = Martyr.query.filter_by(
        name="Test Martyr"
    ).first()

    if existing_martyr:
        return "Test martyr already exists!"

    test_martyr = Martyr(
        name="Test Martyr",
        birthplace="Tehran, Iran",
        category="War Martyr",
        birth_date="1990",
        death_date="2020",
        short_biography="This is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsumThis is a test martyr for our website. lorem epsum",
        biography="This is a longer biography that we will replace with real information later.",
        image="test.jpg",
    )

    db.session.add(test_martyr)
    db.session.commit()

    return "Test martyr added successfully!"
# -------------------------
# Home page
# -------------------------

@app.route("/")
def home():
    is_existing_assignment = False
    visitor_id = request.cookies.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    today = str(date.today())

    assignment = DailyAssignment.query.filter_by(
        visitor_id=visitor_id,
        assigned_date=today
    ).first()

    if assignment:

     martyr = Martyr.query.get(assignment.martyr_id)
     is_existing_assignment = True

    else:

        martyr = Martyr.query.filter_by(
            status="approved"
        ).order_by(func.random()).first()

        if martyr:

            assignment = DailyAssignment(
                visitor_id=visitor_id,
                assigned_date=today,
                martyr_id=martyr.id
            )

            db.session.add(assignment)
            db.session.commit()

    response = make_response(
    render_template(
        "index.html",
        martyr=martyr,
        is_existing_assignment=is_existing_assignment
    )
)

    response.set_cookie(
        "visitor_id",
        visitor_id,
        max_age=60 * 60 * 24 * 365
    )

    return response


# -------------------------
# Create database
# -------------------------

with app.app_context():
    db.create_all()


# -------------------------
# submit page
# -------------------------
@app.route("/submit")
def submit_page():
    return render_template("submit.html")

@app.route("/submit-martyr", methods=["POST"])
def submit_martyr():

    new_martyr = Martyr(
        name=request.form["name"],
        birthplace=request.form["birthplace"],
        category=request.form["category"],
        birth_date=request.form["birth_date"],
        death_date=request.form["death_date"],
        short_biography=request.form["short_biography"],
        biography=request.form["biography"],
        submitted_by=request.form["submitted_by"],
        status="pending"
    )

    db.session.add(new_martyr)
    db.session.commit()

    return """
        <h1>Thank you!</h1>
        <p>Your submission has been sent for review.</p>
        <a href="/">Return to homepage</a>
    """
# -------------------------
# Start Flask
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
