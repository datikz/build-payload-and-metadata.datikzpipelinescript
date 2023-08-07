"""Implementation of function that creates the zip file for the lambda function"""
import os
import shutil
import sys

from .makeDirRecursively import mkdirR

temp_file_name = "temp"
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
    if os.path.isdir(temp_file_name):
        shutil.rmtree(temp_file_name)
    mkdirR(f"{temp_file_name}/shared")
    os.system(f"cp -r ./shared/* ./{temp_file_name}/shared/")
    assert os.path.isdir(temp_file_name + "/shared/framework")
    shutil.copyfile(f"framework/lambdaAWS/{handler_f_name}", temp_file_name + "/lambda_function.py")
    db = "database"
    if os.path.isdir(db):
        shutil.copytree(db, f"{temp_file_name}/{db}")

        dbSettings = f"{temp_file_name}/{db}/implementations/mongodb/settings/"
        if os.path.isdir(dbSettings):
            shutil.rmtree(dbSettings)
    coincidences = [x for x in usecasesInDir if x["file"] == python_f_name]
    if coincidences:
        path_bef = coincidences[0]["path"]
        mkdirR(f"{temp_file_name}/{path_bef}/")
        shutil.copyfile(f"{path_bef}/{python_f_name}", f"{temp_file_name}/{path_bef}/{python_f_name}")
        shutil.copyfile(f"{path_bef}/__init__.py", f"{temp_file_name}/{path_bef}/__init__.py")
        shutil.copyfile(f"{path_bef}/__init__.py", f"{temp_file_name}/__init__.py")
        shutil.copyfile(f"{path_bef}/{python_f_name}",
                        f"{temp_file_name}/{path_bef}/{python_f_name}")
    inte = "usecases/internal/"
    if os.path.isdir(inte):
        if os.path.isdir(f"{temp_file_name}/{inte}"):
            shutil.rmtree(f"{temp_file_name}/{inte}")
        shutil.copytree(inte, f"{temp_file_name}/{inte}")
    shutil.copytree("buildPayload/", temp_file_name + "/buildPayload/")
    shutil.copyfile(inise, f"{temp_file_name}/{inise}")
    os.system(f"cd {temp_file_name};{sys.executable} lambda_function.py && exit 1;cd ..")
    shutil.rmtree(temp_file_name + "/shared")
    os.system(f"rm -rf {temp_file_name}/shared")
    os.system(f'find {temp_file_name} | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
    os.system(f"find {temp_file_name} -name '*.md' -delete")
    if os.path.exists(nameFile):
        os.remove(f"./{nameFile}")
    shutil.rmtree(f"{temp_file_name}/buildPayload/")
    # Zip file creation
    os.system(f"cd {temp_file_name}; zip -rq ../{nameFile} *;zipinfo -h -t ../{nameFile};cd ..")

    if os.path.isdir(temp_file_name):
        shutil.rmtree(temp_file_name)
