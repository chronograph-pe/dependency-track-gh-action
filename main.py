from ast import arg
from audioop import add
import os
from unittest import result
import time
import datetime
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    url = os.environ.get("URL")
    api_key = os.environ.get("API_KEY")
    project_uuid = os.environ.get("PROJECT_UUID")

    args = {
        "url": url,
        "api_key": api_key,
        "project_uuid": project_uuid
    }

    err = input_validation(args)
    if err:
        print(f"::set-output name=results::{err}")
        print(f"::set-output name=status::false")
        return

    dependencies, err = gets_dependencies(args)
    if err:
        print(f"::set-output name=results::{err}")
        print(f"::set-output name=status::false")
        return
   

    results = find_new_vulnerbilities(dependencies)
    if not results:
        print(f"::set-output name=status::true")

    print(f"::set-output name=results::{results}")
    print(f"::set-output name=status::false")
    

def input_validation(args):
    if not args["url"]:
        return "no url input found"

    if not args["api_key"]:
        return "no api key found"

    if not args["project_uuid"]:
        return "no project uuid found"

    return ""


def gets_dependencies(args):
    r = requests.get('{}/api/v1/dependency/project/{}'.format(
        args["url"], args["project_uuid"]), 
        headers={"Content-Type":"application/json", "X-Api-Key": args["api_key"]})

    if r.status_code != 200:
        return {}, "failed getting dependencies"

    results = r.json()

    return results, None


def find_new_vulnerbilities(dependencies):
    now = datetime.datetime.fromtimestamp(time.time()) 
    results = {}

    for dependency in dependencies:
        added_on = datetime.datetime.fromtimestamp(dependency["addedOn"] / 1000)

        delta = now - added_on
        minutes = divmod(delta.total_seconds(), 60) 
        if minutes[0] <= os.getenv("TIME_DIFF", 60):
            component = dependency.get("component")
            metrics = dependency.get("metrics")
            component_version = "{}-{}".format(component["name"], component["version"]) 
            if (metrics["critical"] or metrics["high"]) >= 1:
                results[component_version] = {
                    "critical": metrics["critical"],
                    "high": metrics["high"]
                }

    return results


if __name__ == "__main__":
    main()
