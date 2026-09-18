from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

    name = db.Column(db.String(200), nullable=False)

    birthplace = db.Column(db.String(200))

    category = db.Column(db.String(100))

    birth_date = db.Column(db.String(50))

    death_date = db.Column(db.String(50))

    short_biography = db.Column(db.Text)

    biography = db.Column(db.Text)

    image = db.Column(db.String(300))


# -------------------------
# Home page
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# Create database
# -------------------------

with app.app_context():
    db.create_all()


# -------------------------
# Start Flask
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
