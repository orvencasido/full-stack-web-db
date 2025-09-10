from flask import Flask, jsonify
import cx_Oracle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connection details
dsn = "oracle-xe:1521/XEPDB1"
username = "hr"
password = "hr1234"

@app.route("/api/employees")
def get_employees():
    conn = cx_Oracle.connect(username, password, dsn)
    cursor = conn.cursor()
    cursor.execute("SELECT FIRST_NAME, LAST_NAME, EMPLOYEE_ID FROM EMPLOYEES FETCH FIRST 5 ROWS ONLY")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to JSON
    employees = [
        {"employee_id": r[2], "first_name": r[0], "last_name": r[1]}
        for r in rows
    ]
    return jsonify(employees)

@app.route("/api/update_employee", methods=["POST"])
def update_employee():
    data = request.json  
    emp_id = data.get("employee_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    conn = cx_Oracle.connect(username, password, dsn)
    cursor = conn.cursor()
    
    sql = "UPDATE EMPLOYEES SET FIRST_NAME = :fn, LAST_NAME = :ln WHERE EMPLOYEE_ID = :id"
    cursor.execute(sql, fn=first_name, ln=last_name, id=emp_id)
    conn.commit()  # IMPORTANT: commit changes
    
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success", "employee_id": emp_id, "first_name": first_name, "last_name": last_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
