from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import json, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "izedinnursefa235@gmail.com"
app.config['MAIL_PASSWORD'] = "your-app-password"  # <-- put your 16-digit Google App password here
app.config['MAIL_DEFAULT_SENDER'] = "izedinnursefa235@gmail.com"

mail = Mail(app)

BOOKINGS_FILE = "bookings.json"

# --------- Helper Functions ----------
def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        return []
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_booking(data):
    bookings = load_bookings()
    bookings.append(data)
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

# --------- Translations ----------
translations = {
    "en": {
        "title": "Hotel Booking System",
        "guest_name": "Guest Name",
        "room": "Room Number",
        "checkin": "Check-in Date",
        "checkout": "Check-out Date",
        "amount": "Amount (USD)",
        "payment": "Payment Method",
        "source": "Source",
        "notes": "Notes",
        "submit": "Save Booking",
        "language": "Language"
    },
    "tr": {
        "title": "Otel Rezervasyon Sistemi",
        "guest_name": "Misafir Adı",
        "room": "Oda Numarası",
        "checkin": "Giriş Tarihi",
        "checkout": "Çıkış Tarihi",
        "amount": "Tutar (USD)",
        "payment": "Ödeme Yöntemi",
        "source": "Kaynak",
        "notes": "Notlar",
        "submit": "Rezervasyonu Kaydet",
        "language": "Dil"
    },
    "ar": {
        "title": "نظام حجز الفندق",
        "guest_name": "اسم الضيف",
        "room": "رقم الغرفة",
        "checkin": "تاريخ الدخول",
        "checkout": "تاريخ المغادرة",
        "amount": "المبلغ (دولار)",
        "payment": "طريقة الدفع",
        "source": "المصدر",
        "notes": "ملاحظات",
        "submit": "حفظ الحجز",
        "language": "اللغة"
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    lang = session.get("lang", "en")  # default English
    t = translations[lang]

    if request.method == "POST":
        data = {
            "guest": request.form["guest"],
            "room": request.form["room"],
            "checkin": request.form["checkin"],
            "checkout": request.form["checkout"],
            "amount": request.form["amount"],
            "payment": request.form["payment"],
            "source": request.form["source"],
            "notes": request.form.get("notes", "")
        }

        # Save booking
        save_booking(data)

        # --- WhatsApp (Turkish) ---
        whatsapp_msg = (
            f"📢 Yeni Rezervasyon\n"
            f"👤 Misafir: {data['guest']}\n"
            f"🏨 Oda: {data['room']}\n"
            f"📅 Giriş: {data['checkin']} - Çıkış: {data['checkout']}\n"
            f"💵 Tutar: {data['amount']} USD\n"
            f"💳 Ödeme: {data['payment']}\n"
            f"📌 Kaynak: {data['source']}\n"
            f"📝 Notlar: {data['notes']}"
        )
        print("WhatsApp message (Turkish):")
        print(whatsapp_msg)

        # --- Email (English) ---
        email_msg = Message("New Hotel Booking", recipients=["yourboss@example.com"])
        email_msg.body = (
            f"New booking:\n"
            f"Guest: {data['guest']}\n"
            f"Room: {data['room']}\n"
            f"Check-in: {data['checkin']}\n"
            f"Check-out: {data['checkout']}\n"
            f"Amount: {data['amount']} USD\n"
            f"Payment: {data['payment']}\n"
            f"Source: {data['source']}\n"
            f"Notes: {data['notes']}"
        )
        try:
            mail.send(email_msg)
            print("✅ Email sent")
        except Exception as e:
            print("❌ Email failed:", e)

        return redirect(url_for("index"))

    return render_template("index.html", t=t, lang=lang)

@app.route("/setlang/<lang>")
def setlang(lang):
    if lang in translations:
        session["lang"] = lang
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
