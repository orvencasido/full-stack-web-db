from flask import Flask, jsonify
import cx_Oracle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connection details
dsn = "54.179.52.209:1521/XEPDB1"
username = "hr"
password = "hr1234"

@app.route("/api/employees")
def get_employees():
    conn = cx_Oracle.connect(username, password, dsn)
    cursor = conn.cursor()
    cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM EMPLOYEES FETCH FIRST 5 ROWS ONLY")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to JSON
    employees = [{"first_name": r[0], "last_name": r[1]} for r in rows]
    return jsonify(employees)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
