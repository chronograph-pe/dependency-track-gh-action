from gemfileparser2 import GemfileParser
import requests
import json
from pathlib import Path



def licenses(gemfile, repository):
    n = GemfileParser(gemfile, repository)
    dependency_dictionary = n.parse()
    licenses = {}

    for env, dependencies in dependency_dictionary.items():
        print("Finding licenses for gems in {}...".format(env))
        if dependencies:
            gem_names = []
            for gem in dependencies:
                gem_names.append(gem.name)
            lics = get_licenses(gem_names, repository)
            licenses[env] = lics
    
    return licenses


def get_licenses(gem_names, repository):
    licenses = []
    license_file = "licenses/{}/ruby/lic.json".format(repository)
    
    with open(license_file) as f:
        license_data = json.load(f)
        
    for gem_name in gem_names:
        license = license_data.get(gem_name)
        if license:
            licenses.append({gem_name: license})
        else:
            print("{} not found in database. fetching from rubygems.org...".format(gem_name))
            license = fetch_license(gem_name)
            licenses.append({gem_name: license})
            add_gem_to_license_file(gem_name, license, license_file)
            
    return licenses


def fetch_license(gem_name):
    r = requests.get(
        'https://rubygems.org/api/v1/gems/{}.json'.format(gem_name))
    
    if r.status_code != 200:
        return "error"
    
    data = r.json()

    if not data.get("licenses"):
        return "unknown"
    
    return data.get("licenses")


def add_gem_to_license_file(gem_name, license, license_file):
    with open(license_file,'r+') as file:
        file_data = json.load(file)
        file_data[gem_name] = license
        file.seek(0)
        json.dump(file_data, file, indent = 4)


 