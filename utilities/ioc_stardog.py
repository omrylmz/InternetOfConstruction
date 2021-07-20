import io
import logging
import stardog
import pandas as pd
import seaborn as sns


class IoCStardog():

    def __init__(self, conn_details: dict = None, database_name: str = "") -> None:
        # TODO: Decide if we will provide default conn_details and database_name
        if conn_details is None:
            self.conn_details={
                    'endpoint': 'http://ioc.rob.arch.rwth-aachen.de',
                    'username': 'admin',
                    'password': 'admin'
                }
        else:
            self.conn_details = conn_details
        
        if database_name == "":
            self.database_name = 'IOC'
        else:
            self.database_name = database_name

        self.conn = None

    def connect(self):
        # self.conn = stardog.Connection(self.database_name, **self.conn_details)
        _ = self.__enter__()

    def __enter__(self):
        self.conn = stardog.Connection(self.database_name, **self.conn_details)
        logging.info("Valla oldu!")
        return self

    # TODO: Decide if we filter anything here?
    def query(self, query: str) -> str:
        self.conn.begin()
        return self.conn.select(query, content_type="application/sparql-results+json")

    def create_database(self, database_name: str) -> None:
        with stardog.Admin(**self.connection_details) as admin:
            if database_name in [db.name for db in admin.databases()]:
                admin.database(database_name).drop()
            db = admin.new_database(database_name)

    def add(self, file: stardog.content.File) -> None:
        self.conn.begin()
        self.conn.add(file)
        self.conn.commit()

    def close(self):
        # self.__exit()
        self.conn.__exit__()
        logging.info("Connection is closed")

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.__exit__()
        logging.info("Connection is closed")

# def main():
#     sd = IoCStardog()
#     sd.connect()
#     print("WWWWWWWWWWWWWWWWWWWWWWWWWw")

#     #GUID to search for
#     INPUT_S = "58ZF72VoHCV08vLIz1C9sy"
#     INPUT2 = "?GUID"

#     #Add "" for string
#     INPUT= """ """ + "\"" + INPUT_S + "\"" + """ """
#     #If you change between INPUT and INPUT2 in the querystring below you either search for a specific element or all elements

#     #SPARQL Query String
#     querystring = """
#     PREFIX bot: <https://w3id.org/bot#>
#     PREFIX schema: <http://schema.org/>
#     PREFIX seas:  <https://w3id.org/seas/>
#     PREFIX inst:  <https://rob.arch.rwth-aachen.de/Test01#> 
#     PREFIX props: <http://lbd.arch.rwth-aachen.de/props#>
#     PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

#     SELECT DISTINCT  ?Weight
#     WHERE {
#         ?UUID schema:value """" " + INPUT2 + " """" .
#         ?property seas:evaluation ?UUID .
#         ?Object props:uUID ?property;
#             props:weight ?propertyW;
#             a bot:Element . 
#         ?propertyW seas:evaluation ?Wnumber .
#         ?Wnumber schema:value ?Weight .
#         }
#         """ 

#     response = sd.query(querystring)
#     print(response)
#     # logging.info(sd.query(querystring))
#     # sd.close()

# if __name__ == "__main__":
#     main()
