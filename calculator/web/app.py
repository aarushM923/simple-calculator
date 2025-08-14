from flask import Flask, render_template, request, jsonify
from calculator.engine import evaluate, CalcError

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/calc", methods=["POST"])
def api_calc():
    data = request.get_json(silent=True) or {}
    expr = (data.get("expr") or request.form.get("expr") or "").strip()
    try:
        result = evaluate(expr)
        return jsonify({"result": result})
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero"}), 400
    except CalcError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Run with: python -m calculator.web.app
    app.run(debug=True)
