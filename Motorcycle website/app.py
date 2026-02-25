from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

#initalise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    #home page hust the ID, Maker, Model and Image URL
    sql = """   
                SELECT Bikes.BikeID,Makers.Name,Bikes.Model,Bikes.ImageURL
                FROM Bikes
                Join Makers ON Makers.MakerID=Bikes.MakerID;"""
    results = query_db(sql)
    return str(results)

@app.route("/bike/<int:id>")
def bike(id):
    #just one bike based on the id
    sql = """SELECT * FROM Bikes 
    JOIN Makers ON Makers.MakerID=Bikes.MakerID
    WHERE Bikes.BikeID = ?;"""
    result = query_db(sql,(id,),True)
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)