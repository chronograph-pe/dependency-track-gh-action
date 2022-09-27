import rubygeminfo
import os
import json

repository = os.environ.get("REPOSITORY")
license_files_path = os.environ.get("LICENSE_FILES_PATH")
gemfile = os.environ.get("GEMFILE")
package_file = os.environ.get("PACKAGE_FILE")
requirements_file = os.environ.get("REQUIREMENTS_FILE")
block_build = os.environ.get("BLOCK_BUILD", False)


def main():
    dependencies = {}

    if not repository:
        print("REPOSITORY env var required".format(repository))
        exit(1)

    if gemfile:
        if not os.path.exists(gemfile):
            print("{} not found".format(gemfile))
            exit(1)
        print("{} found".format(gemfile))
        lics = rubygeminfo.licenses(gemfile, repository, license_files_path)
        dependencies["ruby"] = lics

    if package_file:
        if not os.path.exists(package_file):
            print("{} not found".format(package_file))
            exit(1)
        print("{} found".format(package_file))
        dependencies["node"] = lics

    if requirements_file:
        if not os.path.exists(requirements_file):
            print("{} not found".format(requirements_file))
            exit(1)
        print("{} found".format(requirements_file))
        dependencies["python"] = lics

    results = check_for_violations(dependencies)


def check_for_violations(dependencies):
    violations = []

    with open("restricted_licenses.json") as f:
        restricted_licenses = json.load(f)

    with open("dependency_exceptions.json") as f:
        dependency_exceptions = json.load(f)

    for lang, deps in dependencies.items():
        for env, dependency_list in deps.items():
            for dependency_items in dependency_list:
                for dependency_name, license_name in dependency_items.items():
                    for restricted_license in restricted_licenses:
                        if restricted_license in license_name:
                            if dependency_name in dependency_exceptions:
                                print()
                                print(" ##### Violation found but explicitly excepted. Dependency name: {},  License name: {} ##### ".format(dependency_name, restricted_license))
                                continue
                            violations.append({dependency_name: restricted_license})
                            print()
                            print("############################## LICENSE VIOLATION ##############################")
                            print("Language: {}".format(lang))
                            print("Env: {}".format(env))
                            print("Dependency name: {}".format(dependency_name))
                            print("License name: {}".format(restricted_license))
                            print("###############################################################################")
                            print()

    if block_build:
        if violations:
            print("exiting because restricted licenses are in use...")
            exit(1)
    
    if violations:
            print("restricted licenses are in use...")
    else:
        print("all dependencies are using approved licenses")


if __name__ == "__main__":
    main()
