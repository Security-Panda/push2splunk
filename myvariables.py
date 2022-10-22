class CSVvariables:
    FolderPath="<folder location for CSV lookup files to upload>"

class SplunkVariables:
        SplunkURL="https://<splunk URL>:8089"
        SplunkLookupURL = "/services/properties/lookups"
        SplunkSearchURL = "/services/search/jobs"
        SplunkAPIUser = "<Splunk API user to authenticate>" #Note that this user requires the 'api management' role and also requires access to internal and non internal indexers
        SplunkAPIpass = "<Base64 encoded splunk API user's password>" #Hard coded password, I know! I know! :(
        Proxy_host = "<zproxy.company.net>"
        Proxy_port = 80
