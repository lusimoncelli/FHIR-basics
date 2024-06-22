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

def get_procedure_snomedct_code(procedure_name):
    
    terminology_server_url = "https://r4.ontoserver.csiro.au/fhir"
    search_url = f"{terminology_server_url}/CodeSystem/$lookup?system=http://snomed.info/sct&code={procedure_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        results = response.json()
        # Parse the result to get the SNOMED CT code and display text
        for parameter in results.get("parameter", []):
            if parameter["name"] == "code":
                snomed_code = parameter["valueString"]
            elif parameter["name"] == "display":
                snomed_display = parameter["valueString"]
                
        return {"code": snomed_code, "display": snomed_display}
    else:
        print(f"Failed to retrieve SNOMED CT code for {procedure_name}. HTTP Status: {response.status_code}")
        return None