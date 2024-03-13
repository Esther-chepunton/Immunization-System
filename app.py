from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Initialize Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immunization.db'
db = SQLAlchemy(app)

# Define the model for Immunization
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(100), nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'), nullable=False)

    # Define the relationship with Vaccine table
    vaccine = db.relationship('Vaccine', backref='patients')

    def __init__(self, patient_name, birth_date, vaccine_id):
        self.patient_name = patient_name
        self.birth_date = birth_date
        self.vaccine_id = vaccine_id

class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    accepted_age = db.Column(db.String(50), nullable=False)


# Set up the application context and create database tables
with app.app_context():
    db.create_all()

# Define routes
@app.route('/')
def index():
    # querry the vaccine table
    vaccines = [
        {'name':'BCD'},
        {'name':'Polio'},
        {'name':'DPT'}
        ]
    #vaccine = Vaccine.query.all()
    return render_template('index.html', vaccines=vaccines)  # Adjust the path here

@app.route('/doctor', methods=['POST'])
def doctor():
    try:
        patient_name = request.form['patient_name']
        birth_date = request.form['birth_date']
        vaccine_id = request.form['vaccine_id']

        # Validate input data (not implemented in this code)
        
        immunization = Patient(patient_name, birth_date, vaccine_id)
        db.session.add(immunization)
        db.session.commit()

        return jsonify({'message': 'Immunization record added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/patient')
def patient():
    try:
        immunizations = Patient.query.all()
        immunization_list = [{'patient_name': i.patient_name, 'birth_date': i.birth_date, 'Vaccine_id': i.Vaccine_id} for i in immunizations]
        return jsonify({'immunizations': immunization_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/vaccine', methods=['POST'])
def enter_vaccine():
    try:
        immunizations = Patient.query.all()
        immunization_list = [{'patient_name': i.patient_name, 'birth_date': i.birth_date, 'Vaccine_id': i.Vaccine_id} for i in immunizations]
        return jsonify({'immunizations': immunization_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/immunization_records')
def immunization_records():
    try:
        # Retrieve all immunization records from the database
        immunization_records = Patient.query.all()
        
        # Render a template with the retrieved data
        return render_template('immunization_records.html', immunization_records=immunization_records)
    except Exception as e:
        # Handle exceptions if any
        return render_template('error.html', error=str(e))

@app.route('/view_data')
def view_data():
    try:
        # Query the database to retrieve immunization records
        immunization_records = Patient.query.all()
        
        # Render a template with the retrieved data
        return render_template('view_data.html', immunization_records=immunization_records)
    except Exception as e:
        # Handle exceptions if any
        return render_template('error.html', error=str(e))    
# Run the application
if __name__ == '__main__':
    app.run(debug=True)