from database.DB_connect import DBConnect
from model.avvistamento import Avvistamento
from model.stato import Stato


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_avvistamenti():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, shape, s_datetime, state FROM sighting """

        cursor.execute(query)
        result = []
        for row in cursor:

            result.append(Avvistamento(row["id"], row["shape"], row["s_datetime"].year, row["state"]))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def get_stati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state"""

        cursor.execute(query)

        for row in cursor:
            vicini = row["neighbors"]
            vicini_lower = []
            if vicini is not None:
                vicini = vicini.strip().split()
                for vicino in vicini:
                    if vicino.lower() != row["id"].lower():
                        vicini_lower.append(vicino.lower())
            else:
                vicini_lower = []
            result.append(Stato(row["id"].lower(), row["name"], row["capital"], row["lat"], row["lng"], row["area"], row["population"], vicini_lower))

        cursor.close()
        conn.close()
        return result