# PaperBoy
A python script to deliver newsletters right into your kindle
## How it works
This scripts reads your emails within a certain Folder and converts them to an epub, and then sends it to a kindle e-mail. You can add it to a cron to have this process automated, you should also create some filters to automate the labeling on your e-mail.
## Setup
Take a look at `.env.example`, fill out the data and copy it to .env

You can create an app password for gmail by following [this guide](https://support.google.com/accounts/answer/185833?hl=en)

You must also get your kindle e-mail by following [this guide](https://www.amazon.com/sendtokindle/email)
## TODO
At this state this is just a proof of concept, here's some possible improvements
- [ ] Sanitize HTML, since epub readers are less forgiving than browsers
- [ ] Test with more newsletters
- [ ] Support for Kobo (Maybe trough google drive)
