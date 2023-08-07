"""Implementation of a function that verifies the
inserted tags and validates the standard again in a certain way."""
from . import ok, nok


def __boolToString(b):
    """Converts a boolean to a standard string"""
    return str(b).lower()


BOOLEAN_STANDARD = ["true", "false"]


def checkTagsAndCompleteInfo(usecase, repoName, roleHttp, roleWS, internalAPIGW, customerAPIGW,
                             customerAPIGWWS, externalResourcesAPIGW, stage, config, *nextArgs):
    """Verify and complete the remaining tag information in the use case."""
    tags = usecase["tags"]
    for wayOfInvoke in ["http", "ws", "queue"]:
        tags[wayOfInvoke] = tags.get(wayOfInvoke, "false")
        assert tags[wayOfInvoke] in BOOLEAN_STANDARD, \
            f"{nok}{wayOfInvoke} is not among the standard values allowed for boolean values"
    assert (0 < int(tags["http"] == "true") +
            int(tags["ws"] == "true") + int(tags["queue"] == "true") < 2), \
        f"{nok}More than one of the properties http, ws or queue are true"

    usecase["role"] = roleHttp  # <- default role
    apigw = tags["apigw"]

    if tags["http"] == "true":
        usecase["method"] = usecase["method"].upper()
        assert usecase["method"] in ["GET", "DELETE", "UPDATE", "POST"]
        assert "route" in usecase
        usecase["role"] = roleHttp

        if apigw == "internal":
            usecase["apigateway"] = internalAPIGW
        elif apigw == "customer":
            usecase["apigateway"] = customerAPIGW
        elif apigw == "receptor":
            usecase["apigateway"] = externalResourcesAPIGW
        elif apigw == "none":
            usecase["apigateway"] = "none"
        else:
            raise AssertionError(f"\n{nok}There is no compatible api gateway")

    elif tags["ws"] == "true":
        usecase["role"] = roleWS
        if apigw == "customer":
            usecase["apigateway"] = customerAPIGWWS
        else:
            raise AssertionError(f"\n{nok}There is no compatible api gateway")
    elif tags["queue"] == "true":
        usecase["role"] = roleWS
        usecase["apigateway"] = 'none'
    else:
        usecase["apigateway"] = 'none'

    # Microservice
    tags["ms"] = repoName.split('.')[0]

    # Stage
    usecase["stage"] = stage

    # AWS Layers
    usecase["layers"] = " ".join(nextArgs)

    # Cacheable: if the operation does not change over time, many caches are allowed,
    # and it means that the operation will return the same if the same parameters are received.
    usecase["cacheable"] = usecase.get("cacheable", False)
    tags["cacheable"] = __boolToString(usecase["cacheable"])

    # Need authentication
    usecase["needAuthentication"] = usecase.get("needAuthentication", False)
    tags["needAuthentication"] = __boolToString(usecase["needAuthentication"])

    usecase["envs"] = "".join(f",{k}='{v}'" for k, v in
                              {**usecase.get("envs", {}), **config.get("envs", {})}.items())
    usecase["tagstring"] = ",".join(f"{k}='{v}'" for k, v in tags.items())
    return usecase
