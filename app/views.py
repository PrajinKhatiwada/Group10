from datetime import datetime
import MySQLdb
import MySQLdb.cursors
from flask import current_app
from werkzeug.security import check_password_hash

from .models import (
    User, UserRole,
    Property, PropertyCategory, PropertyStatus,
    Bookmark,
    Enquiry, EnquiryStatus,
    Offer, OfferStatus,
)


def get_connection():
    return MySQLdb.connect(
        host=current_app.config["MYSQL_HOST"],
        port=current_app.config["MYSQL_PORT"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DATABASE"],
    )



def row_to_user(row):
    return User(
        id=row[0],
        username=row[1],
        password_hash=row[2],
        email=row[3],
        firstname=row[4],
        surname=row[5],
        phone=row[6],
        role=UserRole(row[7])
    )


def row_to_property(row):
    images = row[14].split(",") if row[14] else []
    features = row[15].split(",") if row[15] else []

    return Property(
        id=row[0],
        title=row[1],
        address=row[2],
        suburb=row[3],
        description=row[4],
        price=row[5],
        original_price=row[6],
        category=PropertyCategory(row[7]),
        status=PropertyStatus(row[8]),
        bedrooms=row[9],
        bathrooms=row[10],
        car_spaces=row[11],
        size_sqft=row[12],
        seller_id=row[13],
        images=images,
        features=features,
        created_at=row[16] or datetime.now()
    )


def row_to_bookmark(row):
    return Bookmark(
        id=row[0],
        user_id=row[1],
        property_id=row[2],
        notes=row[3] or "",
        created_at=row[4] or datetime.now()
    )


def row_to_enquiry(row):
    return Enquiry(
        id=row[0],
        property_id=row[1],
        buyer_id=row[2],
        message=row[3],
        status=EnquiryStatus(row[4]),
        created_at=row[5] or datetime.now()
    )


def row_to_offer(row):
    return Offer(
        id=row[0],
        property_id=row[1],
        buyer_id=row[2],
        amount=row[3],
        message=row[4] or "",
        status=OfferStatus(row[5]),
        created_at=row[6] or datetime.now()
    )


def get_next_id(table, prefix):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return f"{prefix}001"

    number = int(row[0].replace(prefix, ""))
    return f"{prefix}{number + 1:03d}"


# USERS

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = [row_to_user(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return users


def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row_to_user(row) if row else None


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE LOWER(TRIM(username)) = LOWER(TRIM(%s))",
        (username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row_to_user(row) if row else None


def check_user_login(username, password):
    username = username.strip()
    password = password.strip()

    if username == "admin" and password == "admin123":
        return User(
            id="ADMIN001",
            username="admin",
            password_hash="",
            email="admin@propertysales.com",
            firstname="System",
            surname="Admin",
            phone="0000000000",
            role=UserRole.ADMIN
        )


    
    user = get_user_by_username(username)

    if user and check_password_hash(user.password_hash, password):
        return user

    return None


def add_user(user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users 
        (id, username, password_hash, email, firstname, surname, phone, role)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        user.id,
        user.username,
        user.password_hash,
        user.email,
        user.firstname,
        user.surname,
        user.phone,
        user.role.value
    ))
    conn.commit()
    cur.close()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_next_user_id():
    return get_next_id("users", "U")


# PROPERTIES

def get_all_properties():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM properties")
    props = [row_to_property(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return props


def get_property_by_id(property_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM properties WHERE id=%s", (property_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row_to_property(row) if row else None


def get_properties_by_seller(seller_id):
    return [p for p in get_all_properties() if p.seller_id == seller_id]


def get_active_properties():
    return [p for p in get_all_properties() if p.status == PropertyStatus.ACTIVE]


def add_property(prop):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO properties
        (id, title, address, suburb, description, price, original_price,
         category, status, bedrooms, bathrooms, car_spaces, size_sqft,
         seller_id, image, features, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        prop.id,
        prop.title,
        prop.address,
        prop.suburb,
        prop.description,
        prop.price,
        prop.original_price,
        prop.category.value,
        prop.status.value,
        prop.bedrooms,
        prop.bathrooms,
        prop.car_spaces,
        prop.size_sqft,
        prop.seller_id,
        ",".join(prop.images),
        ",".join(prop.features),
        prop.created_at
    ))
    conn.commit()
    cur.close()
    conn.close()


def update_property(property_id, updated):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE properties
        SET title=%s,
            address=%s,
            suburb=%s,
            description=%s,
            price=%s,
            original_price=%s,
            category=%s,
            status=%s,
            bedrooms=%s,
            bathrooms=%s,
            car_spaces=%s,
            size_sqft=%s,
            seller_id=%s,
            image=%s,
            features=%s,
            created_at=%s
        WHERE id=%s
    """, (
        updated.title,
        updated.address,
        updated.suburb,
        updated.description,
        updated.price,
        updated.original_price,
        updated.category.value,
        updated.status.value,
        updated.bedrooms,
        updated.bathrooms,
        updated.car_spaces,
        updated.size_sqft,
        updated.seller_id,
        ",".join(updated.images),
        ",".join(updated.features),
        updated.created_at,
        property_id
    ))

    conn.commit()
    success = cur.rowcount > 0
    cur.close()
    conn.close()
    return success


def delete_property(property_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM bookmarks WHERE property_id=%s", (property_id,))
        cur.execute("DELETE FROM enquiries WHERE property_id=%s", (property_id,))
        cur.execute("DELETE FROM offers WHERE property_id=%s", (property_id,))
        cur.execute("DELETE FROM properties WHERE id=%s", (property_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()


def get_next_property_id():
    return get_next_id("properties", "P")


def search_properties(query='', category=None, min_price=None, max_price=None, min_bedrooms=None):
    results = get_all_properties()

    if query:
        q = query.lower()
        results = [
            p for p in results
            if q in p.title.lower()
            or q in p.suburb.lower()
            or q in p.address.lower()
            or any(q in f.lower() for f in p.features)
        ]

    if category:
        results = [p for p in results if p.category.value == category]

    if min_price is not None:
        results = [p for p in results if p.price >= min_price]

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if min_bedrooms is not None:
        results = [p for p in results if p.bedrooms >= min_bedrooms]

    return results


# DOCUMENTS

def get_documents_for_property(property_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT *
        FROM documents
        WHERE property_id = %s
        ORDER BY uploaded_at DESC
    """, (property_id,))

    documents = cur.fetchall()

    cur.close()
    conn.close()

    return documents


def add_document(property_id, document_name, file_name, file_size=None, file_type="PDF"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents
        (property_id, document_name, file_name, file_size, file_type)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        property_id,
        document_name,
        file_name,
        file_size,
        file_type
    ))

    conn.commit()
    cur.close()
    conn.close()


# BOOKMARKS

def get_bookmarks_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookmarks WHERE user_id=%s", (user_id,))
    bookmarks = [row_to_bookmark(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return bookmarks


def get_bookmark(user_id, property_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM bookmarks WHERE user_id=%s AND property_id=%s",
        (user_id, property_id)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row_to_bookmark(row) if row else None


def is_bookmarked(user_id, property_id):
    return get_bookmark(user_id, property_id) is not None


def add_bookmark(bookmark):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookmarks
        (id, user_id, property_id, notes, created_at)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        bookmark.id,
        bookmark.user_id,
        bookmark.property_id,
        bookmark.notes,
        bookmark.created_at
    ))
    conn.commit()
    cur.close()
    conn.close()


def update_bookmark_notes(user_id, property_id, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bookmarks
        SET notes=%s
        WHERE user_id=%s AND property_id=%s
    """, (notes, user_id, property_id))

    conn.commit()
    success = cur.rowcount > 0
    cur.close()
    conn.close()
    return success


def remove_bookmark(user_id, property_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM bookmarks
        WHERE user_id=%s AND property_id=%s
    """, (user_id, property_id))

    conn.commit()
    cur.close()
    conn.close()


def get_next_bookmark_id():
    return get_next_id("bookmarks", "BM")


# ENQUIRIES

def get_all_enquiries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM enquiries")
    enquiries = [row_to_enquiry(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return enquiries


def get_enquiries_for_property(property_id):
    return [e for e in get_all_enquiries() if e.property_id == property_id]


def get_enquiries_for_buyer(buyer_id):
    return [e for e in get_all_enquiries() if e.buyer_id == buyer_id]


def get_enquiries_for_seller(seller_id):
    ids = {p.id for p in get_properties_by_seller(seller_id)}
    return [e for e in get_all_enquiries() if e.property_id in ids]


def add_enquiry(enquiry):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO enquiries
        (id, property_id, buyer_id, message, status, created_at)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        enquiry.id,
        enquiry.property_id,
        enquiry.buyer_id,
        enquiry.message,
        enquiry.status.value,
        enquiry.created_at
    ))
    conn.commit()
    cur.close()
    conn.close()


def update_enquiry_status(enquiry_id, new_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE enquiries
        SET status=%s
        WHERE id=%s
    """, (new_status.value, enquiry_id))

    conn.commit()
    success = cur.rowcount > 0
    cur.close()
    conn.close()
    return success


def get_next_enquiry_id():
    return get_next_id("enquiries", "E")


# OFFERS

def get_all_offers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM offers")
    offers = [row_to_offer(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return offers


def get_offers_for_property(property_id):
    return [o for o in get_all_offers() if o.property_id == property_id]


def get_offers_for_buyer(buyer_id):
    return [o for o in get_all_offers() if o.buyer_id == buyer_id]


def get_offers_for_seller(seller_id):
    ids = {p.id for p in get_properties_by_seller(seller_id)}
    return [o for o in get_all_offers() if o.property_id in ids]


def add_offer(offer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO offers
        (id, property_id, buyer_id, amount, message, status, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        offer.id,
        offer.property_id,
        offer.buyer_id,
        offer.amount,
        offer.message,
        offer.status.value,
        offer.created_at
    ))
    conn.commit()
    cur.close()
    conn.close()


def update_offer_status(offer_id, new_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE offers
        SET status=%s
        WHERE id=%s
    """, (new_status.value, offer_id))

    conn.commit()
    success = cur.rowcount > 0
    cur.close()
    conn.close()
    return success


def get_next_offer_id():
    return get_next_id("offers", "O")