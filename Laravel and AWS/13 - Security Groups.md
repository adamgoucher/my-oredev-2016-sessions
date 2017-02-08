# Security Groups

*Tip* - Have a naming convention. Include things like Region in it.

My philosophy around SGs is evolving. A number of sites suggest a 'tier' approach, but that starts to get difficult when a box has more than one tier as non-production ones sometimes do.

This is where I am currently heading;
* Each environment has a 'common' SG which has SSH constrained to the VPN assigned address range. (There should only be 1 box which can be externally ssh-ed into and that's the VPN appliance.)
* Each app has a SG per environment
* Each environment has an 'infrastructure' specific SG for things that are not yet hosted by AWS
