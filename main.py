from flask import Flask, render_template

app = Flask("Cool-blogs")


@app.route('/')
def home_page():
    return render_template("base.html", title="Дом")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')