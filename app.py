import os

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def pounds_to_kg(pounds: float) -> float:
    return pounds * 0.45359237


def calculate_bmi(weight: float, height: float, weight_unit: str = "kg", height_unit: str = "m") -> float:
    w_kg = weight if weight_unit == "kg" else pounds_to_kg(weight)
    h_m = height
    if height_unit == "cm":
        h_m = height / 100.0
    if h_m <= 0:
        raise ValueError("Height must be positive")
    return w_kg / (h_m ** 2)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal weight"
    if bmi < 30.0:
        return "Overweight"
    return "Obesity"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/bmi", methods=["POST"])
def api_bmi():
    # Accept JSON or form data
    data = request.get_json(silent=True) or request.form

    try:
        weight = float(data.get("weight", 0))
    except Exception:
        return jsonify({"error": "Invalid weight"}), 400

    weight_unit = (data.get("weight_unit") or "kg").lower()

    # height may be provided as meters or centimeters, or as feet/inches
    height_unit = (data.get("height_unit") or "m").lower()

    if height_unit == "ft":
        # expect feet and inches fields
        try:
            feet = float(data.get("feet", 0))
            inches = float(data.get("inches", 0))
            total_inches = feet * 12 + inches
            height_m = total_inches * 0.0254
        except Exception:
            return jsonify({"error": "Invalid feet/inches"}), 400
        height = height_m
        height_unit = "m"
    else:
        try:
            height = float(data.get("height", 0))
        except Exception:
            return jsonify({"error": "Invalid height"}), 400

    try:
        bmi = calculate_bmi(weight, height, weight_unit=weight_unit, height_unit=height_unit)
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    result = {
        "bmi": round(bmi, 1),
        "category": bmi_category(bmi),
    }
    return jsonify(result)


if __name__ == "__main__":
    # Use the PORT environment variable when available (Render/Heroku style)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
