import requests
import json
import requirements

def licenses(dependency_file, app_name, license_file):
    dependencies = {}
    
    with open(dependency_file) as f:
        dep_names = []
        for req in requirements.parse(f):
            dep_names.append(req.name)

    dependencies["production"] = dep_names
        
    licenses = get_licenses(dependencies, license_file)
    
    return licenses
    

def get_licenses(dependencies, license_file):
    full_deps = {}
    
    with open(license_file) as f:
        dependency_data = json.load(f)
        
    for env, deps in dependencies.items():
        licenses = []
        for dep_name in deps:
            license = dependency_data.get(dep_name)
            if license:
                licenses.append({dep_name: license})
            else:
                print("{} not found in database. fetching from pypi.org...".format(dep_name))
                license = fetch_license(dep_name)
                if license:
                    add_dep_to_license_file(dep_name, license, license_file)
                licenses.append({dep_name: license})
        full_deps[env] = licenses  
        
    return full_deps


def fetch_license(dep_name):
    r = requests.get(
        'https://pypi.org//pypi/{}/json'.format(dep_name))
    
    if r.status_code != 200:
        print("error retrieving {} license. skipping adding to licenses.json.".format(dep_name))
        return False
    
    data = r.json().get("info")
    
    if not data.get("license"):
        print("[WARN] No license info found for {}".format(dep_name))
        return ["unknown"]
    
    return [data.get("license")]


def add_dep_to_license_file(dep_name, license, license_file):
    with open(license_file,'r+') as file:
        file_data = json.load(file)
        file_data[dep_name] = license
        file.seek(0)
        json.dump(file_data, file, indent = 4)
