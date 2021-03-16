def print_classification(input, classification, displace):
    if 'name' in classification:
        input += displace + '- ' + classification['name'] + '(' + classification['slug'] + ')' + '\n'
    else:
        print('oups', classification)
    if 'children' in classification:
        input += ''.join(map(lambda c : print_classification('', c, displace + '  '), classification['children']))
    return input;

