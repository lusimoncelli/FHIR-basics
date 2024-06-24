from fhir.resources.procedure import Procedure
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from base import get_snomedct_code, get_patient_id_by_name

def create_procedure_resource(procedure_name=None, status=None, patient_name=None, performed_date=None):
    
    # Obtener ID del paciente
    patient_id = get_patient_id_by_name(patient_name)
    
    
    procedure = Procedure(
        status = status,
        subject = Reference(reference=f'Patient/{patient_id}')
    )

    # Add occurrenceDateTime if available
    if performed_date:
        procedure.occurrenceDateTime = performed_date

    # Add code for the procedure
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

    