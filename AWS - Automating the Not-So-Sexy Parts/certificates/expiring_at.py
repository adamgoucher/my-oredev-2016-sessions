import boto3

longest = 0;
data = {}

client = boto3.client('iam')

for certificate in client.list_server_certificates()['ServerCertificateMetadataList']:
    if len(certificate['ServerCertificateName']) > longest:
        longest = len(certificate['ServerCertificateName'])
    data[certificate['Expiration']] = {
        'name': certificate['ServerCertificateName'],
        'expiry': certificate['Expiration']
    }

print("{0: <{1}s} Expiry".format("Certificate", longest))
print("{0:_<{1}s} {2: <{3}s} ______".format("", len("Certificate"), "", longest - len("Certificate") - 1))
for d in sorted(data.keys()):
    print("{0: <{1}s} {2}".format(data[d]['name'], longest, data[d]['expiry']))
