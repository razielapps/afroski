from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from utils import save_image
from app.models import Listing,db,User,Message
from forms import MessageForm

listings_bp = Blueprint("listings", __name__, template_folder="templates/listings")

@listings_bp.route("/listings")
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

        # Handle image
        image_file = request.files.get("image")
        filename = None

        if image_file and image_file.filename != "":
            filename = save_image(image_file, "listings")

        listing = Listing(
            title=title,
            category=category,
            description=description,
            image=filename,            # ← store image filename
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
        abort(403)

    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.category = request.form.get("category")
        listing.description = request.form.get("description")

        # Handle optional image update
        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            filename = save_image(image_file, "listings")
            listing.image = filename   # overwrite old image

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



@app.route("/messages/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)
    form = MessageForm()

    # Fetch conversation
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    # Handle new message
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            body=form.body.data
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for("chat", user_id=user_id))

    return render_template("messages/chat.html",
                           other_user=other_user,
                           messages=messages,
                           form=form)

@messages_bp.route("/messages")
@login_required
def inbox():
    # Find all users who have chatted with the current user
    sent_to = (
        Message.query
        .filter_by(sender_id=current_user.id)
        .with_entities(Message.receiver_id)
    )

    received_from = (
        Message.query
        .filter_by(receiver_id=current_user.id)
        .with_entities(Message.sender_id)
    )

    # Create a unique set of conversation partner IDs
    user_ids = {uid for (uid,) in sent_to.union(received_from).all()}

    # Fetch user objects for each ID
    users = User.query.filter(User.id.in_(user_ids)).all()

    # Last message for preview
    last_messages = {}
    for uid in user_ids:
        last_messages[uid] = (
            Message.query.filter(
                ((Message.sender_id == current_user.id) & (Message.receiver_id == uid)) |
                ((Message.sender_id == uid) & (Message.receiver_id == current_user.id))
            )
            .order_by(Message.timestamp.desc())
            .first()
        )

    return render_template("messages/inbox.html", users=users, last_messages=last_messages)
