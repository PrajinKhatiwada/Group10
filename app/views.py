from functools import wraps
from datetime import datetime
import os

from flask import (Blueprint, render_template, request, session,
                   flash, redirect, url_for, current_app)
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from .forms import (LoginForm, RegisterForm, PropertyForm,
                    EnquiryForm, OfferForm, BookmarkNotesForm,
                    AdminCreateUserForm)
from .models import (UserRole, Property, PropertyCategory, PropertyStatus,
                     Bookmark, Enquiry, EnquiryStatus, Offer, OfferStatus, User)
from . import db

main = Blueprint('main', __name__)


def get_current_user():
    uid = session.get('user_id')
    if uid:
        return db.get_user_by_id(uid)
    return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access that page.', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated


def buyer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or not (user.is_buyer() or user.is_admin()):
            flash('That page is for buyers only.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated


def seller_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or not (user.is_seller() or user.is_admin()):
            flash('That page is for sellers and admins only.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_admin():
            flash('Admin access required.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated


@main.context_processor
def inject_user():
    return dict(current_user=get_current_user())


def save_property_images(image_files, property_title):
    uploaded_images = []

    folder_name = secure_filename(property_title.lower())

    upload_folder = os.path.join(
        current_app.root_path,
        'static',
        'uploads',
        folder_name
    )

    os.makedirs(upload_folder, exist_ok=True)

    for image_file in image_files:
        if image_file and image_file.filename:

            filename = secure_filename(image_file.filename)

            file_path = os.path.join(upload_folder, filename)

            image_file.save(file_path)

            uploaded_images.append(f"{folder_name}/{filename}")

    return uploaded_images


@main.route('/')
def home():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    price_range = request.args.get('price', '')
    bedrooms = request.args.get('bedrooms', '')

    min_price = max_price = min_beds = None

    if price_range == 'under1m':
        max_price = 1_000_000
    elif price_range == '1m-2m':
        min_price, max_price = 1_000_000, 2_000_000
    elif price_range == '2m-3m':
        min_price, max_price = 2_000_000, 3_000_000
    elif price_range == '3m+':
        min_price = 3_000_000

    if bedrooms.isdigit():
        min_beds = int(bedrooms)

    properties = db.search_properties(
        query=query,
        category=category if category else None,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_beds,
    )

    user = get_current_user()
    bookmarked_ids = set()

    if user and user.is_buyer():
        bookmarked_ids = {b.property_id for b in db.get_bookmarks_for_user(user.id)}

    return render_template(
        'index.html',
        properties=properties,
        query=query,
        selected_category=category,
        selected_price=price_range,
        selected_bedrooms=bedrooms,
        bookmarked_ids=bookmarked_ids
    )


@main.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.check_user_login(form.username.data, form.password.data)

        if user:
            session['user_id'] = user.id
            flash(f'Welcome back, {user.firstname}!', 'message')
            return redirect(url_for('main.home'))

        flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.home'))

    form = RegisterForm()

    if form.validate_on_submit():
        if db.get_user_by_username(form.username.data):
            flash('Username already taken. Please choose another.', 'error')
        else:
            role_map = {
                'buyer': UserRole.BUYER,
                'seller': UserRole.SELLER,
                'admin': UserRole.ADMIN
            }

            new_user = User(
                id=db.get_next_user_id(),
                username=form.username.data,
                password_hash=generate_password_hash(form.password.data),
                email=form.email.data,
                firstname=form.firstname.data,
                surname=form.surname.data,
                phone=form.phone.data,
                role=role_map.get(form.role.data, UserRole.BUYER),
            )

            db.add_user(new_user)

            flash('Account created! Please log in.', 'message')
            return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'message')
    return redirect(url_for('main.home'))


@main.route('/property/<property_id>')
def property_details(property_id):
    prop = db.get_property_by_id(property_id)

    if not prop:
        return render_template(
            'error.html',
            code=404,
            message='Property not found.'
        ), 404

    user = get_current_user()
    bookmarked = False
    enquiry_form = EnquiryForm()
    offer_form = OfferForm()

    if user and user.is_buyer():
        bookmarked = db.is_bookmarked(user.id, property_id)

    seller = db.get_user_by_id(prop.seller_id)
    enquiry_count = len(db.get_enquiries_for_property(property_id))
    offer_count = len(db.get_offers_for_property(property_id))
    documents = db.get_documents_for_property(property_id)

    return render_template(
        'property_details.html',
        prop=prop,
        seller=seller,
        bookmarked=bookmarked,
        enquiry_form=enquiry_form,
        offer_form=offer_form,
        enquiry_count=enquiry_count,
        offer_count=offer_count,
        documents=documents
    )


@main.route('/bookmark/<property_id>', methods=['POST'])
@login_required
@buyer_required
def toggle_bookmark(property_id):
    user = get_current_user()
    prop = db.get_property_by_id(property_id)

    if not prop:
        flash('Property not found.', 'error')
        return redirect(url_for('main.home'))

    if db.is_bookmarked(user.id, property_id):
        db.remove_bookmark(user.id, property_id)
        flash('Property removed from saved properties.', 'message')
    else:
        bm = Bookmark(
            id=db.get_next_bookmark_id(),
            user_id=user.id,
            property_id=property_id,
            notes='',
            created_at=datetime.now(),
        )
        db.add_bookmark(bm)
        flash('Property saved to your bookmarks!', 'message')

    return redirect(url_for('main.property_details', property_id=property_id))


@main.route('/bookmark/<property_id>/notes', methods=['POST'])
@login_required
@buyer_required
def update_bookmark_notes(property_id):
    user = get_current_user()
    notes = request.form.get('notes', '')

    db.update_bookmark_notes(user.id, property_id, notes)

    flash('Notes updated.', 'message')
    return redirect(url_for('main.bookmarks'))


@main.route('/bookmark/<property_id>/remove', methods=['POST'])
@login_required
@buyer_required
def remove_bookmark(property_id):
    user = get_current_user()

    db.remove_bookmark(user.id, property_id)

    flash('Property removed from saved properties.', 'message')
    return redirect(url_for('main.bookmarks'))


@main.route('/bookmarks')
@login_required
@buyer_required
def bookmarks():
    user = get_current_user()
    bms = db.get_bookmarks_for_user(user.id)
    props_map = {p.id: p for p in db.get_all_properties()}
    items = [(bm, props_map[bm.property_id]) for bm in bms if bm.property_id in props_map]

    return render_template('bookmarks.html', items=items)


@main.route('/property/<property_id>/enquiry', methods=['POST'])
@login_required
@buyer_required
def submit_enquiry(property_id):
    form = EnquiryForm()

    if form.validate_on_submit():
        user = get_current_user()

        enq = Enquiry(
            id=db.get_next_enquiry_id(),
            property_id=property_id,
            buyer_id=user.id,
            message=form.message.data,
            status=EnquiryStatus.NEW,
            created_at=datetime.now(),
        )

        db.add_enquiry(enq)

        flash('Your enquiry has been submitted!', 'message')
    else:
        flash('Please enter a valid message (at least 10 characters).', 'error')

    return redirect(url_for('main.property_details', property_id=property_id))


@main.route('/property/<property_id>/offer', methods=['POST'])
@login_required
@buyer_required
def submit_offer(property_id):
    form = OfferForm()

    if form.validate_on_submit():
        user = get_current_user()

        offer = Offer(
            id=db.get_next_offer_id(),
            property_id=property_id,
            buyer_id=user.id,
            amount=form.amount.data,
            message=form.message.data or '',
            status=OfferStatus.PENDING,
            created_at=datetime.now(),
        )

        db.add_offer(offer)

        flash('Your offer has been submitted!', 'message')
    else:
        flash('Please enter a valid offer amount.', 'error')

    return redirect(url_for('main.property_details', property_id=property_id))


@main.route('/listings')
@login_required
@seller_required
def listings():
    user = get_current_user()

    if user.is_admin():
        props = db.get_all_properties()
    else:
        props = db.get_properties_by_seller(user.id)

    active_count = sum(1 for p in props if p.status == PropertyStatus.ACTIVE)
    enquiry_count = sum(len(db.get_enquiries_for_property(p.id)) for p in props)
    offer_count = sum(len(db.get_offers_for_property(p.id)) for p in props)

    return render_template(
        'listings.html',
        props=props,
        active_count=active_count,
        enquiry_count=enquiry_count,
        offer_count=offer_count
    )


@main.route('/listings/new', methods=['GET', 'POST'])
@login_required
@seller_required
def new_listing():
    form = PropertyForm()

    if form.validate_on_submit():
        user = get_current_user()
        cat = PropertyCategory(form.category.data)
        stat = PropertyStatus(form.status.data)
        features = [f.strip() for f in form.features.data.split(',') if f.strip()]

        uploaded_images = save_property_images(request.files.getlist('images'),form.title.data)

        prop = Property(
            id=db.get_next_property_id(),
            title=form.title.data,
            address=form.address.data,
            suburb=form.suburb.data,
            description=form.description.data,
            price=form.price.data,
            original_price=form.original_price.data,
            category=cat,
            status=stat,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            car_spaces=form.car_spaces.data,
            size_sqft=form.size_sqft.data,
            seller_id=user.id,
            images=uploaded_images,
            features=features,
            created_at=datetime.now(),
        )

        db.add_property(prop)

        doc_file = form.document_file.data
        doc_name = form.document_name.data

        if doc_file and doc_file.filename:
            filename = secure_filename(doc_file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                'static',
                'documents'
            )

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            doc_file.save(file_path)

            file_size = f"{round(os.path.getsize(file_path) / 1024, 1)} KB"
            file_type = filename.rsplit('.', 1)[-1].upper()

            db.add_document(
                property_id=prop.id,
                document_name=doc_name or filename,
                file_name=filename,
                file_size=file_size,
                file_type=file_type
            )

        flash('Listing created successfully!', 'message')
        return redirect(url_for('main.listings'))

    return render_template('property_form.html', form=form, title='New Listing')


@main.route('/listings/<property_id>/edit', methods=['GET', 'POST'])
@login_required
@seller_required
def edit_listing(property_id):
    prop = db.get_property_by_id(property_id)

    if not prop:
        return render_template(
            'error.html',
            code=404,
            message='Property not found.'
        ), 404

    user = get_current_user()

    if not user.is_admin() and prop.seller_id != user.id:
        flash('You can only edit your own listings.', 'error')
        return redirect(url_for('main.listings'))

    form = PropertyForm()

    if form.validate_on_submit():
        cat = PropertyCategory(form.category.data)
        stat = PropertyStatus(form.status.data)
        features = [f.strip() for f in form.features.data.split(',') if f.strip()]

        uploaded_images = save_property_images(request.files.getlist('images'),form.title.data)

        if not uploaded_images:
            uploaded_images = prop.images

        updated = Property(
            id=property_id,
            title=form.title.data,
            address=form.address.data,
            suburb=form.suburb.data,
            description=form.description.data,
            price=form.price.data,
            original_price=form.original_price.data,
            category=cat,
            status=stat,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            car_spaces=form.car_spaces.data,
            size_sqft=form.size_sqft.data,
            seller_id=prop.seller_id,
            images=uploaded_images,
            features=features,
            created_at=prop.created_at,
        )

        db.update_property(property_id, updated)

        doc_file = form.document_file.data
        doc_name = form.document_name.data

        if doc_file and doc_file.filename:
            filename = secure_filename(doc_file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                'static',
                'documents'
            )

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            doc_file.save(file_path)

            file_size = f"{round(os.path.getsize(file_path) / 1024, 1)} KB"
            file_type = filename.rsplit('.', 1)[-1].upper()

            db.add_document(
                property_id=property_id,
                document_name=doc_name or filename,
                file_name=filename,
                file_size=file_size,
                file_type=file_type
            )

        flash('Listing updated successfully!', 'message')
        return redirect(url_for('main.listings'))

    form.title.data = prop.title
    form.address.data = prop.address
    form.suburb.data = prop.suburb
    form.description.data = prop.description
    form.price.data = prop.price
    form.original_price.data = prop.original_price
    form.category.data = prop.category.value
    form.status.data = prop.status.value
    form.bedrooms.data = prop.bedrooms
    form.bathrooms.data = prop.bathrooms
    form.car_spaces.data = prop.car_spaces
    form.size_sqft.data = prop.size_sqft
    form.features.data = ', '.join(prop.features)

    return render_template(
        'property_form.html',
        form=form,
        title='Edit Listing',
        prop=prop
    )


@main.route('/listings/<property_id>/delete', methods=['POST'])
@login_required
@seller_required
def delete_listing(property_id):
    prop = db.get_property_by_id(property_id)
    user = get_current_user()

    if prop and (user.is_admin() or prop.seller_id == user.id):
        db.delete_property(property_id)
        flash('Listing deleted.', 'message')
    else:
        flash('You do not have permission to delete this listing.', 'error')

    return redirect(url_for('main.listings'))


@main.route('/listings/<property_id>/enquiries')
@login_required
@seller_required
def listing_enquiries(property_id):
    prop = db.get_property_by_id(property_id)

    if not prop:
        return render_template(
            'error.html',
            code=404,
            message='Property not found.'
        ), 404

    user = get_current_user()

    if not user.is_admin() and prop.seller_id != user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.listings'))

    enquiries = db.get_enquiries_for_property(property_id)
    buyers = {e.buyer_id: db.get_user_by_id(e.buyer_id) for e in enquiries}

    return render_template(
        'enquiries.html',
        prop=prop,
        enquiries=enquiries,
        buyers=buyers,
        EnquiryStatus=EnquiryStatus
    )


@main.route('/enquiry/<enquiry_id>/status', methods=['POST'])
@login_required
@seller_required
def update_enquiry_status(enquiry_id):
    new_status_val = request.form.get('status')

    try:
        new_status = EnquiryStatus(new_status_val)
    except ValueError:
        flash('Invalid status.', 'error')
        return redirect(url_for('main.listings'))

    db.update_enquiry_status(enquiry_id, new_status)

    flash('Enquiry status updated.', 'message')

    prop_id = request.form.get('property_id')
    return redirect(url_for('main.listing_enquiries', property_id=prop_id))


@main.route('/listings/<property_id>/offers')
@login_required
@seller_required
def listing_offers(property_id):
    prop = db.get_property_by_id(property_id)

    if not prop:
        return render_template(
            'error.html',
            code=404,
            message='Property not found.'
        ), 404

    user = get_current_user()

    if not user.is_admin() and prop.seller_id != user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.listings'))

    offers = db.get_offers_for_property(property_id)
    buyers = {o.buyer_id: db.get_user_by_id(o.buyer_id) for o in offers}

    return render_template(
        'offers.html',
        prop=prop,
        offers=offers,
        buyers=buyers,
        OfferStatus=OfferStatus
    )


@main.route('/offer/<offer_id>/status', methods=['POST'])
@login_required
@seller_required
def update_offer_status(offer_id):
    new_status_val = request.form.get('status')

    try:
        new_status = OfferStatus(new_status_val)
    except ValueError:
        flash('Invalid status.', 'error')
        return redirect(url_for('main.listings'))

    db.update_offer_status(offer_id, new_status)

    flash('Offer status updated.', 'message')

    prop_id = request.form.get('property_id')
    return redirect(url_for('main.listing_offers', property_id=prop_id))


@main.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = db.get_all_users()
    return render_template('admin_users.html', users=users)


@main.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_new_user():
    form = AdminCreateUserForm()

    if form.validate_on_submit():
        if db.get_user_by_username(form.username.data):
            flash('Username already exists.', 'error')
        else:
            role_map = {
                'buyer': UserRole.BUYER,
                'seller': UserRole.SELLER,
                'admin': UserRole.ADMIN
            }

            new_user = User(
                id=db.get_next_user_id(),
                username=form.username.data,
                password_hash=generate_password_hash(form.password.data),
                email=form.email.data,
                firstname=form.firstname.data,
                surname=form.surname.data,
                phone=form.phone.data,
                role=role_map.get(form.role.data, UserRole.BUYER),
            )

            db.add_user(new_user)

            flash('User created successfully.', 'message')
            return redirect(url_for('main.admin_users'))

    return render_template('admin_user_form.html', form=form)


@main.route('/admin/users/<user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    current = get_current_user()

    if current.id == user_id:
        flash('You cannot delete your own account.', 'error')
    else:
        db.delete_user(user_id)
        flash('User deleted.', 'message')

    return redirect(url_for('main.admin_users'))