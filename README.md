# CoreMedia - tomcat

Download an Tomcat archive for a war based CoreMedia deployment.

Also used for the jolokia monitoring Tool.

## supported and tested distributions

- CentOS 7 / 8
- debian 9 / 10
- ubuntu 18.04

## config parameters

```
tomcat_version: 9.0.8

tomcat_major_version: "{{ tomcat_version.split('.')[0] }}"

tomcat_download_dir: "https://archive.apache.org/dist/tomcat/tomcat-{{ tomcat_major_version }}/v{{ tomcat_version }}"

# https://archive.apache.org/dist/tomcat/tomcat-9/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz
tomcat_download_url: "{{ tomcat_download_dir }}/bin/apache-tomcat-{{ tomcat_version }}.tar.gz"
tomcat_extra_jmx_url: "{{ tomcat_download_dir }}/bin/extras/catalina-jmx-remote.jar"

# only for coremedia related applications
# not needed for spring-boot applications!
tomcat_coremedia_files: {}
# tomcat_coremedia_files:
#   - { src: 'coremedia-tomcat.jar', checksum: 'accc2b68f38dced4a804d32a0c4939a84183fda2' }
#
# tomcat_coremedia_artefact_url: "{{ artefact_server }}/{{ application_version }}"
```
