# Logs

Laravel (and its ecosystem) don't seem to expect you to be running things outside of a single instance. So just writing a view that reads your logs into some sort of admin panel of your app doesn't really work. Also, you can't tune how noisy logs are in differently environments. Which means, you're going to have to use something like Logstash.

Logstash backends onto Elasticsearch, which AWS handily provides as a service ... but it doesn't have VPC support. This is annoying for a couple reasons; all your vpc security groups don't apply, and your traffic needs to exit your VPC to access it -- which is a chargable item.

For these reasons, we run our own Elasticsearch instance per 'environment'.

Tip: Exceptions in (production) logs are broken windows. Every ERROR that lands in production ends up producing an email to us. And gets addressed. It was painful originally, but only because we had let the windows stay broken for awhile.
