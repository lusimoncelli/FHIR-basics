from patient import create_patient_resource
from procedure import create_procedure_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir

if __name__ == "__main__":
    # Parámetros del paciente (se puede dejar algunos vacíos)
    family_name = "Doe"
    given_name = "John"
    birth_date = "1990-01-01"
    gender = "male"
    phone = None 

    # Parametros del procedimiento
    procedure_name = "Open heart surgery"
    status = "completed"
    patient_name = "John Doe"
    performed_date = "2024-06-01"

    # Crear y enviar el recurso de paciente
    patient = create_patient_resource(family_name, given_name, birth_date, gender, phone)
    patient_id = send_resource_to_hapi_fhir(patient, 'Patient')

    # Crear y enviar recurso de procedimiento
    procedure = create_procedure_resource(procedure_name, status, patient_name, performed_date)
    procedure_id = send_resource_to_hapi_fhir(procedure, 'Procedure')
    
    # Ver el recurso de paciente creado
    if patient_id:
        get_resource_from_hapi_fhir(patient_id,'Patient')
    if procedure_id:
        get_resource_from_hapi_fhir(procedure_id, 'Procedure')