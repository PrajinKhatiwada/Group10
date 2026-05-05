import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app

from .db import db
from .models import User, Property, PropertyDocument

main = Blueprint("main", __name__)


def login_required():
    return "user_id" in session


def seller_required():
    return session.get("role") == "seller"


def save_image(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        return "uploads/" + filename
    return None


def save_document(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config["DOCUMENT_UPLOAD_FOLDER"], filename)
        file.save(path)
        return "documents/" + filename
    return None


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/listings")
def listings():
    if not login_required():
        return redirect(url_for("main.login"))

    if session.get("role") == "seller":
        properties = Property.query.filter_by(seller_id=session["user_id"]).order_by(Property.created_at.desc()).all()
    else:
        properties = Property.query.order_by(Property.created_at.desc()).all()

    return render_template("listings.html", properties=properties)


@main.route("/property-details/<int:property_id>")
def property_details(property_id):
    if not login_required():
        return redirect(url_for("main.login"))

    property = Property.query.get_or_404(property_id)

    return render_template("property_details.html", property=property)


@main.route("/add-property", methods=["GET", "POST"])
def add_property():
    if not login_required():
        return redirect(url_for("main.login"))

    if not seller_required():
        flash("Only sellers can list properties.", "danger")
        return redirect(url_for("main.listings"))

    if request.method == "POST":
        main_image = save_image(request.files.get("main_image"))
        side_image_one = save_image(request.files.get("side_image_one"))
        side_image_two = save_image(request.files.get("side_image_two"))

        property = Property(
            title=request.form.get("title"),
            address=request.form.get("address"),
            suburb=request.form.get("suburb"),
            price=request.form.get("price"),
            old_price=request.form.get("old_price") or None,
            status=request.form.get("status"),
            bedrooms=request.form.get("bedrooms"),
            bathrooms=request.form.get("bathrooms"),
            car_spaces=request.form.get("car_spaces"),
            area_sqft=request.form.get("area_sqft"),
            description=request.form.get("description"),
            features=request.form.get("features"),
            main_image=main_image,
            side_image_one=side_image_one,
            side_image_two=side_image_two,
            enquiries_count=request.form.get("enquiries_count") or 0,
            offers_pending=request.form.get("offers_pending") or 0,
            seller_id=session["user_id"]
        )

        db.session.add(property)
        db.session.commit()

        document_files = request.files.getlist("documents")
        document_names = request.form.getlist("document_names")

        for index, document_file in enumerate(document_files):
            file_path = save_document(document_file)

            if file_path:
                document = PropertyDocument(
                    document_name=document_names[index] if index < len(document_names) and document_names[index] else document_file.filename,
                    file_path=file_path,
                    file_type=document_file.content_type,
                    file_size="Uploaded",
                    property_id=property.id
                )
                db.session.add(document)

        db.session.commit()

        flash("Property added successfully.", "success")
        return redirect(url_for("main.listings"))

    return render_template("property_form.html", property=None)


@main.route("/edit-property/<int:property_id>", methods=["GET", "POST"])
def edit_property(property_id):
    if not login_required():
        return redirect(url_for("main.login"))

    if not seller_required():
        flash("Only sellers can edit properties.", "danger")
        return redirect(url_for("main.listings"))

    property = Property.query.get_or_404(property_id)

    if property.seller_id != session["user_id"]:
        flash("You can only edit your own properties.", "danger")
        return redirect(url_for("main.listings"))

    if request.method == "POST":
        property.title = request.form.get("title")
        property.address = request.form.get("address")
        property.suburb = request.form.get("suburb")
        property.price = request.form.get("price")
        property.old_price = request.form.get("old_price") or None
        property.status = request.form.get("status")
        property.bedrooms = request.form.get("bedrooms")
        property.bathrooms = request.form.get("bathrooms")
        property.car_spaces = request.form.get("car_spaces")
        property.area_sqft = request.form.get("area_sqft")
        property.description = request.form.get("description")
        property.features = request.form.get("features")
        property.enquiries_count = request.form.get("enquiries_count") or 0
        property.offers_pending = request.form.get("offers_pending") or 0

        main_image = save_image(request.files.get("main_image"))
        side_image_one = save_image(request.files.get("side_image_one"))
        side_image_two = save_image(request.files.get("side_image_two"))

        if main_image:
            property.main_image = main_image
        if side_image_one:
            property.side_image_one = side_image_one
        if side_image_two:
            property.side_image_two = side_image_two

        document_files = request.files.getlist("documents")
        document_names = request.form.getlist("document_names")

        for index, document_file in enumerate(document_files):
            file_path = save_document(document_file)

            if file_path:
                document = PropertyDocument(
                    document_name=document_names[index] if index < len(document_names) and document_names[index] else document_file.filename,
                    file_path=file_path,
                    file_type=document_file.content_type,
                    file_size="Uploaded",
                    property_id=property.id
                )
                db.session.add(document)

        db.session.commit()

        flash("Property updated successfully.", "success")
        return redirect(url_for("main.property_details", property_id=property.id))

    return render_template("property_form.html", property=property)


@main.route("/bookmarks")
def bookmarks():
    if not login_required():
        return redirect(url_for("main.login"))

    properties = Property.query.order_by(Property.created_at.desc()).limit(3).all()
    return render_template("bookmarks.html", properties=properties)


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("main.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("main.login"))

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("main.login"))

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["role"] = user.role

        flash("Login successful.", "success")
        return redirect(url_for("main.listings"))

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))