# Dependancies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    all_of_mars = mongo.db.all_of_mars.find_one()
    return render_template("index.html", all_of_mars=all_of_mars)

@app.route("/scrape")
def scraper():
    all_of_mars = mongo.db.all_of_mars
    all_of_mars_data = scrape_mars.scrape()
    all_of_mars.update({}, all_of_mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)    
