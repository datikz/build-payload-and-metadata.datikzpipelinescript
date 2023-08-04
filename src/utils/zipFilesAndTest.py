"""Implementation of function that creates the zip file for the lambda function"""
import os
import shutil
import sys

from src.utils.makeDirRecursively import mkdirR

t = "temp"
inise = "initializerService.py"


def zipFilesAndTest(usecase, usecasesInDir):
    """Packages the code in a zip file for the lambdas in aws

    Parameters
    ----------
    usecase: dict
        Use case information
    usecasesInDir: list
        Information of the use cases in the code folder

    Returns
    -------
    None
    """
    uc_keyname = usecase["keyname"]
    nameFile = f"lambdaFunction{uc_keyname}.zip"

    if "base" in usecase:
        uc_base = usecase["base"]
    else:
        uc_base = uc_keyname
    python_f_name, handler_f_name = f'{uc_base}UseCase.py', f'{uc_base}Handler.py'
    if os.path.isdir(t): shutil.rmtree(t)
    mkdirR(f"{t}/shared")
    os.system(f"cp -r ./shared/* ./{t}/shared/")
    assert os.path.isdir(t + "/shared/framework")
    shutil.copyfile(f"framework/lambdaAWS/{handler_f_name}", t + "/lambda_function.py")
    db = "database"
    os.path.isdir(db) and shutil.copytree(db, f"{t}/{db}") and shutil.rmtree(
        f"{t}/{db}/implementations/mongodb/settings/")
    coincidences = [x for x in usecasesInDir if x["file"] == python_f_name]
    if coincidences:
        path_bef = coincidences[0]["path"]
        mkdirR(f"{t}/{path_bef}/")
        shutil.copyfile(f"{path_bef}/{python_f_name}", f"{t}/{path_bef}/{python_f_name}")
        shutil.copyfile(f"{path_bef}/__init__.py", f"{t}/{path_bef}/__init__.py")
        shutil.copyfile(f"{path_bef}/__init__.py", f"{t}/__init__.py")
        shutil.copyfile(f"{path_bef}/{python_f_name}",
                        f"{t}/{path_bef}/{python_f_name}")
    inte = "usecases/internal/"
    if os.path.isdir(inte):
        if os.path.isdir(f"{t}/{inte}"): shutil.rmtree(f"{t}/{inte}")
        shutil.copytree(inte, f"{t}/{inte}")
    shutil.copytree("src/", t + "/src/")
    shutil.copyfile(inise, f"{t}/{inise}")
    os.system(f"cd {t};{sys.executable} lambda_function.py && exit 1;cd ..")
    shutil.rmtree(t + "/shared")
    os.system(f"rm -rf {t}/shared")
    os.system(f'find {t} | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
    os.system(f"find {t} -name '*.md' -delete")
    if os.path.exists(nameFile):
        os.remove(f"./{nameFile}")
    os.system(f"cd {t}; zip -rq ../{nameFile} *;zipinfo -h -t ../{nameFile};cd ..")
