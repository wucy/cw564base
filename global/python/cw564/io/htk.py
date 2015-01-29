import re

def is_void_line(line):
    return len(line) == 0 or line.startswith('#') or line == '\n'


def read_scp(scp_fn):
    ret = dict()
    text = open(scp_fn, 'r')
    for line in text:
        if is_void_line(line):
            continue
        splits = re.split('\.', line)
        header = splits[0]
        ret[header] = line.strip()
    return ret

def write_scp(out_fn, scp_dict, order = None):
    if order == None:
        order = list(scp_dict.keys())

    out = open(out_fn, 'w')
    for key in order:
        out.write(scp_dict[key] + '\n')

    out.close()

def read_mlf(mlf_fn):
    ret = dict()
    text = open(mlf_fn, 'r')
    header = None
    content = None
    for line in text:
        if is_void_line(line):
            continue
        if line.strip() == '.': #last line of a lab file
            continue
        if line.startswith('"'):
            if header != None:
                ret[header] = content
            header = line.split('.')[0][1:]
            content = list()
            continue
        content.append(line.strip())
    ret[header] = content #for the last lab file
    return ret

def write_mlf(out_fn, mlf_dict, order = None):
    if order == None:
        order = list(mlf_dict.keys())

    out = open(out_fn, 'w')
    out.write('#!MLF!#\n')
    for key in order:
        out.write('"' + key + '.lab"\n')
        for line in mlf_dict[key]:
            out.write(line + '\n')
        out.write('.\n')

    out.close()


