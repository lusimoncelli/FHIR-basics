from fhir.resources.condition import Condition
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from base import get_snomedct_code, get_patient_id_by_name

def create_condition_resource(condition_name=None, clinical_status=None, verification_status=None, given_name=None, family_name = None, onset_date=None):
    
    # Obtener ID del paciente
    if given_name and family_name:
        patient_id = get_patient_id_by_name(given_name, family_name)

    
    # Crear instancia de Condition con clinicalStatus y subject (required)
    condition = Condition(
        clinicalStatus = CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                    code=clinical_status
                )
            ]
        ),
        subject = Reference(reference=f'Patient/{patient_id}')
    )

    # Agregar verification status si está disponible
    if verification_status:
        condition.verificationStatus = CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    code=verification_status
                )
            ]
        )

    # Agregar código de la condición
    if condition_name:
        snomed = get_snomedct_code(condition_name)
        if snomed is None:
            raise ValueError(f"No se pudo encontrar el código SNOMED CT para la condición: {condition_name}")

        condition.code = CodeableConcept(
            coding=[
                Coding(
                    system="http://snomed.info/sct",
                    code=snomed["code"],
                    display=snomed["display"]
                )
            ]
        )

    # Agregar fecha de inicio si está disponible
    if onset_date:
        condition.onsetDateTime = onset_date

    return condition

