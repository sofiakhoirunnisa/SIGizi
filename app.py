from flask import Flask, render_template, request, redirect, session, flash
from supabase import create_client, Client
from models import Pasien

app = Flask(__name__)
app.secret_key = "secret123"

SUPABASE_URL = "https://elgwjoamyswqfkibsqtf.supabase.co"
SUPABASE_KEY = "sb_publishable_RK6ZPrh_-b8oyIri72QDjQ_aCFIz6mp"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        res = supabase.table("users") \
            .select("*") \
            .eq("username", username) \
            .eq("password", password) \
            .execute()

        if res.data:
            session["username"] = res.data[0]["username"]
            session["role"] = res.data[0]["role"]
            return redirect("/dashboard")
        else:
            flash("Login gagal! Username atau password salah.", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        role = "user"

        cek = supabase.table("users").select("id").eq("username", username).execute()

        if cek.data:
            flash("Username sudah terdaftar!", "danger")
        else:
            supabase.table("users").insert({
                "username": username,
                "password": password,
                "role": role
            }).execute()

            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/pasien")
def pasien():
    if "username" not in session:
        return redirect("/")

    res = supabase.table("pasien").select("*").order("id").execute()
    return render_template("pasien.html", data=res.data)

@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if session.get("role") != "admin":
        return redirect("/pasien")

    if request.method == "POST":
        berat = float(request.form["berat"])
        kalori = float(request.form["kalori"])

        status = Pasien.hitung_status(berat, kalori)

        data = {
            "nama": request.form["nama"],
            "umur": int(request.form["umur"]),
            "berat": berat,
            "tinggi": float(request.form["tinggi"]),
            "kebutuhan_kalori": kalori,
            "status": status
        }

        supabase.table("pasien").insert(data).execute()
        return redirect("/pasien")

    return render_template("tambah.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if session.get("role") != "admin":
        return redirect("/pasien")

    pasien = supabase.table("pasien").select("*").eq("id", id).single().execute()

    if request.method == "POST":
        berat = float(request.form["berat"])
        kalori = float(request.form["kalori"])

        status = Pasien.hitung_status(berat, kalori)

        data = {
            "nama": request.form["nama"],
            "umur": int(request.form["umur"]),
            "berat": berat,
            "tinggi": float(request.form["tinggi"]),
            "kebutuhan_kalori": kalori,
            "status": status
        }

        supabase.table("pasien").update(data).eq("id", id).execute()
        return redirect("/pasien")

    return render_template("edit.html", p=pasien.data)

@app.route("/hapus/<int:id>")
def hapus(id):
    if session.get("role") != "admin":
        return redirect("/pasien")

    supabase.table("pasien").delete().eq("id", id).execute()
    return redirect("/pasien")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
