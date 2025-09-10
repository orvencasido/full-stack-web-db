from flask import Flask, jsonify, request
import cx_Oracle
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

# Connection details
dsn = "oracle-xe:1521/XEPDB1"
username = "hr"
password = "hr1234"


@app.route("/api/employees")
def get_employees():
    conn = cx_Oracle.connect(username, password, dsn)
    cursor = conn.cursor()
    cursor.execute("SELECT FIRST_NAME, LAST_NAME, EMPLOYEE_ID FROM EMPLOYEES")
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
    try:
        data = request.get_json()
        emp_id = data.get("employee_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        conn = cx_Oracle.connect(username, password, dsn)
        cursor = conn.cursor()
        sql = "UPDATE EMPLOYEES SET FIRST_NAME = :fn, LAST_NAME = :ln WHERE EMPLOYEE_ID = :id"
        cursor.execute(sql, fn=first_name, ln=last_name, id=emp_id)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "employee_id": emp_id, "first_name": first_name, "last_name": last_name})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/insert_employee", methods=["POST"])
def insert_employee():
    try:
        data = request.get_json()
        emp_id = data.get("employee_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email") or f"{first_name.lower()}.{last_name.lower()}@example.com"
        hire_date = data.get("hire_date") or "01-01-2025"  # default date if not provided
        job_id = data.get("job_id") or "IT_PROG"           # default job_id to satisfy FK

        conn = cx_Oracle.connect(username, password, dsn)
        cursor = conn.cursor()

        sql = """
            INSERT INTO EMPLOYEES 
            (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, HIRE_DATE, JOB_ID)
            VALUES (:id, :fn, :ln, :email, TO_DATE(:hire_date, 'DD-MM-YYYY'), :job_id)
        """
        cursor.execute(sql, id=emp_id, fn=first_name, ln=last_name, email=email, hire_date=hire_date, job_id=job_id)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "employee_id": emp_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "hire_date": hire_date,
            "job_id": job_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/delete_employee", methods=["POST"])
def delete_employee():
    try:
        data = request.get_json()
        emp_id = data.get("employee_id")

        conn = cx_Oracle.connect(username, password, dsn)
        cursor = conn.cursor()
        sql = "DELETE FROM EMPLOYEES WHERE EMPLOYEE_ID = :id"
        cursor.execute(sql, id=emp_id)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "employee_id": emp_id})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
