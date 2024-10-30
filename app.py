from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters for Supabase
hostname = "aws-0-ap-southeast-1.pooler.supabase.com"
database = "postgres"
port = "6543"
username = "postgres.wznglqsbzzejpfwhesmw"
password = "M@langPost11"  # Pastikan password tidak diubah dan sesuai


def get_db_connection():
    conn = psycopg2.connect(
        database=database, user=username, password=password, host=hostname, port=port
    )
    return conn


@app.route("/", methods=["GET"])
def dashboard():
    return render_template("index.html")


@app.route("/bugs", methods=["GET"])
def get_bugs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bug_management.bugs ORDER BY id ASC;"  # Mengurutkan berdasarkan ID secara ascending
    )
    bugs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(bugs)


@app.route("/bug/<int:bug_id>", methods=["GET"])
def get_bug_details(bug_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bug_management.bugs WHERE id = %s;", (bug_id,))
    bug = cursor.fetchone()
    cursor.close()
    conn.close()

    if bug:
        bug_detail = {
            "id": bug[0],
            "date_reported": bug[1],
            "platform": bug[2],
            "session": bug[3] if bug[3] else "N/A",
            "checking_by_developer": bug[4] if bug[4] else "N/A",
            "note": bug[5] if bug[5] else "N/A",
            "issue": bug[6],
            "summary": bug[7],
            "reported_by": bug[8],
            "expectation": bug[9] if bug[9] else "N/A",
            "priority": bug[10] if bug[10] else "N/A",
            "evidence_status": bug[11] if bug[11] else "N/A",
            "retest_bug": bug[12] if bug[12] else "N/A",
            "created_at": bug[13],
            "updated_at": bug[14],
            "status": bug[15] if bug[15] else "N/A",
        }
        return jsonify(bug_detail)
    else:
        return jsonify({"error": "Bug not found"}), 404


# Perbarui route add_bug agar mendukung project_id
@app.route("/bugs", methods=["POST"])
def add_bug():
    try:
        new_bug = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bug_management.bugs (platform, session, checking_by_developer, note, issue, 
                summary, reported_by, expectation, priority, evidence_status, retest_bug, status, project_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                new_bug["platform"],
                new_bug["session"],
                new_bug["checking_by_developer"],
                new_bug["note"],
                new_bug["issue"],
                new_bug["summary"],
                new_bug["reported_by"],
                new_bug["expectation"],
                new_bug["priority"],
                new_bug["evidence_status"],
                new_bug["retest_bug"],
                new_bug["status"],
                new_bug["project_id"],
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(new_bug), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/bug/<int:bug_id>", methods=["PUT"])
def update_bug(bug_id):
    try:
        updated_bug = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE bug_management.bugs
            SET platform = %s, session = %s, checking_by_developer = %s, note = %s, issue = %s, 
                summary = %s, reported_by = %s, expectation = %s, priority = %s, evidence_status = %s, 
                retest_bug = %s, status = %s
            WHERE id = %s;
            """,
            (
                updated_bug["platform"],
                updated_bug["session"],
                updated_bug["checking_by_developer"],
                updated_bug["note"],
                updated_bug["issue"],
                updated_bug["summary"],
                updated_bug["reported_by"],
                updated_bug["expectation"],
                updated_bug["priority"],
                updated_bug["evidence_status"],
                updated_bug["retest_bug"],
                updated_bug["status"],
                bug_id,
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(updated_bug), 200
    except Exception as e:
        return (
            jsonify({"error": str(e)}),
            400,
        )


@app.route("/add-bug", methods=["GET"])
def add_bug_page():
    return render_template("add_bug.html")


@app.route("/create-project")
def create_project():
    return render_template("create_project.html")  # File form Create Project


@app.route("/projects", methods=["POST"])
def add_project():
    try:
        # Mengambil data proyek dari request JSON
        new_project = request.json

        # Koneksi ke database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Menyimpan data proyek ke database
        cursor.execute(
            """
            INSERT INTO bug_management.projects (name, description)
            VALUES (%s, %s);
            """,
            (
                new_project["name"],
                new_project.get(
                    "description", ""
                ),  # Menggunakan get untuk default jika description tidak ada
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return (
            jsonify(new_project),
            201,
        )  # Mengembalikan data proyek yang ditambahkan dengan status 201 Created
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Mengembalikan error jika terjadi


@app.route("/projects", methods=["GET"])
def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM bug_management.projects;")
        projects = cursor.fetchall()
        cursor.close()
        conn.close()

        # Ubah data menjadi list of dict agar mudah digunakan di frontend
        project_list = [{"id": row[0], "name": row[1]} for row in projects]
        return jsonify(project_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
