import json
import os
import sys

from buildPayload.utils.checkTagsAndCompleteInfo import checkTagsAndCompleteInfo
from buildPayload.utils.getStage import getStage
from buildPayload.utils.getYamlFn import getYaml
from buildPayload.utils.getInfoAndPaths import getInfoAndPaths
from buildPayload.utils.zipFilesAndTest import zipFilesAndTest


def buildPayload(*args, **_):
    repoName = args[1]
    branch = args[2]
    config = getYaml(args[3])
    roleHttp = args[4]
    roleWS = args[5]
    internalAPIGW = args[6]
    customerAPIGW = args[7]
    customerAPIGWWS = args[8]
    externalResourcesAPIGW = args[9]
    stage = getStage(branch)
    usecases_in_dir = getInfoAndPaths('usecases')
    if config.get("framework") == "lambdaAWS":
        os.environ["PASSWORD_DATABASE"] = "example_password"
        os.environ["USERNAME_DATABASE"] = "example_username"
        os.environ["URL_DATABASE"] = "example_url"
        for usecase in config["usecases"]:
            usecaseKeyname = usecase["keyname"]
            zipFilesAndTest(usecase, usecases_in_dir)
            usecase = checkTagsAndCompleteInfo(
                usecase, repoName, roleHttp, roleWS, internalAPIGW, customerAPIGW, customerAPIGWWS,
                externalResourcesAPIGW, stage, config, *args[10:])
            with open(f"{usecaseKeyname}.txt", "w", encoding="utf8") as metadataFile:
                json.dump(usecase, metadataFile, indent=4)


if __name__ == "__main__":
    buildPayload(*sys.argv)

