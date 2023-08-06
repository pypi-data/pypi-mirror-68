def audatex_software(ems):
    return ems.est_system == 'A'


def valid_audatex_version(ems):
    return ems.ems_ver is not None and ems.ems_ver >= '2.6'


def mitchell_software(ems):
    return ems.est_system == 'M'


def ccc_software(ems):
    return ems.est_system == 'C'
