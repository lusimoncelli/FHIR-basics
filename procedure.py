from fhir.resources.procedure import Procedure, ProcedurePerformer
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from base import get_procedure_snomedct_code, get_patient_id_by_name

def create_procedure_resource(procedure_name = None, status = None, patient_name = None, performed_date = None, performer_id = None):
    
    procedure = Procedure()
    
    # Get procedure and patient codes
    snomed = get_procedure_snomedct_code(procedure_name)
    patient_id = get_patient_id_by_name(patient_name)
    
    if snomed is None:
        raise ValueError(f"Could not find SNOMED CT code for procedure: {procedure_name}")
    
    # status: done, in progress, unknown,
    procedure.status = status
    procedure.occurrenceDateTime = performed_date
    
    procedure.code = CodeableConcept(
        coding = [
            Coding(
                system="http://snomed.info/sct",
                code=snomed["code"],
                display=snomed["display"]
            )
        ])
    
    procedure.subject = Reference(reference = f'Patient/{patient_id}')
    procedure.performer = performer_id
    
    return procedure
    