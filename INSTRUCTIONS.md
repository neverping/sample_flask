# INSTRUCTIONS

Below are the instructions of how to setup this project in your computer.

## INSTALLATION PROCEDURES

The setup process covers Ubuntu based distributions such as the own Ubuntu or LinuxMint, but I will cover Mac OSX as well.

### Ensure you have pip, virtualenv and virtualenv-wrapper installed:

Pip is a Python package management and helps you to install, update and remove Python libraries with a single command line tool.

Virtualenv is a tool to create isolated Python environment. It helps you out to create multiple Python environments and guarantees you don't mix-up different libraries with different projects.

Virtualenvwrapper, finally, helps you by creating command line tools for easily managing different Python virtualenvs.

On an Ubuntu system, you can install everything using the following command:

`sudo apt-get install python-virtualenv virtualenvwrapper virtualenv python-pip`

On a Mac, the best solution is by installing Homebrew first, which is a package manager to OSX and helps you to install, update and remove development software as well other open source system packages. However, since there are several steps to follow, I recommend you to read <a href="https://medium.com/@briantorresgil/definitive-guide-to-python-on-mac-osx-65acd8d969d0">this guide</a>, which will cover almost everything you need to know.

### Installing Python packages for the project:

After installing Python, pip, Virtualenv and Virtualenvwrapper, it's time to set your own python environment for this project. Start it by creating a new virtualenv:

```bash
$ mkvirtualenv sample_flask
```

The output will be something like this and your shell environment will also automatically switch your Python path to the newly one created.


```bash
Running virtualenv with interpreter /usr/bin/python2
New python executable in /home/user/.virtualenvs/sample_flask/bin/python2
Also creating executable in /home/user/.virtualenvs/sample_flask/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
(sample_flask) user@host:~/somedir $
```

Now it's time to install required packages using pip:


```bash
$ pip install -r dev_requirements.txt
```

## TESTING

The project is covered by pytest suite, and you can run it to check whether if the project is working properly or needs fixes as you keep adding features in the code.

### Running tests:

After you installed the required packages, you can invoke the tests as follows:

```bash
$ pytest -v
```

### Running the project locally:

To run the project locally, you can use this bash script below:

```bash
$ ./run.sh
```

Flask will run using a loopback addresss (127.0.0.1 or localhost), and you can access the app using a web browser at `http://127.0.0.1:5000/`.

## DEPLOYING

Right now you can deploy to Amazon Web Services (AWS) using Amazon's Elastic Beanstalk (EB). Amazon EB is a simple PaaS solution to deploy code and run within AWS cloud.

To use this public cloud provider, you must create an <a href="https://portal.aws.amazon.com/billing/signup#/start">AWS account</a> and associate it with a Credit Card in case you never done it before. Charges may apply if you leave the instance running for over 10 minutes. Under this time, it will be free for a year for a quick setup and destroy. If you already have an AWS account or finished creating your account, let's prepare your environment to use EB.

### Deploying to Amazon Elastic Beanstalk using EB client

