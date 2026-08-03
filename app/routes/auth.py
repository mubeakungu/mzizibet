from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("casino.lobby"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "")
        dob_raw = request.form.get("date_of_birth", "")

        if not all([full_name, phone_number, password, dob_raw]):
            flash("All fields are required.", "error")
            return render_template("auth/register.html")

        try:
            dob = datetime.strptime(dob_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Enter a valid date of birth.", "error")
            return render_template("auth/register.html")

        age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
        if age < 18:
            flash("You must be 18 or older to register.", "error")
            return render_template("auth/register.html")

        if User.query.filter_by(phone_number=phone_number).first():
            flash("An account with that phone number already exists.", "error")
            return render_template("auth/register.html")

        user = User(full_name=full_name, phone_number=phone_number, date_of_birth=dob)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        wallet = Wallet(user_id=user.id, balance=0)
        db.session.add(wallet)
        db.session.commit()

        login_user(user)
        flash("Welcome to Mzizibet. Verify your ID to unlock withdrawals.", "success")
        return redirect(url_for("casino.lobby"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("casino.lobby"))

    if request.method == "POST":
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(phone_number=phone_number).first()
        if user and user.check_password(password):
            can_play, reason = user.can_play()
            login_user(user)
            if not can_play:
                flash(reason, "warning")
            return redirect(url_for("casino.lobby"))

        flash("Invalid phone number or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for("auth.login"))
