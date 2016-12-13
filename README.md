Converts output from CDL's internal ipservice into a bucket policy for Amazon S3

Uses S3's new "tags" -- set a tag such as "campus=ucx" to allow access to UCX

TEST.csv is an example of the report format I can get from the internal CDL service

TODO; make is so the Resource is not hardcoded

TODO; make is so that the bucket policy gets automatically updated / applied to bucket

TODO; use ipservice API?

TODO; IPv6?
