from flask import Flask, jsonify, render_template,request

app = Flask(__name__)

beds = {
    101: {
        "patient": "Patient A",
        "fluid_remaining": 100,
        "status": "NORMAL"
    },
    102: {
        "patient": "Patient B",
        "fluid_remaining": 100,
        "status": "NORMAL"
    },
    103: {
        "patient": "Patient C",
        "fluid_remaining": 100,
        "status": "NORMAL"
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api_home():
    return jsonify({
        "project": "IV Fluid Monitoring and Alarm System",
        "message": "Backend is running!",
        "mode": "SIMULATION ONLY"
    })


@app.route("/api/beds")
def get_beds():
    return jsonify(beds)


@app.route("/api/bed/<int:bed_id>")
def get_bed(bed_id):
    bed = beds.get(bed_id)

    if bed is None:
        return jsonify({"error": "Bed not found"}), 404

    return jsonify(bed)
@app.route("/api/bed/<int:bed_id>/status", methods=["POST"])
def update_bed_status(bed_id):
    bed = beds.get(bed_id)

    if bed is None:
        return jsonify({"error": "Bed not found"}), 404

    data = request.get_json(silent=True) or {}
    status = data.get("status", "").upper()

    allowed_statuses = ["NORMAL", "LOW", "CRITICAL", "NO FLOW"]

    if status not in allowed_statuses:
        return jsonify({"error": "Invalid status"}), 400

    bed["status"] = status

    if status == "NORMAL":
        bed["fluid_remaining"] = 100
    elif status == "LOW":
        bed["fluid_remaining"] = 25
    elif status == "CRITICAL":
        bed["fluid_remaining"] = 10

    return jsonify({
        "message": "Simulation status updated",
        "bed": bed_id,
        "data": bed
    })
if __name__ == "__main__":
app.run(host="ivfluidmonitoring", port=5000, debug=False)
