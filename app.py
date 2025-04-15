from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # TODO: spracovanie formulára
        return render_template('dashboard.html', players=[])
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)