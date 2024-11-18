from flask import Flask, request, render_template
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

# Database connection settings (use environment variables for security in ACS)
db_username = os.getenv("DB_USERNAME", "your_db_username")
db_password = os.getenv("DB_PASSWORD", "your_db_password")
db_host = os.getenv("DB_HOST", "your_rds_endpoint")  # e.g., 'your-instance-name.xxxxxxx.us-east-1.rds.amazonaws.com'
db_name = os.getenv("DB_NAME", "your_database_name")

# Set up the SQLAlchemy engine
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}')


@app.route('/')
def home():
    # Fetch distinct DriverID values to populate the dropdown
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DISTINCT DriverID FROM dispatch_data"))
        drivers = [row['DriverID'] for row in result.mappings()]  # Use .mappings() to get rows as dictionaries

    # Render the template with the list of drivers
    return render_template('index.html', drivers=drivers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
