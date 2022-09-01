import mysql.connector as conn

mydb = conn.connect(host="localhost", user="root", passwd="password")
cursor = mydb.cursor()

# cursor.execute("create database gunjan")
# cursor.execute("show databases")
# cursor.execute("create table gunjan.details(employee_id int(10),
# employee_name varchar(80), emp_mailid varchar(20), emp_salary int(6), emp_attendance int(2) )")

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/insert_record_mysql', methods=['GET', 'POST'])
def insertINTO_sql():
    if(request.method=='POST'):
        # cursor.execute("insert into gunjan.details values(101, 'Gunjan Varde', 'xyz@gmail.com', 200, 25)")
        cursor.execute("insert into " + str(request.json["DB_Name"]) + "." +
                       str(request.json["Table_Name"]) +
                       " values(" + str(request.json["EMP_ID"]) +
                       ", " + "'" + str(request.json["EMP_Name"]) + "'" + ", " + "'" +
                       str(request.json["EMAIL"]) + "'" + ", " + str(request.json["SALARY"]) +
                       ", " + str(request.json["Attendance"]) + " )")
        mydb.commit()
        return jsonify((str("Values has been inserted successfully!")))


@app.route('/update_record_mysql', methods=['GET', 'POST'])
def update_value():
    if(request.method=='POST'):
        # cursor.execute("update gunjan.details set emp_attendance = 25 where emp_attendance = 5")
        cursor.execute("update " + str(request.json["DB_Name"]) + "." + str(request.json["Table_Name"]) +
                       " set emp_attendance = " + str(request.json["Updated_Attendance"]) +
                       " where emp_attendance = " + str(request.json["Attendance"]) )
        mydb.commit()
        return jsonify((str("Values has been updated successfully!")))

@app.route('/delete_record_mysql', methods=['GET', 'POST'])
def delete_row():
    if(request.method=='POST'):
        # cursor.execute("delete from gunjan.details where employee_name = 'Gunjan Varde'")
        cursor.execute("delete from " + str(request.json["DB_Name"]) + "." +
                       str(request.json["Table_Name"]) + " where employee_name = '" +
                       str(request.json["EMP_Name"]) + "'")
        mydb.commit()
        return jsonify((str("Values has been deleted successfully!")))

@app.route('/fetch_record_mysql', methods=['GET', 'POST'])
def fetch_records():
    if(request.method=='POST'):
        # cursor.execute("select * from gunjan.details")
        cursor.execute("select * from " +
                       str(request.json["DB_Name"]) + "." +
                       str(request.json["Table_Name"]))
        l = []
        for i in cursor.fetchall():
            l.append(i)
        return jsonify(l)


# cursor.execute("insert into gunjan.details values(101, 'VARDE GUNJAN', 'ABC@gmail.com', 200, 15)")
# mydb.commit()

import pymongo
client = pymongo.MongoClient("mongodb+srv://<username:password>@cluster0.2esukot.mongodb.net/?retryWrites=true&w=majority")
db = client.test


@app.route('/insert_record_mongodb', methods=['GET', 'POST'])
def insert_mongodb():
    if(request.method=='POST'):
        data = {
            "name": request.json["emp_name"],
            "email": request.json["mailid"],
            "surname": request.json["sirname"],
            "subject": request.json["subject_list"]
        }

        database = client[request.json["DB_Name"]]
        collection = database[request.json["Table_Name"]]
        collection.insert_one(data)

        all_records = collection.find()
        record = []
        for i in all_records:
            record.append(i)
        return jsonify((str(record)))

        # return jsonify((str("Record has been inserted successfully in MongoDB!")))


@app.route('/update_record_mongodb', methods=['GET', 'POST'])
def update_mongodb():
    if(request.method=='POST'):
        database = client[request.json["DB_Name"]]
        collection = database[request.json["Table_Name"]]
        collection.update_one({'name': request.json["emp_name"]},
                              {'$set': {'name': request.json["updated_emp_name"]}})
        collection.update_one({'subject': request.json["subject_list"]},
                              {'$set': {'subject': request.json["updated_subject_list"]}})

        record = []
        for i in collection.find():
            record.append(i)
        return jsonify((str(record)))

        # return jsonify((str("Values has been updated successfully in MongoDB!")))


@app.route('/delete_record_mongodb', methods=['GET', 'POST'])
def delete_mongodb():
    if(request.method=='POST'):
        database = client[request.json["DB_Name"]]
        collection = database[request.json["Table_Name"]]
        collection.delete_one({'name': request.json["emp_name"]})

        record = []
        for i in collection.find():
            record.append(i)
        return jsonify((str(record)))

        # return jsonify((str("record has been deleted successfully in MongoDB!")))


@app.route('/fetch_record_mongodb', methods=['GET', 'POST'])
def fetch_mongodb():
    if(request.method=='POST'):
        database = client[request.json["DB_Name"]]
        collection = database[request.json["Table_Name"]]

        fetch_all_record = []
        for i in collection.find():
            fetch_all_record.append(i)
        return jsonify((str(fetch_all_record)))

        # return jsonify((str("All records has been fetched successfully from MongoDB!")))


if __name__=='__main__':
    app.run()