#!/usr/bin/python
from flask import Flask, jsonify, request

# import openshift_client as oc
import yaml
from kubernetes import client
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration
import json
import os

app = Flask(__name__)

apihost = "https://api.66a1ed2175adaf001de70e6d.ocp.techzone.ibm.com:6443"
username = "kubeadmin"
password = "Gq6Rn-moadj-K44Dw-RGE3G"
kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
kubeConfig.host = apihost


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/project", methods=["GET", "POST"])
def Services():
    buffer = {}
    if request.method == "POST":
        k8s_client = client.ApiClient(kubeConfig)
        dyn_client = DynamicClient(k8s_client)
        services = dyn_client.resources.get(api_version="v1", kind="project")

        project = """
        apiVersion: v1alpha
        kind: Project
        metadata:
        name: testDemo
        """

        service_data = yaml.load(services)
        resp = service_data.create(body=project)

        # resp is a ResourceInstance object
        buffer["resp"] = resp.metadata
        return json.dumps(buffer)


@app.route("/service", methods=["GET", "POST"])
def Services():
    buffer = {}
    if request.method == "GET":
        k8s_client = client.ApiClient(kubeConfig)
        dyn_client = DynamicClient(k8s_client)
        v1_service_list = dyn_client.resources.get(api_version="v1", kind="ServiceList")
        v1_services = v1_service_list.get()
        for service in v1_services:
            print(service.name)

        print("v1_services: {0}".format(v1_services))
        # buffer["service details"] = v1_services
        return json.dumps(buffer)


@app.route("/projects", methods=["GET"])
def getProjects():
    if request.method == "GET":

        # kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
        # kubeConfig.host = apihost
        # kubeConfig.verify_ssl = True
        # kubeConfig.ssl_ca_cert = "./ocp.pem"  # use a certificate bundle for the TLS validation
        buffer = {}
        # Retrieve the auth token
        kubeConfig.get_token()

        print("Auth token: {0}".format(kubeConfig.api_key))
        print("Token expires: {0}".format(kubeConfig.api_key_expires))

        buffer["token"] = kubeConfig.api_key
        buffer["Expires"] = kubeConfig.api_key_expires

        k8s_client = client.ApiClient(kubeConfig)

        dyn_client = DynamicClient(k8s_client)
        v1_projects = dyn_client.resources.get(
            api_version="project.openshift.io/v1", kind="Project"
        )
        project_list = v1_projects.get()
        k = 0
        for project in project_list.items:
            buffer[str(k)] = project.metadata.name
            k = k + 1

    return json.dumps(buffer)


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
