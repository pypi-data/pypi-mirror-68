from helpers.alert import AlertLabel, AlertSeverity, alert_object
from helpers.messages import est_required_extension


def required_uploaded_extension(ems, uploaded_files):
    if not _mitchell_or_ccc_estimate(ems):
        return True

    if _required_extension(ems.est_system) in uploaded_files:
        return True

    return alert_object(
            AlertLabel.EMS_REQUIRED_EXTENSION.value,
            AlertSeverity.ERROR.value,
            lambda: est_required_extension(
                _required_extension(ems.est_system)
            )
        )


# Internal Functions

def _mitchell_or_ccc_estimate(ems):
    return ems.est_system is not None and ems.est_system in ['M', 'C']


def _required_extension(est_system):
    return 'awf' if est_system == 'C' else 'mie'
