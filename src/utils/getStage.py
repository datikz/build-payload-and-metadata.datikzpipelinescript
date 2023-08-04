"""Implementation of function to obtain the stage of the repository"""


def getStage(branch):
    """Gets the standardized stage of the repository according to the branch.

    Parameters
    ----------
    branch: str
        Name of raw branch

    Returns
    -------
    stage: str
        Stage standardized to the company
    """
    branch = branch.replace("refs/heads/", "")

    if branch == "master":
        stage = "pdn"
    elif branch.startswith("release"):
        stage = "qa"
    elif branch == "develop" or branch.startswith("feature/"):
        stage = "dev"
    else:
        raise Exception(f"The branch {branch} is invalid")
    return stage
