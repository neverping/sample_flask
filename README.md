# Simple Flask application running on Vagrant

Greetings!

This web application was written using <a href="http://flask.pocoo.org/docs/1.0/">Flask</a>. <a href="http://flask.pocoo.org/docs/1.0/">Flask</a> is a very simple micro web framework written in Python designed to help developers to create small applications and APIs.

This PoC was all written in Python 2.7, but it should work well with Python 3.x for Development usage. Unfortunately, because of MySQL - Python, we cannot use under Python 3 inside Vagrant (but in your local enviroment will be ok, as we use sqlite3 as database). This app is a partial fork of <a href=" https://github.com/kalise/flask-vote-app/">Flask Voting App</a>, but unfortunately the app didn't provide any test suite, so I have to create one and also adept to work within Vagrant.

Below is a link with full instructions describing the steps to run this project:

- [Instructions](INSTRUCTIONS.md) 
- [Issues](ISSUES.md) 
