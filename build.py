#!/usr/bin/python
import re,os,shutil

BUILD_DIR='build'
configs={ 'CENTOS_VERSION': '7.2', 'CENTOS_VERSION_MINOR': '1511' } 

def parse_template_string(input_string,configs):
    pattern = re.compile('%%([A-Z_]+)%%')
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
    template_file('{}.{}'.format(base_file,'template'),'{}/{}'.format(BUILD_DIR,base_file),configs,['start.sh']) 

if __name__ == "__main__":
    main()
