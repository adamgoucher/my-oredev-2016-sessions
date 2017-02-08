# SES

SES works with IAM Roles right out of the box with modern Laravel. But in order to be using SES you must be running at least 5.3.23.

AWS will happily tell you the Request Id and Message Ids of things you tell it to send, but the SesTransport class quietly swallows this information. You /really/ want this information. Why? Because AWS wants to tell you when there is a bounce or complaint around your message. (In fact, so get out of their sandbox you have to tell them you have a solution for this.)

If you are using SES to send mail, you need to either use [MailTracker](https://github.com/jdavidbakr/mail-tracker) as is, or use it as an example to build your own Swiftmailer plugin (which is what we are doing). Our email flow has become
- mail gets queued
- *beforeSendPerformed* is fired which associates a guid onto the email message in the database
- email is sent, which sets an X-SES-Message-ID header on the message object
- *sendPerformed* is fired which looks up the message by the guid and sets the SES Message Id on the record
- when AWS needs to tell us about a bounce or other status, it drops it on AWS SNS where AWS Lambda will POST back to an endpoint on our side which will set the status
