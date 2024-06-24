import requests
from patient import create_patient_resource


# Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource,resource_type):
    url = f"http://hapi.fhir.org/baseR4/{resource_type}"
    headers = {"Content-Type": "application/fhir+json"}
    resource_json = resource.json()

    response = requests.post(url, headers=headers, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")
        
        # Devolver el ID del recurso creado
        return response.json()['id']
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar el recurso por ID 
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"http://hapi.fhir.org/baseR4/{resource_type}/{resource_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        resource = response.json()
        print(resource)
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())

def get_snomedct_code(procedure_name):

    terminology_server_url = "https://r4.ontoserver.csiro.au/fhir"
    search_url = f"{terminology_server_url}/ValueSet/$expand"
    
    # Define the parameters for the $expand operation
    params = {
        "url": "http://snomed.info/sct?fhir_vs",  # Base URL for SNOMED CT ValueSet
        "filter": procedure_name,  # Filter the codes by the procedure name
        "count": 1  # Limit to one result
    }
    
    # Perform the GET request with parameters
    response = requests.get(search_url, params=params, headers={"Accept": "application/fhir+json"})
    
    if response.status_code == 200:
        results = response.json()
        # Check if there are matching codes
        if "expansion" in results and "contains" in results["expansion"] and len(results["expansion"]["contains"]) > 0:
            code_entry = results["expansion"]["contains"][0]
            return {
                "code": code_entry["code"],
                "display": code_entry["display"]
            }
        else:
            print(f"No SNOMED CT code found for: {procedure_name}")
    else:
        print(f"Failed to retrieve SNOMED CT code for {procedure_name}. HTTP Status: {response.status_code}")
    
    return None

def get_patient_id_by_name(given_name, family_name):

    hapi_fhir_url = "http://hapi.fhir.org/baseR4"
    search_url = f"{hapi_fhir_url}/Patient?family={family_name}&given={given_name}"
    
    response = requests.get(search_url, headers={"Accept": "application/fhir+json"})
    
    if response.status_code == 200:
        results = response.json()
        if 'entry' in results and len(results['entry']) > 0:
            patient_id = results['entry'][0]['resource']['id']
            return patient_id
        else:
            raise ValueError(f"No patient found with name: {given_name} {family_name}")
    else:
        raise ValueError(f"Failed to retrieve patient ID for {given_name} {family_name}. HTTP Status: {response.status_code}")
