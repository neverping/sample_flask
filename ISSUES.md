# ISSUES

Here is a list of errors you might encounter:

### You tried to execute run.sh but it didn't start the app

After you run `run.sh`, you experience the following error:

```bash
Usage: flask run [OPTIONS]

Error: The file/path provided (polls) does not appear to exist.  Please verify the path is correct.  If app is not on PYTHONPATH, ensure the extension is .py
```

Here are the following reasons:

1- You have flask installed, but you didn't switch to the correct virtualenv:

Maybe you are using a different virtualenv, so the best approach is switch to the correct virtualenv. Here are the steps below:

```bash
$ deactivate
$ workon sample_flask
$ pip install -r requirements.txt
```

After that, please try again by running `$ ./run.sh` once again.

### After creating the app on AWS Beanstalk, it throws an error about the ssh file.

If you experience an error like the following below:

```bash
$ eb create polls
Creating application version archive "app-51c9-180913_224858".
Uploading polls/app-51c9-180913_224858.zip to S3. This may take a while.
Upload Complete.
ERROR: NotSupportedError - The EB CLI cannot find your SSH key file for keyname "your-ssh-keyname". Your SSH key file must be located in the .ssh folder in your home directory.
```

It means you tried to create your app in a different AWS region you previously used before.
Just copy the ssh key file (usually in PEM format) into your `~/.ssh` dir. This file is PER AWS REGION and that's why the eb client is complaining in this case.

This file you only generate ONCE at AWS. If you lost it, you need to <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html">regenerate it again</a>.
