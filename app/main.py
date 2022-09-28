import rubygeminfo
import nodedepinfo
import pythondepinfo
import action_summary
import os
import tools
import yaml
from pathlib import Path

dependency_check_config_file = os.environ.get(
    "DEPENDENCY_CHECK_CONFIG", "./dependency-check-config.yml")


def main():
    license_violations = []
    
    if not os.path.exists(dependency_check_config_file):
        print("{} not found".format(dependency_check_config_file))
        exit(1)
    
    config = yaml.safe_load(Path(dependency_check_config_file).read_text())
    
    err = tools.check_config_files(config)
    if err: print(err); exit(1)

    for app in config["apps"]:
        for app_name, app_config in app.items():
            print("-- Generating license data for {}".format(app_name))
            
            license_file = app_config["license_file"]
            restricted_licenses_file = app_config["restricted_licenses_file"]
            dependency_exceptions_file = app_config["dependency_exceptions_file"]
            language = app_config["language"]
            dependency_file = app_config["dependency_file"]
            
            if language == "ruby":
                license_data = rubygeminfo.licenses(dependency_file, app_name, license_file)

            if language == "python":
                license_data = pythondepinfo.licenses(dependency_file, app_name, license_file)
            
            if language == "node":
                license_data = nodedepinfo.licenses(dependency_file, app_name, license_file)

            violations = tools.check_for_violations(
                license_data, restricted_licenses_file, dependency_exceptions_file)

            if violations:
                for violation in violations:
                    for dependency_name, license_name in violation.items():
                        license_violations.append({
                            "app_name": app_name,
                            "language": language,
                            "dependency_name": dependency_name,
                            "license_name": license_name
                        })
                   
    action_summary.create(license_violations)
         
    if license_violations:
        for violation in license_violations:
            print()
            print("################ LICENSE VIOLATION ################")
            print("App name: {}".format(violation["app_name"]))
            print("Language: {}".format(violation["language"]))
            print("Dependency name: {}".format(violation["dependency_name"]))
            print("License name: {}".format(violation["license_name"]))
            print("###################################################")
    
        if config["block_build"]:
            print("exiting...")
            exit(1)
    else:
         print("[OK] No license violations found")
            
   

if __name__ == "__main__":
    main()
