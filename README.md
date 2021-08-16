# (WIP) bottle-oidc-example

This is a simple web application to show how to integrate the OIDC 
protocol to be able to use authentication and authorization in your own
web applications.

There are tons of plugins or packages that does this integration for you, but
sometimes you may just want to understand how the protocol works, so you can
implement your own package/library for other frameworks.

## Why bottle.py
Bottle is a web micro framework which let you set up web applications with minimal
lines of code. I decided to use this framework to focus on the OIDC integration instead
of the framework configuration. Once you understand how the protocol works it becomes
super easy to migrate the ideas to frameworks like Django or Flask.

## Running the app

To be able to use this application you need an identity provider (the server side of the oidc protocol).
In this example I use keycloak as the identity provider since it is open source and it is easy to set up 
locally, but the same principles work with providers like Okta, Auth0, etc.

To make things easier, there is a docker-compose file that will run keycloak together with a postgres database
with a single command:

```shell
docker-compose up -d
```

I am working on a blog entry to configure keycloak for this application. So I will not explain how to do that here.

At the end you just need to install dependencies and then run `main.py`

```shell
pip install -r requirements.txt
python main.py
```

