import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    print(ansible_vars)

    return ansible_vars


def test_tmp_directory(host, get_vars):
    dir = host.file(get_vars['deployment_tmp_directory'])
    assert dir.exists
    assert dir.is_directory


@pytest.mark.parametrize("files", [
    "catalina-jmx-remote.jar",
    "coremedia-tomcat.jar",
])
def test_files(host, get_vars, files):
    dir = host.file(get_vars['deployment_tmp_directory'])
    f = host.file("%s/%s" % (dir.linked_to, files))
    assert f.exists
    assert f.is_file
