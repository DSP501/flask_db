from flask import Flask, render_template, request
import mysql.connector
from decouple import config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return render_template('account_auth.html')


@app.route('/account', methods=['POST'])
def account():

    email = request.form['email']
    password = request.form['password']

    if email != config('ADMIN_ID') and password != config('ADMIN_PASS'):
        return auth()


    head = ''' <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <!-- CSS only -->

            <script type="text/javascript" src="https://unpkg.com/xlsx@0.15.1/dist/xlsx.full.min.js"></script>



            
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
                integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
                crossorigin="anonymous"></script>
            </head> '''

    body = ''' <body>
        <div class="container">
        <div class="">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="/">Link</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item ">
                <a class="nav-link" href="/">Home </a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="/auth">Admin</a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="#" onclick="ExportToExcel('xlsx')">Export Data</a>
                </li>
            </ul>
            </div>
        </nav>
        </div>

        <table class="table" id="result">
            <thead>
            <tr>
                <th scope="col">Link</th>
                <th scope="col">Description</th>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">IP</th>
                <th scope="col">Date</th>
            </tr>
            </thead>'''

    end = '''</tbody></table>
        </div></body>

        <script>
  
            function ExportToExcel(type, fn, dl) {
                var elt = document.getElementById('result');
                var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
                return dl ?
                    XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
                    XLSX.writeFile(wb, fn || ('LinkDatabase.' + (type || 'xlsx')));
            }
        </script>



        
        </html>'''

    try:
        mydb = mysql.connector.connect(
            host=config('HOST'),
            database=config('DATABASE_NAME'),
            user=config('USER_ID'),
            password=config('PASSWORD'))

        mycursor = mydb.cursor()

        sql = "SELECT link, description, name, email, ip, date FROM links"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        final_string = ""

        for r in result:
            print(r)
            final_string += "<tr>"
            for index, data in enumerate(r):
                if index == 0:
                    final_string += "<td>" + "<a href=' " + \
                        str(data) + " '> " + str(data) + "</td></a>"
                elif index == 3:
                    final_string += "<td>" + "<a href='mailto: " + \
                        str(data) + " '> " + str(data) + "</td></a>"
                elif index == 4:
                    final_string += "<td>" + "<a href=' " + 'https://www.ip2location.com/demo/' + \
                        str(data) + " ' target='blank'> " + \
                        str(data) + "</td></a>"
                else:
                    final_string += "<td>" + str(data) + "</td>"
            final_string += "</tr>"

        # print(head + final_string)

    except Exception as e:
        final_string += "Database Server Error Pl Try Later"
        print(e)
    finally:
        # mydb.close()
        pass

    # return render_template('account.html', data=final_string)
    return head + body + final_string + end


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        link = request.form['link']
        describe = request.form['describe']
        ip = request.form['ip']

        print(name, email, link, describe, ip)

        try:
            mydb = mysql.connector.connect(
                host=config('HOST'),
                database=config('DATABASE_NAME'),
                user=config('USER_ID'),
                password=config('PASSWORD'))

            mycursor = mydb.cursor()

            sql = "INSERT INTO links (name, email, link, description, ip) VALUES (%s, %s, %s, %s, %s)"
            val = (name, email, link, describe, ip)
            mycursor.execute(sql, val)

            mydb.commit()

            # print(mydb)
        except Exception as e:
            print(e)
        finally:
            mydb.close()
    return render_template('success.html')


if __name__ == '__main__':

    app.debug = True
    app.run()
