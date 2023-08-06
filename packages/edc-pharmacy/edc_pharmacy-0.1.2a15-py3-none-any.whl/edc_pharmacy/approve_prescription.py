class PrescriptionApprovalValidatorError(Exception):
    pass


class ApprovePrescription:

    prescription_model = "edc_pharmacy.prescription"

    def __init__(self, prescription_model_obj=None):
        dispense_appointment = prescription_model_obj.dispense_appointment
        previous_appointment = dispense_appointment.previous()
        if previous_appointment:
            if prescription_model_obj.__class__.objects.filter(
                is_approved=False, dispense_appointment=previous_appointment
            ).exists():
                raise PrescriptionApprovalValidatorError(
                    f"Future prescriptions cannot be approved. Approve "
                    f"prescriptions for dispensing date "
                    f"{previous_appointment.appt_datetime}"
                )
