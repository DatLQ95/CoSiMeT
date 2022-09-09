import os

# Config the Database:
database = dict(
    host="nl-cs.genexislocal.nl",
    database="CloudSightServers",
    table=os.environ["COSIMET_DB_TABLE"],
    general_info_table="general_info",
    constant_table = "constant_info",
)

# CS server default info
cs_server_info = dict(
    default_status="N/A",
    default_date="N/A",
    default_version="N/A",
    default_expiry_date="N/A",
)

ansible_data = dict(
    inventory_file_path = "ansible/hosts.yaml",
    main_file_path = "ansible/site.yml",
)

general_info = dict(
    cloudsight_server_install_url = None,
    cs_admin_port = None,
    inteno_password = None,
    inteno_user = None,
    license_server_address = None,
    license_server_IP_addr = None, 
    license_server_port = None,
    salt = None,
    crypto_key = None,
)


status_state = dict(
    available = "Available",
    unreachable = "Unreachable",
    failed = "Failed",
)

