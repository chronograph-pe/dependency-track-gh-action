#  dependency-track-gh-action

A github action to check if our apps our using dependencies with non-approved licenses. 

## Installation

1. Add `dependency-check-config.yml` to the root of a repo you want to check licenses for. The repo can contain multiple apps you want to scan.  
2. Use the following configuration to the yaml as a template...
```yaml
apps:
  # A list of apps in your repo that you want to check licenses for
  - {app_name}:
      # A file (can be empty) that the action will store dependencies 
      # and their licenses. This is used to cache license data 
      # obtained remotely. 
      license_file: sample-ruby-app/licenses.json
      # A file (can be empty) to store licenses you do not want
      # to be used in your apps. 
      restricted_licenses_file: sample-ruby-app/restricted_licenses.json
      # A file (can be empty) to store dependencies that will 
      # bypass license checks.
      dependency_exceptions_file: sample-ruby-app/dependency_exceptions.json
      # Currently supports ruby, python, and node
      language: ruby
      # The location of your dependency file (currently supports Gemfile, 
      # package.json, and requirements.txt.
      dependency_file: sample-ruby-app/Gemfile
# If set to true, license violations will return an exit(1) to block a build
block_build: False
```
3. Add `license_file.json`, `restricted_licenses.json`, and `dependency_exceptions.json` files to your app directory. Add `{}` to all these files before first run.  

## Usage

The `license_file.json` file will contain a list of dependencies and their licenses that are scanned via this action. The license is used to cache data so we don't have to look to outside sources for license data every run. The action will auto-commit updates as needed. 

No need to touch this file after initial creation.

The `restricted_licenses.json` file contains a list of dependency licenses you do not want to use in your app. You should https://spdx.org/licenses/ ID's in list format to this file, then commit to the repo. For example:

```json
# restricted_licenses.json

{
 ["LGPL-2.0-only", "LPL-1.0"]
}
```

The `dependency_exceptions.json` file contains a list of dependency names you want to skip checks for. Follow the same schema as the `restricted_licenses.json` except use dependency names. You can look in `license_file.json` to find valid names, or look in the github action console output. 
