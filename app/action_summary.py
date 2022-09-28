
def create(license_violations):
        
   with open ("job_summary.md", "w") as f:
       f.write("# Dependency Check Summary \n")
       f.write(" --- \n")
       f.write("### License Violations\n")
       f.write("")
       f.write("")
       if not license_violations:
           f.write("#### No license violations found\n\n")
       else:
           f.write("| App Name | Language | Dependency Name | License Name\n")
           f.write("| ------ | ------ | ------ | ------ | \n")
           for violation in license_violations:
            f.write("| {} | {} | {} | {} |\n".format(
                violation["app_name"], violation["language"], 
                violation["dependency_name"], violation["license_name"]
            ))