If you created your virtualenv and installed the packages by running `pip install -r dev_requirements.txt`, the EB client will be already installed. You can check if it is working by running the following command (versions may differ, but it won't be an issue at all). 

```bash
$ eb --version
EB CLI 3.14.6 (Python 2.7.1)
```

Now it is time to setup your project name inside EB and select the closest region for you. Here are the closest regions for Melbourne: `ap-southeast-2` (Asia-Pacific - Sydney), and `ap-southeast-1` (Asia-Pacific - Singapoure).

In our example, we will choose 'polls' as our app name, Python 3.6 (the app is Python 2.x and 3.x compatible), and 'Sydney' region: 

```bash
$ eb init -p python-3.6 polls --region ap-southeast-2
```

EB client will ask you to fill the following details below:

```bash
You have not yet set up your credentials or your credentials are incorrect 
You must provide your credentials.
(aws-access-id): 
(aws-secret): 
```

You need to create your AWS Client credentials in order to continue. Please visit this <a href="https://console.aws.amazon.com/iam/home?region=ap-southeast-2#/security_credential">page over here</a>, click on Access Keys, press "Create New Access Key". If you already have this key, please use it to create your app. 

NOTE: Be aware the acccess key has, BY DEFAULT, access to ALL AWS resources. On the other hand, if you already have credentials from a corporate AWS acccounts, check with your system administrator if your issued key has permissions to create and manage EB apps.

After configuring your AWS key, it is time to create the app inside your region, deploy it and access it. This might take a couple of minutes.

```bash
(previous command will return this)
Application polls has been created.

$ eb create polls
Creating application version archive "app-5123-181115_212303".
Uploading polls/app-5123-181115_212303.zip to S3. This may take a while.
Upload Complete.
Environment details for: polls
  Application name: polls
  Region: ap-southeast-2
  Deployed Version: app-5123-181115_212303
  Environment ID: e-ei7XXXXXX
  Platform: arn:aws:elasticbeanstalk:ap-southeast-2::platform/Python 3.6 running on 64bit Amazon Linux/2.7.5
  Tier: WebServer-Standard-1.0
  CNAME: UNKNOWN
  Updated: 2018-11-15 23:23:14.878000+00:00
Printing Status:
2018-11-15 23:23:14    INFO    createEnvironment is starting.
2018-11-15 23:23:15    INFO    Using elasticbeanstalk-ap-southeast-2-3XXXXX as Amazon S3 storage bucket for environment data.
(...)
2018-11-15 23:25:59    INFO    Application available at polls.XXXXXXXX.ap-southeast-2.elasticbeanstalk.com.
2018-11-15 23:26:00    INFO    Successfully launched environment: polls
```

When the environment creation process completes, it is time to check it out!

```bash
$ eb open
```

This will open a browser window using the domain name created for your application. You should see the same Flask website that you created and tested locally. 

After evaluating the app, you should terminate it as soon as you can, as charges may apply. For that, you type `eb terminate polls` (as 'polls' being the app name you choose to create). AWS will ask you to confirm this operation by typing the app name again. Below is the logging example that will be shown to you.


```bash
$ eb terminate polls
The environment "polls" and all associated instances will be terminated.
To confirm, type the environment name: polls
2018-11-15 23:26:56    INFO    terminateEnvironment is starting.
(...)
2018-11-15 23:31:38    INFO    Deleting SNS topic for environment polls.
2018-11-15 23:31:40    INFO    terminateEnvironment completed successfully.
                                

```
AWS will keep all your deployed zip files into AWS S3, which stands for Simple Storage Service. You must manually delete it to avoid charges in your credit card. You can access it from <a href="https://s3.console.aws.amazon.com/s3/home?region=ap-southeast-2">here</a>. The correct bucket you need to delete it will be shown at the app creation time. You can spot it something such as ` Using elasticbeanstalk-ap-southeast-2-347XXX as Amazon S3 storage bucket for environment data`. Following this example, you need to navigante inside bucket  `elasticbeanstalk-ap-southeast-2-347XXX`, then 'polls' directory and you see a list of zip files. Mark the checkbox on each of these zip files, and then at 'actions' button, select 'delete' and then click on 'delete' again to confirm.

After the termination, AWS will remove everything it was needed to create our sample app, with the exception of the S3 objects we just deleted. This will ensure we won't be charged for any services left unused.

### Deploying to Vagrant 

Vagrant is an open source project aimed to manage guest virtual machines with simplicity, by reducing time to create, configure and destroying them. Vagrant makes virtualization simple, as it download boxes (virtual machines ready to be used into Vagrant) directly from the Vagrant community and you don't need to worry to install them and configure them. Of course, you can use configuration management tools such as Puppet, Ansible, and Chef to configure your projects, and this project uses Ansible to setup our project inside the virtual machine.

The idea of running this app inside Vagrant is to show my skills using configuration management tools such as Ansible.

Vagrant supports Oracle Virtual Box, Microsoft Hyper-V, and Docker as a type-2 hypervisor. A type-2 hypervisor is a software designed to run guest machines within a operating system, such as Windows, Linux or OSX. I choose Oracle VirtualBox to be the most popular choice among developers and to be free.

As Flask is in auto-reload mode, you don't need to restart or redeploy the app in order to see the modifications inside Vagrant. You can edit the code inside this git repository and it will be reflected into the guest machine.

To setup Vagrant at your computer, we use a configuration file called 'Vagrantfile'. This file will instruct Vagrant how to work with our guest machine.

This Vagrantifle was configured to run using Vagrant 2.0.2 or newer. This won't work with older Vagrant version, but it can be downgraded later if needed, although it is not recommended, since it uses an old syntax and it is deprecated.

If you don't have Vagrant installed, you can download Vagrant from <a href="https://www.vagrantup.com/">here</a> if you are a OSX user. If you are using Ubuntu, just run `sudo apt-get install vagrant`

As mentioned before, all the setup was done using the Virtualbox. You can download Virtualbox from <a href="https://www.virtualbox.org/">here</a> if you are a OSX user. If you are using Ubuntu, just run `sudo apt-get install virtualbox`

This vagrant is using Ubuntu 16.04 LTS / Xenial Xerus box. Vagrant will download the correct virtual machine to you and set it up using Ansible automatically.

OK, finally! Time to setup the virtual machine at your computer! No secrets at all! Just fire it up by invoking:

`$ vagrant up`

This will download a Ubuntu directly from the internet, it will set it up (vagrant calls it 'provision'). The output will be similar as follows:

```bash
$ vagrant up
$ vagrant up
Bringing machine 'ubuntu' up with 'virtualbox' provider...
==> ubuntu: Importing base box 'ubuntu/xenial64'...
(...)
==> ubuntu: Running provisioner: ansible...
    ubuntu: Running ansible-playbook...

PLAY [configuration for ubuntu] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [ubuntu]

TASK [ubuntu : Installing nginx] ***********************************************
changed: [ubuntu]

(...)

PLAY RECAP *********************************************************************
ubuntu                     : ok=22   changed=19   unreachable=0    failed=0   
```

And we see the setup is completed. After that, you can open the browser to the following address: `http://192.168.123.101/

To stop the virtual machine, type `vagrant stop`; and to destroy the virtual machine, `vagrant destroy`.
