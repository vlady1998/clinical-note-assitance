# Setting Up GPU server

## Create a GPU server instance

**You need to create a GPU instance that we can host our AI models.**

**1. Go to your AWS console, and select EC2.**

**2. Select "Stockholm" region on the header. This is the region where your GPU instance will be located.**
   
   
![image](https://github.com/supercompany-llc/backend/assets/35817574/9d0a707c-7763-4d75-80cf-507dc8a7fb39)


**3. On the left sidebar select "Instances", and click "Launch Instances".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/af7ae046-a65a-46c7-b433-82bb59ab4cc9)


**4. Input instance name(eg. "GPU server"), select "Ubuntu Server 22.04 LTS(HVM)" among AMI.**
   

![image](https://github.com/supercompany-llc/backend/assets/35817574/ec42b50b-b017-4fb7-b9b0-7230e137a61e)


**5. In "Instance type", select "g4dn.xlarge"(this is the cheapest GPU instance type).**

*If you need to run llama model, you need at least g5.2xlarge instance.*

![image](https://github.com/supercompany-llc/backend/assets/35817574/e6ae2f43-0065-43a5-8500-710e58f349e3)


**6. Select or Create your key file that you will use when you access instance through SSH.**


![image](https://github.com/supercompany-llc/backend/assets/35817574/1458a919-4772-4e8e-989e-c206b74f750d)


**7. You can leave "Network settings" as they are, and in "Configuration storage", input 100 GiB, gp3.**


![image](https://github.com/supercompany-llc/backend/assets/35817574/8264f800-3891-4293-a9d7-fe0216cd5ca1)


**8. Click "Launch instance" and wait until "status check" become "*/* checks passed".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/2cd5c974-5da9-4d8e-b4af-d0dcc8c358b1)


![image](https://github.com/supercompany-llc/backend/assets/35817574/73729731-8230-4368-9d6b-9e681a8a738f)



## Allocating Elastic IP to GPU instance, configure Network security settings.

**When we created an instance, its public ip address will be changed everytime we restart instance. We can create a ElasticIP and assign this IP to our server so that its ip address never change even if we restart it.**

**1. Go to "Elastic IPs", and select "Allocate ElasticIP address".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/48615ef1-1c42-41ca-ac71-a5c702c9586f)


**2. Select "Allocate" without any change.**


![image](https://github.com/supercompany-llc/backend/assets/35817574/59d6e1a9-cd75-4579-b853-88c84b0e6fa6)


**3. Select Elastic IP address that you just created, and click "Associate ElasticIP address"**


![image](https://github.com/supercompany-llc/backend/assets/35817574/ea83e389-4ef9-41ee-81b3-0a56664fb7e3)


![image](https://github.com/supercompany-llc/backend/assets/35817574/fc39e211-3759-4db8-b01f-3e3793312ea3)


**4. Select your GPU instance and click "Associate".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/f283cffc-03db-48f7-b08f-7707be462bcb)


**5. If you go back to "Instances", you will be able to see Elastic IP address is associated to your instance.**


![image](https://github.com/supercompany-llc/backend/assets/35817574/2021ad10-e70f-49c6-af18-96d02003b0ac)



**By default, server is only accessible through ssh. To enable specific port(port that our backend server and websocket server will listen on) from any ip address.**


**1. Select your instance and go to "Security", select "Security groups" link.**


![image](https://github.com/supercompany-llc/backend/assets/35817574/0657d3de-481b-49d3-9285-b3b65b20348a)


**2. Click "Edit inbound rules".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/dcf70496-9b72-4864-9722-fe08b046e00b)


**3. Click "Add rule", and input the port number you want to enable access, and select "Anywhere-IPv4" to allow access from any ip address, click "Save rules".**


![image](https://github.com/supercompany-llc/backend/assets/35817574/bb227fdd-23e3-4ce5-8ea7-afbaab44822b)



## Access GPU server through SSH

```ssh -i your-pem-file.pem ubuntu@<elastic-ip-address>```
