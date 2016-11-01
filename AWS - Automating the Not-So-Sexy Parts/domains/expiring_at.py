import boto3

longest = 0;
data = {}

client = boto3.client('route53domains', region_name="us-east-1")

for domain in client.list_domains()['Domains']:
    if len(domain['DomainName']) > longest:
        longest = len(domain['DomainName'])
    data[domain['Expiry']] = {
        'name': domain['DomainName'],
        'expiry': domain['Expiry']
    }

print("{0: <{1}s} Expiry".format("Domain", longest))
print("{0:_<{1}s} {2: <{3}s} ______".format("", len("Domain"), "", longest - len("Domain") - 1))
for d in sorted(data.keys()):
    print("{0: <{1}s} {2}".format(data[d]['name'], longest, data[d]['expiry']))
