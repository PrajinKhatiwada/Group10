============================================================
  Property Sales – Web Application
  Assessment 3 | Flask Real Estate App
============================================================

SETUP INSTRUCTIONS
------------------

1. PREREQUISITES
   Ensure Python 3.10+ is installed on your system.

2. INSTALL DEPENDENCIES
   Open a terminal in the root project folder (where run.py lives) and run:

       pip install -r requirements.txt

3. RUN THE APPLICATION
   From the same root folder, run:

       python run.py

   The app will start at:  http://127.0.0.1:8888

4. OPEN IN BROWSER
   Navigate to:  http://127.0.0.1:8888


------------------------------------------------------------
DEMO LOGIN CREDENTIALS
------------------------------------------------------------

  Role     | Username  | Password
  ---------|-----------|----------
  Admin    | admin1    | admin123
  Admin    | admin2    | admin123
  Seller   | seller1   | seller123
  Seller   | seller2   | seller123
  Buyer    | buyer1    | buyer123
  Buyer    | buyer2    | buyer123

------------------------------------------------------------
FOLDER STRUCTURE
------------------------------------------------------------

  run.py                   – Entry point
  README.txt               – This file
  requirements.txt         – Python dependencies
  project/
    __init__.py            – App factory, error handlers
    views.py               – All routes and access control
    models.py              – Dataclasses and enums
    db.py                  – In-memory data store and helpers
    forms.py               – WTForms form definitions
    static/
      css/
        styles.css         – Custom stylesheet
      img/
        ...                – Property and logo images
    templates/
      base.html            – Base layout (navbar, footer, flash)
      index.html           – Home page (search, filter, browse)
      property_details.html – Property detail, enquiry, offer
      listings.html        – Seller/admin listing management
      bookmarks.html       – Buyer saved properties
      login.html           – Login page
      register.html        – Registration page
      error.html           – 404 / 500 error page
      property_form.html   – Create / edit listing form
      enquiries.html       – Seller enquiry management
      offers.html          – Seller offer management
      admin_users.html     – Admin user management
      admin_user_form.html – Admin create user form

------------------------------------------------------------
NOTES
------------------------------------------------------------

- This application uses an in-memory data store (db.py).
  Data resets each time the server is restarted.
- No virtual environment folder is included in this submission.
- All passwords are hashed using Werkzeug's generate_password_hash.

============================================================
