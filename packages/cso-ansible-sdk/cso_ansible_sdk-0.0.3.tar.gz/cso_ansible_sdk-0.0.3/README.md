# Ansible SDK for Juniper's CSO

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/3/31/Juniper_Networks_logo.svg)](https://www.juniper.net/us/en/products-services/sdn/contrail/contrail-service-orchestration/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

`cso_ansible_sdk` is an easier way to interact with Juniper's Contrail Service Orchestrator for building out SD-WAN sites.

  - ease the authentication process with CSO for tokens
  - build out new SD-WAN sites
  - delete active SD-WAN sites
  - retrieve statistics from your production SD-WAN environment

# New Features!

  - Building out a full SD-WAN site through Ansible with this SDK


> this SDK is to be installed on your Ansible Tower instance
> it is meant to be leveraged by the CSO galaxy modules

### Dependencies

`cso_ansible_sdk` uses a single open source project to work properly:

* [requests](https://pypi.org/project/requests/) - interact with REST APIs

### Installation

Python packages are installed with the pip command

```sh
$ pip install cso_ansible_sdk
```



### Development

Want to contribute? Great!

Submit a PR and let's work on this together :D 