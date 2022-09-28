from gemfileparser2 import GemfileParser
import requests
import json
from pathlib import Path


def licenses(dependency_file, app_name, license_file):
    licenses = {}

    n = GemfileParser(dependency_file, app_name)
    dependency_dictionary = n.parse()

    for env, dependencies in dependency_dictionary.items():
        print("Finding licenses for gems in {}...".format(env))
        if dependencies:
            gem_names = []
            for gem in dependencies:
                gem_names.append(gem.name)
            lics = get_licenses(gem_names, license_file)
            licenses[env] = lics
    
    return licenses


def get_licenses(gem_names, license_file):
    licenses = []
    
    with open(license_file) as f:
        dependency_data = json.load(f)
            
    for gem_name in gem_names:
        license = dependency_data.get(gem_name)
        if license:
            licenses.append({gem_name: license})
        else:
            print("{} not found in database. fetching from rubygems.org...".format(gem_name))
            license = fetch_license(gem_name)
            licenses.append({gem_name: license})
            if license:
                add_gem_to_license_file(gem_name, license, license_file)
            
    return licenses


def fetch_license(gem_name):
    r = requests.get(
        'https://rubygems.org/api/v1/gems/{}.json'.format(gem_name))
    
    if r.status_code != 200:
        print("error retrieving {} license. skipping adding to licenses.json.".format(gem_name))
        return False
    
    data = r.json()

    if not data.get("licenses"):
        print("[WARN] No license info found for {}".format(gem_name))
        return "unknown"
    
    return data.get("licenses")


def add_gem_to_license_file(gem_name, license, license_file):
    with open(license_file,'r+') as file:
        file_data = json.load(file)
        file_data[gem_name] = license
        file.seek(0)
        json.dump(file_data, file, indent = 4)


 