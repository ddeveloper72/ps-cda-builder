import os
import secrets
from flask import Flask, render_template, redirect, request, url_for, flash, send_from_directory
from cda_generator import generate_cda_for_patient, get_patient_list


# initialize the Flask app
app = Flask(__name__)

# Secret key for the session
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Rout for main page
@app.route('/')
def index():
    patients = get_patient_list().to_dict(orient='records')
    return render_template('index.html', patients=patients)



# Route to handle CDA generation request
@app.route('/generate_cda', methods=['POST'])
def generate_cda():
    patient_id = request.form.get('patient_id')
    if patient_id:
        generate_cda_for_patient(patient_id)  # Call the correct function to generate CDA
        return redirect(url_for('download_cda', patient_id=patient_id))
    return redirect(url_for('index'))

# Route to download the CDA document
@app.route('/download_cda/<patient_id>')
def download_cda(patient_id):
    # Specify the file path for the generated CDA document
    directory = os.path.join(app.root_path, 'static/out')
    file_name = f"{patient_id}_ps_sample_cda.xml"
    return send_from_directory(directory, file_name, as_attachment=True)

# Page not found error handler
@app.errorhandler(404)
def page_not_found(e):
    flash(e, 'alert-danger')
    return render_template('404.html'), 404

# Internal server error handler
@app.errorhandler(500)
def internal_server_error(e):
    flash(e, 'alert-danger')
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)