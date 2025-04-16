from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        print("Vybraná krajina:", country)

        # TODO: neskôr sem príde reálne filtrovanie podľa krajiny
        return render_template('dashboard.html', players=[], country=country)

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
