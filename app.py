from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    # Pass data directly into the HTML template
    user_info = {"name": "Developer", "status": "Learning Flask"}
    return render_template('index.html', data=user_info)

# Route that accepts dynamic parameters in the URL
@app.route('/user/<username>')
def show_user_profile(username):
    return f"Profile page for user: {username}"

if __name__ == '__main__':
    # Run the local development server
    app.run(debug=True, port=5001)
