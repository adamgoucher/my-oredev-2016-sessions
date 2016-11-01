# SES

(I'm still working on this one as I just encountered it.)

SES works with IAM Roles right out of the box with modern Laravel. But. A commit in February of this year made it a lot more of a headache to do well, and at scale.

AWS will happily tell you the Request Id and Message Ids of things you tell it to send, but the SesTransport class quietly swallows this information. You /really/ want this information. Why? Because AWS wants to tell you when there is a bounce or complaint around your message. (In fact, so get out of their sandbox you have to tell them you have a solution for this.)

If you are using SES to send mail, you need to do the following;
- implement your own Transport that doesn't swallow the SES response
- get that response anytime you call Mail::send()
- write that id to a table somewhere
- write an endpoint that takes SES notifications and updates records accordingly
- figure our your organization's rules around notifications
- wire SES to publish to SNS which gets read by Lambda which POSTs the notification to the server.

