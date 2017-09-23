DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


#Define the database - we are working with
#We'll use SQLite for now
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')



SECRET_KEY = 'thisisasecret'

CB_API_KEY = "XfuZZtRQoIT60ZbC"
CB_API_SECRET = "eXFKOkiLqf47WKsvt5dDgoJAuF3VWFfW"

