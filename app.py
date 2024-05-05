from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime
import pytz
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Convert form data to a dictionary
        form_data = request.form.to_dict()

        # Create timezone object to use when getting current timezone
        PST = pytz.timezone('America/Los_Angeles')
        submission_time = datetime.now(PST).strftime('%H:%M:%s')

        # Add submission_time to form_data dictionary
        form_data['submissionTime'] = submission_time

        # Extract needed fields for the filename
        company = form_data.get('company', 'UnknownCompany')
        job_title = form_data.get('jobTitle', 'UnknownJobTitle')
        current_date = form_data.get('applicationDate', f'{datetime.now().strftime("%Y-%m-%d")}')

        # Create the filename
        filename = f"{company}_{job_title}_{current_date}.csv"

        # Specify the directory to save the CSV
        save_directory = 'PycharmProjects/snowcones/stage'
        os.makedirs(save_directory, exist_ok=True)

        # Define the full path for the CSV file
        filepath = os.path.join(save_directory, filename)

        # Write form data to CSV, including a header if the file is new
        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=form_data.keys())
            if os.stat(filepath).st_size == 0:
                writer.writeheader()
            writer.writerow(form_data)

        # Return a JSON response for the AJAX call
        return jsonify({'success': True, 'message': 'Form submitted successfully!'})
    else:
        # Render the form as the home page
        return render_template('apply_form.html')

if __name__ == '__main__':
    app.run(debug=True)
