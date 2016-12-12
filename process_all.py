import ipaddress


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
        parse_ip_address(ip_range[0]), parse_ip_address(ip_range[1]),)


def parse_ip_address(x):
    """ parse ipservice ipaddress into IPv4Address """
    return ipaddress.ip_address(
        '.'.join( [ str(int(z)) for z in x.split('.') ] ))

file_name = "TEST.csv"
with open(file_name, 'r') as open_file:
    txt = open_file.read()
    items = iter(txt.split('\n\n'))
    ____ = next(items)  # skip the header block
    for campus in items:
        if len(campus) > 0:
            process_campus(campus)

