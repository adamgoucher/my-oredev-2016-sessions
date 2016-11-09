import requests
from io import BytesIO
import gzip
import re
import sys

available = 0

def get_hosted_version(release):
    r = requests.get('http://10.0.1.88/dists/%s/main/binary-i386/Packages.gz' % release, stream=True)
    packages = gzip.GzipFile(fileobj=BytesIO(r.raw.read()))
    # break into individual package sections
    split_packages = str(packages.read(), 'utf-8').strip().split('\n\n')
    print(split_packages)
    versions = []
    for section in split_packages:
        name = re.search('^Package: (.*)\\n', section).group(1)
        if name == 'codedeploy-agent':
            version = re.search('Version: (.*)\\n', section).group(1)
            versions.append(version)
    return versions

def get_aws_version():
    r = requests.get('https://aws-codedeploy-us-west-2.s3.amazonaws.com/latest/VERSION')
    j = r.json()
    return re.search('_(.*)_', j['deb']).group(1)

def report(release, us, them):
    print(release.title())
    print('-' * len(release))
    us.sort()
    if them > us[0]:
        global available
        available += 1
        print('%s is available from aws' % them)
    else:
        print('no updates')
    print('')

precise = get_hosted_version('precise')
trusty = get_hosted_version('trusty')
xenial = get_hosted_version('xenial')
current = get_aws_version()
print('Current hosted package versions vs AWS versions')
print('')
report('precise', precise, current)
report('trusty', trusty, current)
report('xenial', xenial, current)

sys.exit(available)
