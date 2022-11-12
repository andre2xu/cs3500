import os
from flask import Flask, render_template

app = Flask(
    import_name = __name__,
    template_folder = os.path.dirname(__file__) + '/static/html'
)



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)