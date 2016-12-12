#!/bin/env python3
import argparse
import sys
import ipaddress


POLICY_TEMPLATE = """
{
    "Version": "2012-10-17",
    "Id": "RestrictToUCbyTag",
    "Statement": [ {
        "Sid": "IPAllow",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::ucldc-export/ip_restrict/*",
        "Condition": {
            "StringEquals": {
                "s3:ExistingObjectTag/campus": "ucr"
            },
            "IpAddress": {
                "aws:SourceIp": []
            }
        }
    } ]
}
"""


def process_campus(campus):
    """ parse a block out of the file """
    lines = iter(campus.split('\n'))
    name = next(lines)  # line with name of campus
    ____ = next(lines)  # header line
    for line in lines:
        ip_range = line.split(',')[:2]
        print(list(parse_range(ip_range)))


def parse_range(ip_range):
    """ parse the ipservice strings into a IPv4Network """
    return ipaddress.summarize_address_range(
        parse_ip_address(ip_range[0]),
        parse_ip_address(ip_range[1]), )


def parse_ip_address(x):
    """ parse ipservice ipaddress into IPv4Address """
    return ipaddress.ip_address('.'.join([str(int(z)) for z in x.split('.')]))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('csv')

    if argv is None:
        argv = parser.parse_args()

    file_name = argv.csv
    with open(file_name, 'r') as open_file:
        txt = open_file.read()
        items = iter(txt.split('\n\n'))
        ____ = next(items)  # skip the header block
        for campus in items:
            if len(campus) > 0:
                process_campus(campus)

# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())


"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
