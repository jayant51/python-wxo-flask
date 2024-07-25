from kubernetes import client
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration

apihost = "https://api.669ac50b158155001ef90009.ocp.techzone.ibm.com:6443"
username = "kubeadmin"
password = "pwzSX-33xUi-JECMU-7Re7H"

kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
kubeConfig.host = apihost
kubeConfig.verify_ssl = True
# kubeConfig.ssl_ca_cert = "./ocp.pem"  # use a certificate bundle for the TLS validation

# Retrieve the auth token
kubeConfig.get_token()

print("Auth token: {0}".format(kubeConfig.api_key))
print("Token expires: {0}".format(kubeConfig.api_key_expires))

k8s_client = client.ApiClient(kubeConfig)

dyn_client = DynamicClient(k8s_client)
v1_projects = dyn_client.resources.get(
    api_version="project.openshift.io/v1", kind="Project"
)
project_list = v1_projects.get()

for project in project_list.items:
    print(project.metadata.name)
