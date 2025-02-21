from flask import Flask, render_template, jsonify
import requests
import api_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        api_list=api_response.add_player_names_to_list(
            api_response.top_cleaner(api_response.get_top_by())
        ),
    )

@app.route("/player/<uuid:uuid>")
def player(uuid):
    # If you want to pass it to your api_response.getPlayerFull(uuid), make sure to use it as a string
    player_data = api_response.getPlayerFull(
        str(uuid)
    )  # Convert the UUID to a string
    return render_template("player.html", player=player_data)

@app.route("/api/uuid/<player_name>")
def get_uuid(player_name):
    try:
        response = requests.get(
            f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return jsonify({"uuid": data["id"]})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching UUID: {e}")
        return jsonify({"error": str(e)}), 500  # Return error and 500 status

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
