### Examples:
```
xopera-template-library setup
xopera-template-library login --username "username1" --password "password1"

xopera-template-library template save --name AwsLambda --path example/AwsLambdaFunction --public_access True --version 0.0.4

xopera-template-library template list --name AwsLambda --public_access True
xopera-template-library template version list --template_id 4

xopera-template-library template get --version_id 4 --path test-folder --public_access True
``` 


### Particle to upload structure
 ```        
|-- ParticleFolder
        |-- files
            |-- create.yml
            |-- undeploy.yml
        |-- NodeType.tosca
```