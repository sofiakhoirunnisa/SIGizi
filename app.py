from flask import Flask, render_template, request, redirect, session, flash
from supabase import create_client, Client
from models import Pasien
from werkzeug.security import generate_password_hash

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
        res = supabase.table("users").select("*").eq("username", username).execute()
        if res.data and password == res.data[0]["password"]:
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
            password_hash = generate_password_hash(password)
            supabase.table("users").insert({
                "username": username,
                "password": password_hash,
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
        flash("Hanya admin yang bisa menambahkan pasien.", "danger")
        return redirect("/pasien")

    if request.method == "POST":
        try:
            nama = request.form["nama"].strip()
            umur = int(request.form["umur"])
            berat = float(request.form["berat"])
            tinggi = float(request.form["tinggi"])
            kalori = float(request.form["kalori"])
            status = Pasien.hitung_status(berat, kalori) or "aktif"

            data = {
                "nama": nama,
                "umur": umur,
                "berat": berat,
                "tinggi": tinggi,
                "kebutuhan_kalori": kalori,
                "status": status
            }
            supabase.table("pasien").insert(data).execute()
            flash("Data pasien berhasil ditambahkan.", "success")
            return redirect("/pasien")
        except Exception as e:
            flash(f"Gagal menambahkan pasien: {e}", "danger")
            return redirect("/tambah")

    return render_template("tambah.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if session.get("role") != "admin":
        flash("Hanya admin yang bisa mengedit pasien.", "danger")
        return redirect("/pasien")

    pasien_res = supabase.table("pasien").select("*").eq("id", id).single().execute()
    if not pasien_res.data:
        flash("Pasien tidak ditemukan.", "danger")
        return redirect("/pasien")

    pasien_data = pasien_res.data

    if request.method == "POST":
        try:
            nama = request.form["nama"].strip()
            umur = int(request.form["umur"])
            berat = float(request.form["berat"])
            tinggi = float(request.form["tinggi"])
            kalori = float(request.form["kalori"])
            status = Pasien.hitung_status(berat, kalori) or "aktif"

            data = {
                "nama": nama,
                "umur": umur,
                "berat": berat,
                "tinggi": tinggi,
                "kebutuhan_kalori": kalori,
                "status": status
            }
            supabase.table("pasien").update(data).eq("id", id).execute()
            flash("Data pasien berhasil diperbarui.", "success")
            return redirect("/pasien")
        except Exception as e:
            flash(f"Gagal mengedit pasien: {e}", "danger")
            return redirect(f"/edit/{id}")

    return render_template("edit.html", p=pasien_data)

@app.route("/hapus/<int:id>")
def hapus(id):
    if session.get("role") != "admin":
        flash("Hanya admin yang bisa menghapus pasien.", "danger")
        return redirect("/pasien")
    try:
        supabase.table("pasien").delete().eq("id", id).execute()
        flash("Data pasien berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus pasien: {e}", "danger")
    return redirect("/pasien")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
