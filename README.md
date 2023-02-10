
# Ansible Role:  `tomcat`

Download an Tomcat archive for a war based CoreMedia deployment.

Also used for the jolokia monitoring Tool.

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-tomcat/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-tomcat)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-tomcat)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-tomcat/actions
[issues]: https://github.com/bodsch/ansible-tomcat/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-tomcat/releases
[quality]: https://galaxy.ansible.com/bodsch/tomcat



## Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.10
    

## usage

```yaml

tomcat_version: 9.0.14

tomcat_download_mirror: "https://archive.apache.org/dist/tomcat/tomcat-{{ tomcat_major_version }}/v{{ tomcat_version }}"

tomcat_user:
  username: tomcat
  group: tomcat
  home_directory: /opt/tomcat

tomcat_remove_webapps:
  - docs
  - examples
  - host-manager
  - manager
  - ROOT

tomcat_service:
  enabled: false
```


----

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
