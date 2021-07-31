from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        link = request.form['link']
        describe = request.form['describe']
        ip = request.form['ip']

        print(name, email, link, describe, ip)

        try :
            mydb = mysql.connector.connect(
                host="remotemysql.com",
                database="Q8XIXWYOJU",
                user="Q8XIXWYOJU",
                password="g5vvy01OPx")


            mycursor = mydb.cursor()

            sql = "INSERT INTO links (name, email, link, description, ip) VALUES (%s, %s, %s, %s, %s)"
            val = (name, email, link, describe, ip)
            mycursor.execute(sql, val)

            mydb.commit()
            
            # print(mydb)
        except Exception as e :
            print(e)
        finally :
            mydb.close()
    return render_template('success.html')


if __name__ == '__main__':
    
    app.debug = True
    app.run()    
    
