# ALB

/Heuristic/ - The only items that should be able to be reached from the great unwashed internets are load balancers (Elastic - ELB, or Application - ALB).

Why?
## 'security through obscurity'
* AWS manages whatever the ALB is running on so one less thing you need to worry about
* Can whitelist ports, and origins
* All instances you control can be in 'private' subnets with no external routable IP Address

## elasticity
* All your DNS needs to know is the ALB and doesn't care if there is 1 or 1000 instances behind it

Tip: Use AWS Route 53 to resolve DNS to ALB using their 'alias' functionality

## HTTPS termination
* There is no reason not to run HTTPS on all your properties today

Tip: Use HTTPS Certificates from AWS Certificate Manager in your ALB to terminate the connection. They will auto-renew so you never have to worry about browsers complaining because you forgot to renew your cert. (Which has never happened, to anyone, ever)

Note: AWS ALBs support HTTP2 and will claim they are running it to your client. But if your communication from the ALB to Nginx is HTTP -- are you really doing HTTP2?

## Left Right
* ALBs can redirect based on the URI traffic different directions

Note: You really needed to plan your routes properly in order to make full use of this
