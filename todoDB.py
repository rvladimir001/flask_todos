import time
import math
import sqlite3

class todoDB:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        
    def getTodos(self):
        sql = "SELECT * FROM todos"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД1")
        return []
    
    def getTodo(self, id):
        sql = "SELECT * FROM todos WHERE id = {}".format(id)
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res: return res
        except:
            print("Ошибка чтения из БД2")
        return []
    
    def addTodo(self, todo, status):
        try:
            tm = math.floor(time.time())
            created_on = tm
            updated_on = tm
            self.__cur.execute("INSERT INTO todos VALUES(NULL, ? , ?, ?, ?)", (todo, status, created_on, updated_on))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД: " + str(e))
            return False
        return True
    
    def updateTodo(self, todo, status, id):
        try:
            updated_on = math.floor(time.time())
            self.__cur.execute("UPDATE todos SET todo = {}, status = {}, updated_on = {} WHERE id = {}".format(todo, status, updated_on, id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД: " + str(e))
            return False
        return True