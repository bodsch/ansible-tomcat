
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    """
        get molecule directories
    """
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """
      parse ansible variables
      - defaults/main.yml
      - vars/main.yml
      - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    """
        return local fact
    """
    return host.ansible("setup").get("ansible_facts").get("ansible_local").get("tomcat")


def test_fact_file(host):
    """
      check created ansible facts
    """
    f = host.file("/etc/ansible/facts.d/tomcat.fact")
    assert f.exists
    assert f.is_file


def test_tmp_directory(host, get_vars):
    """
      test remote deployment directory
    """
    dir = host.file(get_vars.get('deployment_tmp_directory'))

    assert dir.exists
    assert dir.is_directory


def test_files(host, get_vars):
    """
      test jmx-remote.jar
    """
    facts = local_facts(host)

    major_version = int(facts.get("version").get("major"))
    patch_version = int(facts.get("version").get("patch"))

    f = host.file(
      "{0}/catalina-jmx-remote.jar".format(
        get_vars.get('deployment_tmp_directory')))

    if(major_version <= 9 and patch_version <= 14):
        assert f.exists
        assert f.is_file
    else:
        assert not f.exists


def test_tomcat_version_link(host, get_vars):
    """
      tomcat version
    """
    d = host.file(
      "{0}/{1}".format(
        get_vars.get('tomcat_user').get('home_directory'),
        get_vars.get('tomcat_version')))

    assert d.exists
    assert d.is_symlink


def test_tomcat_webapps(host, get_vars):
    """

    """
    version = get_vars.get('tomcat_version')
    install_path = get_vars.get('tomcat_user').get('home_directory')
    webapps = get_vars.get('tomcat_remove_webapps')

    for w in webapps:
        directory = "{0}/{1}/webapps/{2}".format(install_path, version, w)

        d = host.file(directory)
        assert not d.exists
