____________________________________________________________

  Property Sales – Web Application
  Assessment 3 | Flask Real Estate App
____________________________________________________________

SETUP INSTRUCTIONS
------------------

1. Prerequisites: Ensure Python 3.10+ is installed on your system.

2. Install Dependencies: Open a terminal in the root project folder (where run.py is) and run: 

pip install -r requirements.txt

3. Run the application: From the same root folder, run:

python run.py

The app will start at:  http://127.0.0.1:8888

4. Copy the link and paste it in the browser(Navigate to):  

http://127.0.0.1:8888


----------------------
DEMO LOGIN CREDENTIALS
----------------------

  Role     | Username  | Password
  ---------|-----------|----------
  Admin    | admin1    | Admin123
  Admin    | admin2    | Admin123
  Seller   | seller1   | Seller123
  Seller   | seller2   | Seller123
  Buyer    | buyer1    | Buyer123
  Buyer    | buyer2    | Buyer123
   and many more Users

----------------
FOLDER STRUCTURE
----------------

  run.py                   – Entry point
  README.txt               – This file
  requirements.txt         – Python dependencies
  property.sql             – Database SQL code
  project/
    __init__.py            – App factory, error handlers
    routes.py              – All routes and access control
    views.py               – Manage database connections, cursors, and Parametrized SQL queries
    models.py              – Dataclasses and enums
    forms.py               – WTForms form definitions
    static/
      css/
        styles.css         – Custom stylesheet
      img/
        ...                – Default property image, logo images and others
      documents/
        ...                – All the uplodaed documents
      uploads/
        property_title
          ...              – All the uploaded property images
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

-------
NOTES
-------

- This application uses and manages the data inside a database using Parametrized SQL queries.
  The initial dummy data is in the property.sql file.
- No virtual environment folder is included in this submission.
- All passwords are hashed using Werkzeug's generate_password_hash.

_____________________________________________________________________
