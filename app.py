from flask import Flask, render_template
from flask import request , redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kunal.db"
db = SQLAlchemy(app)

class Doit(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    task = db.Column(db.String(200), nullable=False)
    action =  db.Column(db.String(20), default=False)

with app.app_context():
    db.create_all()

@app.route('/' , methods = ["GET", "POST"])
def hello_world():
    # Create a new record and add it to the database
    if request.method == 'POST':
        task = request.form['task']
        action = request.form['action']
        new_task = Doit(task=task , action = action)
        db.session.add(new_task)
        db.session.commit()
    alldata =  Doit.query.all()
    print(alldata)
    return render_template('index.html' , alldata = alldata)

@app.route('/show')
def show():
    alldata =  Doit.query.all()
    print(alldata)
    #return render_template("show.html", data=alldata)
    return 'This is Database page'  

@app.route('/delete/<int:srno>')
def delete(srno):
    todo = Doit.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:srno>' , methods =  ['GET', 'POST'])
def update(srno):
    if request.method == "POST":
        task = request.form['task']
        action = request.form['action']
        alldata = Doit.query.filter_by(srno=srno).first()
        alldata.task = task
        alldata.action = action
        db.session.add(alldata)
        db.session.commit()
        return redirect("/")
    alldata = Doit.query.filter_by(srno=srno).first()
    return render_template('update.html', alldata=alldata)
    
       

if __name__ == "__main__":
    app.run(debug=True, port=8000)
