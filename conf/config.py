"""
    Configuration file for the project.
"""

dev = {
    "amaya_default_config": "./conf/amaya_default_config.json",
    "model_path": "./models",
    "uploaded_file_save_path": "./uploaded",
    "processed_file_path": "./Result",
    "app_port": 5010,
    "server_configuration": {
        "engine.autoreload_on": True,
        "log.screen": True,
        "server.socket_host": "0.0.0.0",
        "server.ssl_module": "pyopenssl",
        "server.ssl_certificate": "my_cert.crt",
        "server.ssl_private_key": "my_cert.key",
        "server.ssl_certificate_chain": "gd_bundle.crt",
        "log_file_prefix": "./logs/application.log"
    }
}

uat = {
    "amaya_default_config": "./conf/amaya_default_config.json",
    "model_path": "./models",
    "uploaded_file_save_path": "./uploaded",
    "processed_file_path": "./processed_images",
    "app_port": 5010,
    "server_configuration": {
        "engine.autoreload_on": True,
        "log.screen": True,
        "server.socket_host": "0.0.0.0",
        "server.ssl_module": "pyopenssl",
        "server.ssl_certificate": "my_cert.crt",
        "server.ssl_private_key": "my_cert.key",
        "server.ssl_certificate_chain": "gd_bundle.crt",
        "log_file_prefix": "./logs/application.log"
    }
}

prod = {
    "amaya_default_config": "./conf/amaya_default_config.json",
    "model_path": "./models",
    "uploaded_file_save_path": "./uploaded",
    "processed_file_path": "./processed_images",
    "app_port": 5010,
    "server_configuration": {
        "engine.autoreload_on": True,
        "log.screen": True,
        "server.socket_host": "0.0.0.0",
        "server.ssl_module": "pyopenssl",
        "server.ssl_certificate": "my_cert.crt",
        "server.ssl_private_key": "my_cert.key",
        "server.ssl_certificate_chain": "gd_bundle.crt",
        "log_file_prefix": "./logs/application.log"
    }
}
