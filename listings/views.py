from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Listing

listings_bp = Blueprint("listings", __name__, template_folder="templates/listings")

@listings_bp.route("/")
def all_listings():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template("listings/all_listings.html", listings=listings)

@listings_bp.route("/listing/<int:listing_id>")
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template("listings/view_listing.html", listing=listing)

@listings_bp.route("/listing/new", methods=["GET", "POST"])
@login_required
def new_listing():
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")

        listing = Listing(
            title=title,
            category=category,
            description=description,
            user_id=current_user.id
        )
        db.session.add(listing)
        db.session.commit()
        flash("Your craft listing has been posted!", "success")
        return redirect(url_for("listings.all_listings"))

    return render_template("listings/new_listing.html")

@listings_bp.route("/listing/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != current_user.id:
        abort(403)  # Forbidden

    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.category = request.form.get("category")
        listing.description = request.form.get("description")
        db.session.commit()
        flash("Listing updated successfully!", "info")
        return redirect(url_for("listings.view_listing", listing_id=listing.id))

    return render_template("listings/edit_listing.html", listing=listing)

@listings_bp.route("/listing/<int:listing_id>/delete", methods=["POST"])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != current_user.id:
        abort(403)

    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted.", "danger")
    return redirect(url_for("listings.all_listings"))
