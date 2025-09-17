import os
import json
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "your-secret-key"  # change this later

# ---------------- EMAIL CONFIG ----------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "izedinnursefa235@gmail.com"   # your Gmail
app.config["MAIL_PASSWORD"] = "cqjqwbvhdurcizqj"             # your 16-char app password
app.config["MAIL_DEFAULT_SENDER"] = "izedinnursefa235@gmail.com"

mail = Mail(app)

# ---------------- BOOKINGS FILE ----------------
BOOKINGS_FILE = "bookings.json"

if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, "w") as f:
        json.dump([], f)


def load_bookings():
    with open(BOOKINGS_FILE, "r") as f:
        return json.load(f)


def save_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=4)


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    bookings = load_bookings()
    return render_template("index.html", bookings=bookings)


@app.route("/add", methods=["POST"])
def add_booking():
    guest = request.form["guest"]
    room = request.form["room"]
    checkin = request.form["checkin"]
    checkout = request.form["checkout"]
    amount = request.form["amount"]
    payment = request.form["payment"]
    source = request.form["source"]
    notes = request.form["notes"]
    customer_email = request.form["email"]

    booking = {
        "guest": guest,
        "room": room,
        "checkin": checkin,
        "checkout": checkout,
        "amount": amount,
        "payment": payment,
        "source": source,
        "notes": notes,
        "email": customer_email,
    }

    # save
    save_booking(booking)

    # send email receipt
    try:
        msg = Message(
            subject="Your Booking Receipt - AX Hotel",
            recipients=[customer_email],
            body=f"""
Hello {guest},

Thank you for booking with AX Hotel.

Booking Details:
- Guest: {guest}
- Room: {room}
- Check-in: {checkin}
- Check-out: {checkout}
- Amount: {amount} USD
- Payment: {payment}
- Source: {source}
- Notes: {notes}

We look forward to hosting you!

AX Hotel Team
            """,
        )
        mail.send(msg)
        flash("Booking added and receipt sent to customer!", "success")
    except Exception as e:
        flash(f"Booking saved but email not sent: {str(e)}", "danger")

    return redirect(url_for("index"))


@app.route("/whatsapp/<guest>/<room>/<checkin>/<checkout>/<amount>/<payment>/<source>/<notes>")
def whatsapp(guest, room, checkin, checkout, amount, payment, source, notes):
    message = f"""*New booking*
Guest: {guest}
Room: {room}
Check-in: {checkin}
Check-out: {checkout}
Amount: {amount} USD
Payment: {payment}
Source: {source}
Notes: {notes}"""

    # send to both bosses
    numbers = ["+905555555555", "+905444444444"]  # change numbers
    for num in numbers:
        webbrowser.open(f"https://wa.me/{num}?text={message}")

    flash("WhatsApp messages opened (check your browser)", "info")
    return redirect(url_for("index"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns port
    app.run(host="0.0.0.0", port=port, debug=False)
