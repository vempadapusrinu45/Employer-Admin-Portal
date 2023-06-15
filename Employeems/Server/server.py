import tornado.ioloop
import tornado.web
import pymysql
import bcrypt
import jwt
import os

# Create a Tornado application
class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        # Initialize the database connection
        self.db = pymysql.connect(host="localhost", user="root", password="123456789", database="signup")
        self.cursor = self.db.cursor()

    def prepare(self):
        # Prepare the request by setting headers and content type
        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.write("Hello, World!")

class EmployeeHandler(tornado.web.RequestHandler):
    def initialize(self):
    
        self.db = pymysql.connect(host="localhost", user="root", password="123456789", database="signup")
        self.cursor = self.db.cursor()

    def prepare(self):

        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")

    def get(self):
        # Handle GET requests to retrieve all employees
        sql = "SELECT * FROM employee"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.write({"Status": "Success", "Result": result})
        except Exception as e:
            self.write({"Error": "Get employee error in sql"})

    def get_employee(self, id):
        # Handle GET requests to retrieve an employee by ID
        sql = "SELECT * FROM employee WHERE id = %s"
        try:
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchall()
            self.write({"Status": "Success", "Result": result})
        except Exception as e:
            self.write({"Error": "Get employee error in sql"})

    def put(self, id):
        # Handle PUT requests to update an employee's salary by ID
        salary = self.get_argument("salary")
        sql = "UPDATE employee SET salary = %s WHERE id = %s"
        try:
            self.cursor.execute(sql, (salary, id))
            self.db.commit()
            self.write({"Status": "Success"})
        except Exception as e:
            self.write({"Error": "Update employee error in sql"})

    def delete(self, id):
        # Handle DELETE requests to delete an employee by ID
        sql = "DELETE FROM employee WHERE id = %s"
        try:
            self.cursor.execute(sql, (id,))
            self.db.commit()
            self.write({"Status": "Success"})
        except Exception as e:
            self.write({"Error": "Delete employee error in sql"})
class LoginHandler(tornado.web.RequestHandler):
    def initialize(self):
        # Initialize the database connection
        self.db = pymysql.connect(host="localhost", user="root", password="", database="signup")
        self.cursor = self.db.cursor()

    def prepare(self):
        # Prepare the request by setting headers and content type
        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")

    def post(self):
        # Handle POST requests for user login
        email = self.get_argument("email")
        password = self.get_argument("password")
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        try:
            self.cursor.execute(sql, (email, password))
            result = self.cursor.fetchall()
            if len(result) > 0:
                id = result[0][0]
                token = jwt.encode({"role": "admin"}, "jwt-secret-key", algorithm="HS256")
                self.set_cookie("token", token)
                self.write({"Status": "Success"})
            else:
                self.write({"Status": "Error", "Error": "Wrong Email or Password"})
        except Exception as e:
            self.write({"Status": "Error", "Error": "Error in running query"})

class EmployeeLoginHandler(tornado.web.RequestHandler):
    def initialize(self):
        # Initialize the database connection
        self.db = pymysql.connect(host="localhost", user="root", password="", database="signup")
        self.cursor = self.db.cursor()

    def prepare(self):
        # Prepare the request by setting headers and content type
        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")

    def post(self):
        # Handle POST requests for employee login
        email = self.get_argument("email")
        password = self.get_argument("password")
        sql = "SELECT * FROM employee WHERE email = %s"
        try:
            self.cursor.execute(sql, (email,))
            result = self.cursor.fetchall()
            if len(result) > 0:
                hashed_password = result[0][2]
                if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                    id = result[0][0]
                    token = jwt.encode({"role": "employee", "id": id}, "jwt-secret-key", algorithm="HS256")
                    self.set_cookie("token", token)
                    self.write({"Status": "Success", "id": id})
                else:
                    self.write({"Status": "Error", "Error": "Wrong Email or Password"})
            else:
                self.write({"Status": "Error", "Error": "Wrong Email or Password"})
        except Exception as e:
            self.write({"Status": "Error", "Error": "Error in running query"})
class LogoutHandler(tornado.web.RequestHandler):
    def prepare(self):
        # Prepare the request by setting headers and content type
        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")

    def get(self):
        # Handle GET requests for user logout
        self.clear_cookie("token")
        self.write({"Status": "Success"})

class CreateHandler(tornado.web.RequestHandler):
    def initialize(self):
        # Initialize the database connection
        self.db = pymysql.connect(host="localhost", user="root", password="123456789", database="signup")
        self.cursor = self.db.cursor()

    def prepare(self):
        # Prepare the request by setting headers and content type
        self.set_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")

    def post(self):
        # Handle POST requests to create an employee
        name = self.get_argument("name")
        email = self.get_argument("email")
        password = self.get_argument("password")
        address = self.get_argument("address")
        salary = self.get_argument("salary")
        image = self.request.files["image"][0]
        filename = image["filename"]

        # Save the uploaded image
        upload_path = os.path.join(os.path.dirname(__file__), "public/images", filename)
        with open(upload_path, "wb") as f:
            f.write(image["body"])

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert the employee data into the database
        sql = "INSERT INTO employee (`name`, `email`, `password`, `address`, `salary`, `image`) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (name, email, hashed_password, address, salary, filename))
            self.db.commit()
            self.write({"Status": "Success"})
        except Exception as e:
            self.write({"Error": "Error in signup query"})

# Create a Tornado application with routes
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/getEmployee", EmployeeHandler),
        (r"/get/([0-9]+)", EmployeeHandler),
        (r"/update/([0-9]+)", EmployeeHandler),
        (r"/delete/([0-9]+)", EmployeeHandler),
        (r"/login", LoginHandler),
        (r"/employeelogin", EmployeeLoginHandler),
        (r"/logout", LogoutHandler),
        (r"/create", CreateHandler),
    ])
if __name__ == "__main__":
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="signup"
    )

    con.connect(callback=lambda: print("Connected to MySQL"))

    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8081)
    print("Tornado server is running")
    tornado.ioloop.IOLoop.current().start()