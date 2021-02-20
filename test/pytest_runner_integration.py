import requests
import subprocess
import time
import yaml

print("Building SAM test environment...")
process = subprocess.Popen(
    ['/usr/local/bin/sam', 'build', '--use-container', '-b', '../sam-build', '-t', 'sam-integration-test.yaml', '>',
     'samtest_results/output.txt']
)
print("SAM test environment built.")
process.terminate()

integration_test_yaml_file = open('sam-integration-test.yaml')
parsed_yaml_file = yaml.load(integration_test_yaml_file, Loader=yaml.FullLoader)
integration_test_yaml_file.close()

test_scenarios = parsed_yaml_file['Resources']
for scenario in test_scenarios:
    if test_scenarios[scenario]['Type'] == 'AWS::Serverless::Application':
        test_properties = test_scenarios[scenario]['Properties']
        template_file = test_properties['Location']
        if 'Parameters' in test_properties.keys():
            test_parameters = test_properties['Parameters']
            test_name = test_parameters['TestName']
            test_type = test_parameters['TestType']
            test_event = test_parameters['Test1']
            if test_type == 'API':
                f = open('samtest_results/output.txt', 'a')
                process = subprocess.Popen(['sam', 'local', 'start-api', '-t', template_file], stdout=f)
                time.sleep(5)
                requests.get('http://127.0.0.1:3000/', timeout=30)
                process.terminate()
                f.flush()
                f.close()
            elif test_type == 'EVENT':
                f = open('samtest_results/output.txt', 'a')
                f.write(test_name + " STARTING........\n")
                process = subprocess.Popen(['sam', 'local', 'invoke', '-e', test_event, '-t', template_file], stdout=f)
                time.sleep(5)
                f.write(test_name + " COMPLETE........\n")
                f.write("\n")
                f.flush()
                f.close()
            else:
                continue
