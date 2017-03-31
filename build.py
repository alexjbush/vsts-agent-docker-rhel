#!/usr/bin/python
import re,os,shutil

BUILD_DIR='build/'
SRC_DIR='src/'
configs={ 'CENTOS_VERSION': '7.2', 
          'CENTOS_VERSION_MINOR': '1511',
          'DOCKER_REPO': 'bushnoh/vsts-agent-docker-rhel',
          'DOCKER_VERSION': '1.13.1',
          'DOCKER_SHA256': '97892375e756fd29a304bd8cd9ffb256c2e7c8fd759e12a55a6336e15100ad75',
          'DOCKER_COMPOSE_VERSION': '1.11.2' }
oracle_url_map={ '1.8.0_60': 'http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jdk-8u60-linux-x64.rpm' }

def parse_template_string(input_string,configs):
    pattern = re.compile('%%([0-9A-Z_]+)%%')
    output_string = input_string
    for match in pattern.findall(input_string):
        if match not in configs.keys():
            raise KeyError('Template variable %%{}%% not found in list'.format(match))
        output_string = re.sub('%%{}%%'.format(match),configs[match],output_string)
    return output_string

def template_file(src_tag, base_tag='', configs={},assets=[]):
    input_path = SRC_DIR+src_tag+'/'
    new_tag = src_tag if not base_tag else base_tag+'-'+src_tag
    output_path = parse_template_string(BUILD_DIR+new_tag+'/',configs)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(input_path+'Dockerfile.template', 'r') as infile, open(output_path+'Dockerfile', 'w') as outfile:
        outfile.write(parse_template_string(infile.read(),dict(configs,BASE_IMAGE_TAG=base_tag)))
    for asset in assets:
        shutil.copyfile('{}/{}'.format(input_path,asset),'{}/{}'.format(output_path,asset))
    

def main():
    template_file('centos-%%CENTOS_VERSION%%',
                  configs=configs,
                  assets=['start.sh']) 
    template_file('docker-%%DOCKER_VERSION%%',
                  'centos-7.2',
                  configs)
    template_file('standard',
                  'centos-7.2-docker-1.13.1',
                  dict(configs,
                       OPENJDK_VERSION='1.8.0',
                       GIT_VERSION='2.12.2')) 
    template_file('oracle-%%ORACLE_JDK_VERSION%%',
                  'centos-7.2-docker-1.13.1-standard',
                  dict(configs,
                       ORACLE_JDK_VERSION='1.8.0_60',
                       ORACLE_JDK_REPO_URL=oracle_url_map['1.8.0_60'])) 
    template_file('ansible-%%ANSIBLE_VERSION%%',
                  'centos-7.2-docker-1.13.1',
                  dict(configs,
                       ANSIBLE_VERSION='v2.3.0.0-0.2.rc2',
                       GIT_VERSION='2.12.2'))

if __name__ == "__main__":
    main()
