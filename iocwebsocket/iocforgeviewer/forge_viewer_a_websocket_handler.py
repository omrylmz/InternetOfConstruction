import logging
import tornado.websocket

class ForgeViewerAWebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")

        #Setup connection details
        conn_details = {
        'endpoint': 'http://ioc.rob.arch.rwth-aachen.de',
        'username': 'admin',
        'password': 'admin'
        }

        #GUID to search for
        INPUT_S = "58ZF72VoHCV08vLIz1C9sy"
        INPUT2 = "?GUID"

        #Add "" for string
        INPUT= """ """ + "\"" + INPUT_S + "\"" + """ """
        #If you change between INPUT and INPUT2 in the querystring below you either search for a specific element or all elements

        #SPARQL Query String
        querystring = """
        PREFIX bot: <https://w3id.org/bot#>
        PREFIX schema: <http://schema.org/>
        PREFIX seas:  <https://w3id.org/seas/>
        PREFIX inst:  <https://rob.arch.rwth-aachen.de/Test01#> 
        PREFIX props: <http://lbd.arch.rwth-aachen.de/props#>
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT  ?Weight
        WHERE {
            ?UUID schema:value """" " + INPUT2 + " """" .
            ?property seas:evaluation ?UUID .
            ?Object props:uUID ?property;
                props:weight ?propertyW;
                a bot:Element . 
            ?propertyW seas:evaluation ?Wnumber .
            ?Wnumber schema:value ?Weight .
            }
            """ 
            
        #Print how query looks in the end            
        print (querystring)

        #Send query to triple store 
        with stardog.Connection('IOC', **conn_details) as conn:
            conn.begin()
            data = conn.select(querystring, content_type="application/sparql-results+json")
            
        #Print Json
        print(data)

        #Get Value for weight
        for i in range (len(data['results']['bindings'])):
            weight = (data['results']['bindings'][i]['Weight']['value'])    
            print ("Element has a weight of " +weight+ " Kilograms")

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        # logging.info("message: {}".format(message))
        self.write_message("OMER")