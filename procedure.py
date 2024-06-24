from fhir.resources.procedure import Procedure
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from base import get_snomedct_code, get_patient_id_by_name

def create_procedure_resource(procedure_name=None, status=None, given_name = None, family_name = None, performed_date=None):
    
    # Obtener ID del paciente
    patient_id = get_patient_id_by_name(given_name, family_name)
    
    
    if patient_id is None:
        raise ValueError(f"Could not find patient: {f'{given_name} {family_name}'}")
    
    procedure = Procedure(
        status = status,
        subject = Reference(reference=f'Patient/{patient_id}')
    )

    # Agregar occurrenceDateTime
    if performed_date:
        procedure.occurrenceDateTime = performed_date

    #  Agregar codigo para el procedimiento
    if procedure_name:
        snomed = get_snomedct_code(procedure_name)
        if snomed is None:
            raise ValueError(f"Could not find SNOMED CT code for procedure: {procedure_name}")
        procedure.code = CodeableConcept(
            coding=[
                Coding(
                    system="http://snomed.info/sct",  # SNOMED CT system URL
                    code=snomed["code"],
                    display=snomed["display"]
                )
            ]
        )

    return procedure

    