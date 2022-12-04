from client import fountain_object
from flask import Flask, render_template, redirect
from glass import Glass

import json
import os
import random
app = Flask(__name__)

glasses = {}

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/droplet")
def droplet():
    return fountain_object.droplet().toString()

@app.route("/droplet/<amt>")
def droplets(amt):
    amt = int(amt)
    out = []
    for x in range(amt):
        out.append(fountain_object.droplet().toString())
    return json.dumps(out)

@app.route("/glass")
def pickGlass():
    return redirect("/glass/%d" % random.randint(0,2**15-1))

@app.route("/aboutus")
def foraboutus():
    return render_template("/aboutus.html")

@app.route("/glass/<id>")
def glass(id):
    id = int(id)
    glass_Object = getGlass(id)
    # message = "%d of %d chunks reconstructed." % (glass_Object.chunksReceived(), glass_Object.total_chunks)
    chunksCreated=glass_Object.chunksReceived()
    total_chunks=glass_Object.total_chunks
    return render_template('glass.html',
        num_droplets=len(glass_Object.droplets),
        source="/droplet",
        text=glass_Object.getString(),
        id=id,
        droplets=[d for d in glass_Object.droplets],
        chunksCreated=chunksCreated,
        total_chunks=total_chunks
        )

@app.route("/glass/<id>/fill")
def fill(id):
    return fillAmt(id, 1)

@app.route("/glass/<id>/fill/<amt>")
def fillAmt(id, amt):
    id = int(id)
    amt = int(amt)

    glass_Object = getGlass(id)
    for i in range(amt):
        glass_Object.addDroplet(fountain_object.droplet())
    return redirect("/glass/%d" % id)

def getGlass(id):
    id = int(id)
    glass_Object = None
    if id not in glasses:
        glass_Object = Glass(fountain_object.total_chunks)
        glasses[id] = glass_Object
    return glasses[id]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
