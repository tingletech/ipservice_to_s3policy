#!/bin/env python3
import argparse
import copy
import sys
import ipaddress
import json


# policy template to restrict access to a specific UC campus by IP address
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
    # lower case the short name of the campus between `(` and `)`
    name = name[name.index("(") + 1:name.rindex(")")].lower()
    ____ = next(lines)  # header line
    ranges = []
    # convert ranges in campus block to CIDR format
    for line in lines:
        ip_range = line.split(',')[:2]
        ranges.extend(parse_range(ip_range))
    return name, ranges


def parse_range(ip_range):
    """ parse the ipservice strings into a IPv4Network """
    return ipaddress.summarize_address_range(
        parse_ip_address(ip_range[0]),
        parse_ip_address(ip_range[1]), )


def parse_ip_address(x):
    """ parse ipservice ipaddress into IPv4Address """
    return ipaddress.ip_address('.'.join([str(int(z)) for z in x.split('.')]))


def update_policy(output, statement_template, name, ranges):
    """ update the policy with a statement for this campus
        `output` gets modified in place (side effects)
    """
    # make a copy of the policy statement that limits by IP
    statement = copy.deepcopy(statement_template)
    # condition for the tag
    statement["Condition"]["StringEquals"][
        "s3:ExistingObjectTag/campus"] = name
    statement_range = statement["Condition"]["IpAddress"]["aws:SourceIp"]
    # update ip address ranges in the policy
    for r in ranges:
        statement_range.append(str(r))

    # add the statement for this campus to the output
    output["Statement"].append(statement)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('csv')

    if argv is None:
        argv = parser.parse_args()

    file_name = argv.csv

    # load the template
    output = json.loads(POLICY_TEMPLATE)

    # pop out the statement from the policy template
    statement_template = output["Statement"].pop()

    # process the output file from ipservice
    with open(file_name, 'r') as open_file:
        txt = open_file.read()
        # split up input where it has blank lines
        blocks = iter(txt.split('\n\n'))
        ____ = next(blocks)  # skip the header block
        for campus in blocks:
            if len(campus) > 0:
                update_policy(output, statement_template, *
                              process_campus(campus))

    print(json.dumps(output, indent=4))


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
