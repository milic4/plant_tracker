from flask import Flask, render_template, request, redirect, url_for
from pony.orm import Database, Required, db_session
from database import  db, Plant
from collections import Counter
import json
from pony.orm import select, count, db_session


app = Flask(__name__)


@app.route("/home")
@db_session
def home():
    plants = Plant.select()[:]
    return render_template("home.html", plants=plants)


@app.route("/add", methods=["GET", "POST"])
@db_session
def add_plant():
    if request.method == "POST":
        Plant(
            naziv=request.form["naziv"],
            vrsta=request.form["vrsta"],
            potrebe_za_svjetlom=request.form["potrebe_za_svjetlom"],
            zadnje_zalijevanje=request.form["zadnje_zalijevanje"] or None,
            sljedece_zalijevanje=request.form["sljedece_zalijevanje"] or None,
            zadnja_prihrana=request.form["zadnja_prihrana"] or None,
            sljedeca_prihrana=request.form["sljedeca_prihrana"] or None,
            biljeske=request.form["biljeske"]
        )
        return redirect("/plants")
    return render_template("add_plant.html")

@app.route("/plants")
@db_session
def list_plants():
    plants = Plant.select()[:]
    print(f"--- Broj biljaka u bazi: {len(plants)} ---")
    return render_template("plants.html", plants=plants)


@app.route("/delete/<int:plant_id>", methods=["POST"])
@db_session
def delete_plant(plant_id):
    plant = Plant.get(id=plant_id)
    if plant:
        plant.delete()
    return redirect(url_for('list_plants'))

@app.route("/plant/<int:id>")
@db_session
def view_plant(id):
    plant = Plant.get(id=id)
    if not plant:
        return "Biljka nije pronađena", 404
    return render_template("plant_detail.html", plant=plant)

@app.route("/edit/<int:plant_id>", methods=["GET", "POST"])
@db_session
def edit_plant(plant_id):
    plant = Plant.get(id=plant_id)
    if request.method == "POST":
        plant.naziv = request.form["naziv"]
        plant.vrsta = request.form["vrsta"]
        plant.potrebe_za_svjetlom = request.form["potrebe_za_svjetlom"]
        plant.zadnje_zalijevanje = request.form.get("zadnje_zalijevanje") or None
        plant.sljedece_zalijevanje = request.form.get("sljedece_zalijevanje") or None
        plant.zadnja_prihrana = request.form.get("zadnja_prihrana") or None
        plant.sljedeca_prihrana = request.form.get("sljedeca_prihrana") or None
        plant.biljeske = request.form.get("biljeske") or ""
        db.commit()
        return redirect("/plants")
    return render_template("edit_plant.html", plant=plant)

@app.route("/charts")
@db_session
def charts():
    # Podaci za bar graf: broj biljaka po vrsti
    plants = Plant.select()[:]
    vrsta_counts = {}
    for plant in plants:
        vrsta_counts[plant.vrsta] = vrsta_counts.get(plant.vrsta, 0) + 1
    labels = list(vrsta_counts.keys())
    data = list(vrsta_counts.values())

    # Podaci za pie graf: potrebe za svjetlom
    svjetlo_counts = {}
    for plant in plants:
        svjetlo = plant.potrebe_za_svjetlom or "Nepoznato"
        svjetlo_counts[svjetlo] = svjetlo_counts.get(svjetlo, 0) + 1

    return render_template("charts.html", labels=labels, data=data, chart_data=svjetlo_counts)



if __name__ == "__main__":
    app.run(debug=True)
