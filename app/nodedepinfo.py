import requests
import json


def licenses(dependency_file, app_name, license_file):
    dependencies = {}
    
    with open(dependency_file) as f:
        dependency_dictionary = json.load(f)
        
    dev_dependencies = dependency_dictionary.get("devDependencies")
    prod_dependencies = dependency_dictionary.get("dependencies")

    dependencies["development"] = dev_dependencies
    dependencies["production"] = prod_dependencies
    
    licenses = get_licenses(dependencies, license_file)
        
    return licenses


def get_licenses(dependencies, license_file):
    full_deps = {}
    
    with open(license_file) as f:
        dependency_data = json.load(f)
        
    for env, deps in dependencies.items():
        licenses = []
        for dep_name, dep_version in deps.items():
            license = dependency_data.get(dep_name)
            if license:
                licenses.append({dep_name: license})
            else:
                print("{} not found in database. fetching from registry.npmjs.org...".format(dep_name))
                license = fetch_license(dep_name)
                licenses.append({dep_name: license})
                add_dep_to_license_file(dep_name, license, license_file)
        full_deps[env] = licenses
                
    return full_deps


def fetch_license(dep_name):
    r = requests.get(
        'https://registry.npmjs.org/{}'.format(dep_name))
    
    if r.status_code != 200:
        return "error"
    
    data = r.json()

    if not data.get("license"):
        return ["unknown"]
    
    return [data.get("license")]


def add_dep_to_license_file(dep_name, license, license_file):
    with open(license_file,'r+') as file:
        file_data = json.load(file)
        file_data[dep_name] = license
        file.seek(0)
        json.dump(file_data, file, indent = 4)

