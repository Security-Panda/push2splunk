# push2splunk

This my attempt to ease my own pain of uploading Lookup files manually on SplunkCloud.

It allows you to upload a group of CSV files located in a folder (lookupfiles) to your SplunkCloud instance. 


It uses the search as mentioned in the Splunk Answers here:
https://answers.splunk.com/answers/152485/can-you-create-modify-a-lookup-file-via-rest-api.html

The additional features of this python implementation are:
- Multiple CSV file uploads
- Auto header extraction
- Error handling on parsing of CSV files
- Apply proxy if needed