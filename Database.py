import mysql.connector
import datetime
import time

class Database:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="hackcambridge-emotionsdatabase.mysql.database.azure.com",
            user="alice@hackcambridge-emotionsdatabase",
            passwd="C@ntilever",
            database="mydatabase",
            port=3306
        )

        self.cursor = self.db.cursor()

    def add_emotion_data(self, _time, emotions, eye_contact_dist):
        insert = "INSERT INTO emotions (time, sadness, happiness, suprise, fear, contempt, disgust, anger, neutral, nose) values (%s %f %f %f %f %f %f %f %d)"
        data = (_time, emotions['sadness'], emotions['happiness'], emotions['suprise'], emotions['fear'], emotions['contempt'], emotions['disgust'], emotions['anger'], emotions['neutral'], eye_contact_dist)
        self.cursor.execute(insert, data)
        self.db.commit()

if __name__ == "__main__":
    db = Database()



