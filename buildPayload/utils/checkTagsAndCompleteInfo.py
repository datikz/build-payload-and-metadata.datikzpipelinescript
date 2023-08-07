"""Implementation of a function that verifies the
inserted tags and validates the standard again in a certain way."""
from . import ok, nok


def checkTagsAndCompleteInfo(usecase, repoName, roleHttp, roleWS, internalAPIGW, customerAPIGW,
                             customerAPIGWWS, externalResourcesAPIGW, stage, config, *nextArgs):
    """Verify and complete the remaining tag information in the use case."""
    tags = usecase["tags"]
    if tags.get("http", "true") == "true":
        usecase["method"] = m = usecase["method"].upper()
        assert m in ["GET", "DELETE", "UPDATE", "POST"]
    usecase["cacheable"] = usecase.get("cacheable", False)
    tags["ws"] = tags.get("ws", "false")
    usecase["needAuthentication"] = usecase.get("needAuthentication", False)
    tags["ms"] = repoName.split('.')[0]
    usecase["stage"] = stage
    usecase["layers"] = " ".join(nextArgs)
    apigw = tags["apigw"]
    if tags["ws"] == "true":
        usecase["role"] = roleWS
        if apigw == "customer":
            usecase["apigateway"] = customerAPIGWWS
        else:
            raise Exception(f"\n{nok}There is no compatible api gateway")
    else:
        usecase["role"] = roleHttp
        if apigw == "internal":
            usecase["apigateway"] = internalAPIGW
        elif apigw == "customer":
            usecase["apigateway"] = customerAPIGW
        elif apigw == "receptor":
            usecase["apigateway"] = externalResourcesAPIGW
        elif apigw == "none":
            pass
        else:
            raise Exception(f"\n{nok}There is no compatible api gateway")
    usecase["envs"] = "".join(f",{k}='{v}'" for k, v in
                              {**usecase.get("envs", {}), **config.get("envs", {})}.items())
    usecase["tagstring"] = ",".join(f"{k}='{v}'" for k, v in tags.items())
    return usecase
