#!/usr/bin/python
from flask import Flask, jsonify, request
import openshift_client as oc
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route(
    "ver",
    method="GET",
)
def wzo():
    if request.method == "GET":
        print("OpenShift client version: {}".format(oc.get_client_version()))
        print("OpenShift server version: {}".format(oc.get_server_version()))


@app.route("/res", methods=["GET"])
def res():
    if request.method == "GET":
        """
        data = {"ponum": 15, "lineitem": "keyboard"}
        """
        podata = {
            "OrderLines": {
                "OrderLine": {
                    "CarrierServiceCode": "UPS",
                    "ManufacturerName": "",
                    "DeliveryMethod": "SHP",
                    "RecevingNode": "",
                    "DeliveryCode": "Collect",
                    "ReqDeliveryDate": "2024-02-09",
                    "PrimeLineNo": "1",
                    "CustomerPONo": "C123456-4",
                    "Item": {
                        "CustomerItem": "",
                        "UnitOfMeasure": "EACH",
                        "ItemDesc": "Laptop 14",
                        "ManufacturerItem": "",
                        "ProductClass": "",
                        "ItemID": "Laptop 14",
                    },
                    "CarrierAccountNo": "123",
                    "CustomerLinePONo": "1",
                    "SubLineNo": "1",
                    "FillQuantity": "",
                    "SCAC": "UPS",
                    "ShipmentConsolidationGroupId": "",
                    "ItemGroupCode": "",
                    "ReqShipDate": "2024-02-20",
                    "LinePriceInfo": {"UnitPrice": "0", "IsPriceLocked": "Y"},
                    "ShipNode": "ATOS_Store",
                    "FreightTerms": "",
                    "OrderedQty": "1",
                    "LineType": "DS",
                    "FulfillmentType": "SHP",
                }
            }
        }
        return jsonify(podata)


if __name__ == "__main__":
    port = os.environ.get("FLASK_PORT") or 8080
    port = int(port)

    app.run(port=port, host="0.0.0.0")
