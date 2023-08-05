# Script for generating payload of the use cases

This script collects the information provided in the microservice repository of the use cases. 
use cases.

Sources of information

- Raw code
- ./docs/info.yaml
- Pipeline variables 
- Repository information on github

## Pseudocode

- Reading environment variables
- Reading yaml file
- Read code from repository
- Identify framework to deploy to
- Generate code packages for given framework
- Generate file with metadata

The pipeline to call this script has the following code as standard

~~~python
from

{pipeline - standard - scripts.datikzpipeline.src}.main
import main

main()
~~~

Where `pipeline-standard-scripts.datikzpipeline.src` is to be renamed according to pipeline decision
