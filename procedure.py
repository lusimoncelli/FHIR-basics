from fhir.resources.procedure import Procedure, ProcedurePerformer
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.eventdefinition import EventDefinition
from fhir.resources.reference import Reference
from base import get_procedure_snomedct_code, get_patient_id_by_name

def create_procedure_resource(procedure_name = None, status = None, patient_name = None, performed_date = None):
    
    # Get procedure and patient codes
    snomed = get_procedure_snomedct_code(procedure_name)
    patient_id = get_patient_id_by_name(patient_name)
    
    if snomed is None:
        raise ValueError(f"Could not find SNOMED CT code for procedure: {procedure_name}")
    
    procedure = Procedure(
        status = status,
        occurrenceDateTime = performed_date,
        code = CodeableConcept(
            coding = [
                Coding(
                    system="http://snomed.info/sct",  # SNOMED CT system URL
                    code=snomed["code"],
                    display=snomed["display"]
                )
            ]
        ),
        subject = Reference(reference = f'Patient/{patient_id}'),
        )
    
    return procedure
    