import os
import json


supported_languages = os.environ.get(
    "SUPPORTED_LAGUAGES", ["ruby", "node", "python"])


def check_config_files(config):
    apps = config["apps"]
    errors = []
    
    for app in apps:
        for app_name, app_config in app.items():
            license_file = app_config["license_file"]
            restricted_licenses_file = app_config["restricted_licenses_file"]
            dependency_exceptions_file = app_config["dependency_exceptions_file"]
            language = app_config["language"]
            dependency_file = app_config["dependency_file"]
            
            err = is_language_supported(language)
            if err: errors.append(err)
            
            for f in [license_file, restricted_licenses_file, dependency_exceptions_file, dependency_file]:
                if not os.path.exists(f): errors.append("{} required but not found".format(f))
                        
    return errors
                        
                        
def is_language_supported(language):
    if language not in supported_languages:
        return "{} not a supported languaage at this time".format(language)
    
    return ""
    
    
def check_for_violations(license_data, restricted_licenses_file, dependency_exceptions_file):
    violations = []

    with open(restricted_licenses_file) as f:
        restricted_licenses = json.load(f)

    with open(dependency_exceptions_file) as f:
        dependency_exceptions = json.load(f)
        
    for env, dependencies in license_data.items():
        for dependency in dependencies:
            for dependency_name, license_name in dependency.items():
                for restricted_license in restricted_licenses:
                    if restricted_license in license_name:
                        if dependency_name in dependency_exceptions:
                                print(" ##### Violation found but explicitly excepted. Dependency name: {},  License name: {} ##### ".format(dependency_name, restricted_license))
                                continue
                        violations.append({dependency_name: restricted_license})
                        
    return violations