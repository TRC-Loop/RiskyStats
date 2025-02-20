from flask import Flask, render_template, url_for
import api_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", api_list=api_response.add_player_names_to_list(api_response.top_cleaner(api_response.get_top_by())))

if __name__ == "__main__":
    app.run(debug=True)