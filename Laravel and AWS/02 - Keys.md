# Keys

/Heuristic/ - If you are putting an IAM key somewhere in your infrastructure, you're likely doing something wrong. (Use IAM Roles instead)

/Rule/ - Root account should never, ever, ever have an key

AWS suggests the following steps to rotate keys (which you really should practice doing for when you accidently publish your key to github or such)
- Create a second access key in addition to the one in use.
- Update all your applications to use the new access key and validate that the applications are working.
- Change the state of the previous access key to inactive.
- Validate that your applications are still working as expected.
- Delete the inactive access key.