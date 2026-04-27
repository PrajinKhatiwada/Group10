from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/listings")
def listings():
    return render_template("listings.html")

@main.route("/bookmarks")
def bookmarks():
    return render_template("bookmarks.html")

@main.route("/property-details")
def property_details():
    return render_template("property_details.html")