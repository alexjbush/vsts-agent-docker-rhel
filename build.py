#!/usr/bin/python
import re,os,shutil

BUILD_DIR='build'
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

def template_file(input_filename, templated_output_filename, configs,assets=[]):
    input_path = os.path.dirname(input_filename)
    output_filename = parse_template_string(templated_output_filename,configs)
    output_path = os.path.dirname(output_filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        outfile.write(parse_template_string(infile.read(),configs))
    for asset in assets:
        shutil.copyfile('{}/{}'.format(input_path,asset),'{}/{}'.format(output_path,asset))
    

def main():
    base_file='centos/%%CENTOS_VERSION%%/Dockerfile'
    template_file('{}.{}'.format(base_file,'template'),
                  '{}/{}'.format(BUILD_DIR,base_file),
                  configs,
                  ['start.sh']) 
    base_file='centos/%%CENTOS_VERSION%%/docker/%%DOCKER_VERSION%%/Dockerfile'
    template_file('{}.{}'.format(base_file,'template'),
                  '{}/{}'.format(BUILD_DIR,base_file),
                  dict(configs,BASE_IMAGE_TAG='centos-7.2')) 
    base_file='centos/%%CENTOS_VERSION%%/docker/%%DOCKER_VERSION%%/standard/Dockerfile'
    template_file('{}.{}'.format(base_file,'template'),
                  '{}/{}'.format(BUILD_DIR,base_file),
                  dict(configs,BASE_IMAGE_TAG='centos-7.2-docker-1.13.1',OPENJDK_VERSION='1.8.0')) 
    base_file='centos/%%CENTOS_VERSION%%/docker/%%DOCKER_VERSION%%/standard/oraclejdk/%%ORACLE_JDK_VERSION%%/Dockerfile'
    oracle_vers='1.8.0_60'
    template_file('{}.{}'.format(base_file,'template'),
                  '{}/{}'.format(BUILD_DIR,base_file),
                  dict(configs,BASE_IMAGE_TAG='centos-7.2-docker-1.13.1-standard',
                       ORACLE_JDK_VERSION=oracle_vers, ORACLE_JDK_REPO_URL=oracle_url_map['1.8.0_60'])) 

if __name__ == "__main__":
    main()
