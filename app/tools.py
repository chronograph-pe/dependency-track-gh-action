import os
import json


supported_languages = os.environ.get(
    "SUPPORTED_LAGUAGES", ["ruby", "node", "python"])


def check_config_files(config):
    apps = config["apps"]
    errors = []
    allowed_licenses_file = config["allowed_licenses_file"]

    if not os.path.exists(allowed_licenses_file):
        errors.append("allowed_license_file required but not found")
    
    for app in apps:
        for app_name, app_config in app.items():
            license_file = app_config["license_file"]
            dependency_exceptions_file = app_config["dependency_exceptions_file"]
            language = app_config["language"]
            dependency_file = app_config["dependency_file"]
            
            err = is_language_supported(language)
            if err: errors.append(err)
            
            for f in [license_file, dependency_exceptions_file, dependency_file]:
                if not os.path.exists(f): errors.append("{} required but not found".format(f))
                        
    return errors
                        
                        
def is_language_supported(language):
    if language not in supported_languages:
        return "{} not a supported languaage at this time".format(language)
    
    return ""


def check_for_violations(license_data, allowed_licenses_file, dependency_exceptions_file):
    violations = []
    exceptions = []
    unknown_licenses = []

    with open(allowed_licenses_file) as f:
        a = json.load(f)
        allowed_licenses = [item.lower() for item in a]

    with open(dependency_exceptions_file) as f:
        d = json.load(f)
        dependency_exceptions = [item.lower() for item in d]

    for env, dependencies in license_data.items():
        for dependency in dependencies:
            for dependency_name, l in dependency.items():
                license_name = None
                while type(license_name) != str:
                    if type(l) == list:
                        license_name = l[0]
                    elif type(l) == dict:
                        license_name = l.get("type", "unknown")
                    else:
                        license_name = str(l)

                    l = license_name

                if license_name.lower() not in allowed_licenses:
                    if dependency_name.lower() in dependency_exceptions:
                        print(" ##### Violation found but explicitly excepted. Dependency name: {},  License name: {} ##### ".format(dependency_name, license_name))
                        exceptions.append({dependency_name: license_name})
                        continue
                    if license_name.lower() == "unknown":
                        print(" ##### Unknown license for a dependency found . Dependency name: {},  License name: {} ##### ".format(dependency_name, license_name))
                        unknown_licenses.append({dependency_name: license_name})
                        continue
                    violations.append({dependency_name: license_name})

    return violations, exceptions, unknown_licenses
