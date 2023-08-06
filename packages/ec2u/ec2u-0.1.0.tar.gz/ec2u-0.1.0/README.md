# EC2 Utils
- Before you can begin using **ec2-utils**, you must set up authentication credentials. 
If you have the AWS CLI installed, then you can use it to configure your credentials file:
```
aws configure 
```
Alternatively, you can create the credential file yourself. By default, its location is at `~/.aws/credentials`:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```
You may also want to set a default region. This can be done in the configuration file. By default, its location is at ~/.aws/config:
```
[default]
region=us-east-1
```

This sets up credentials for the default profile as well as a default region to use when creating connections. 
See [Credentials](https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration) for in-depth configuration sources and options.

- Supported Python: 2.7
- Install dependencies: `pip install -r requirements.txt`
- Features:
    - Get public IP address by EC2 instance name.
        ```python
        from ec2-utils import get_public_ip
  
        print(get_public_ip("Instance Name"))
        ```
        Output: `{"public_ip": "54.254.212.129", "name": "Instance Name"}`
        
    - Assign an Elastic IP to EC2 instance
        ```python
        from ec2-utils import assign_elastic_ip
  
        assign_elastic_ip("10.11.12.13", "Instance Name")
        ```
