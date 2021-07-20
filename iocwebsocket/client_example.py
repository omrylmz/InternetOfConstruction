import logging
import asyncio
from iocwebsocket.ioc_websocket_client import IoCWebSocketClient


async def main():
    client = await IoCWebSocketClient.create("ws://localhost:3000/iocws/", 5)
    await client.connect()
    # PeriodicCallback(client.keep_alive, 20000).start()
    await client.connect_to_database({
                    'endpoint': 'http://ioc.rob.arch.rwth-aachen.de',
                    'username': 'admin',
                    'password': 'admin'
                })

    # Query example
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

    response = await client.query(querystring)
    print(response)

    await client.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
