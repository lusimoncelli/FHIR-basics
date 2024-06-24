from patient import create_patient_resource
from procedure import create_procedure_resource
from condition import create_condition_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir

if __name__ == "__main__":
    # Parámetros del paciente (se puede dejar algunos vacíos)
    family_name = "Langone"
    given_name = "Mila"
    birth_date = "2000-12-20"
    gender = "female"
    phone = None 

    # Crear y enviar el recurso de paciente
    patient = create_patient_resource(family_name, given_name, birth_date, gender, phone)
    patient_id = send_resource_to_hapi_fhir(patient, 'Patient')

    
    # Parametros de la condicion
    condition_name = 'Coronary arteiosclerosis'
    clinical_status = "active"
    verification_status = "confirmed"
    onset_date = "2024-05-24"

    # Crear y enviar el recurso condicion
    condition = create_condition_resource(condition_name, clinical_status, verification_status, given_name, family_name, onset_date)
    condition_id = send_resource_to_hapi_fhir(condition, 'Condition')

    # Parametros del procedimiento
    procedure_name = 'Open heart surgery'
    status = "completed"
    performed_date = "2024-06-01"

    # Crear y enviar recurso de procedimiento
    procedure = create_procedure_resource(procedure_name, status, given_name, family_name, performed_date)
    procedure_id = send_resource_to_hapi_fhir(procedure, 'Procedure')
    
    # Ver el recurso de paciente creado
    print('\n')
    if patient_id:
        get_resource_from_hapi_fhir(patient_id,'Patient')
    print('\n')
    if procedure_id:
        get_resource_from_hapi_fhir(procedure_id, 'Procedure')
    print('\n')
    if condition_id:
        get_resource_from_hapi_fhir(condition_id, 'Condition')
    print('\n')