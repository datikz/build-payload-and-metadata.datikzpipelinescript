# Script for generating payload of the use cases

This script collects the information provided in the microservice repository of the use cases. 
use cases.

Sources of information

- Raw code
- ./docs/info.yaml
- Pipeline variables 
- Repository information on GitHub

## Pseudocode

- Reading environment variables
- Reading yaml file
- Read code from repository
- Identify framework to deploy to
- Generate code packages for given framework
- Generate file with metadata



The pipeline performs the execution of the script by changing 
the name of the main and executing everything through it.