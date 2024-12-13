import psycopg2
import mysql.connector

class DatabaseConnection:

    def postgresConnection(self, database):
        return psycopg2.connect(host="10.211.55.3", user="postgres", password="123456", database=database)

    def mariadbConnection(self, database):
        return mysql.connector.connect(host="localhost", user="root", password="", database=database)

    def mysqlConnection(self, database):
        return mysql.connector.connect(host="10.211.55.3", user="root", password="123456", database=database)

    def getConnection(self, type, databaseName):
        if type == 'pg':
            return self.postgresConnection(databaseName)
        elif type == 'mysql':
            return self.mysqlConnection(databaseName)
        elif type == 'mariadb':
            return self.mariadbConnection(databaseName)
        else:
            print("Database type not supported")