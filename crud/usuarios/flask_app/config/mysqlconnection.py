# un cursor es el objeto que usamos para interactuar con la base de datos
import pymysql.cursors


class MySQLConnection:
    def __init__(self, db): 
        connection = pymysql.connect(host = 'localhost', # Con esto creamos la conexión a MySQL
                                    user = 'root', # change the user and password as needed
                                    password = 'rootapalm811*', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection

        
    # el método para consultar la base de datos
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor: # Un cursor es un acceso a la base de datos. Debo pedirle a la conexión un cursor
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                # Con la siguiente sentencia, ejecuto una consulta SQL. Aca los resultados quedan guardados en cursor
                # executable = 
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # if the query is an insert, return the id of the last row, since that is the row we just added
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # if the query is a select, return everything that is fetched from the database
                    # the result will be a list of dictionaries
                    result = cursor.fetchall()    # Acá pido los datos al cursos
                    return result
                else:
                    # if the query is not an insert or a select, such as an update or delete, commit the changes
                    # return nothing
                    self.connection.commit()
            except Exception as e:
                # in case the query fails
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# this connectToMySQL function creates an instance of MySQLConnection, which will be used by server.py
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)