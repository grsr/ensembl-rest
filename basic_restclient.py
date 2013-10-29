import sys
import urllib2
import json

def perform_rest_action(endpoint, server='http://beta.rest.ensembl.org', hdrs=None):
    if hdrs is None:
        hdrs = {'Content-Type': 'application/json'}

    data = None

    try:
        request = urllib2.Request(server + endpoint, headers=hdrs)
        response = urllib2.urlopen(request)
        content = response.read()
        data = json.loads(content)
    except urllib2.HTTPError, e:
        sys.stderr.write('Request failed: Status code: {0.code} Reason: {0.reason}\n'.format(e))

    return data

def get_variants(species, symbol):
    genes = perform_rest_action('/xrefs/symbol/{0}/{1}?object_type=gene'.format(species, symbol))
    if genes:
        stable_id = genes[0]['id']
        variants = perform_rest_action('/feature/id/{0}?feature=variation'.format(stable_id))
        return variants
    return None

def run(species, symbol):
    variants = get_variants(species, symbol)
    if variants:
        for v in variants:
            print '{seq_region_name}:{start}-{end}:{strand} ==> {ID} ({consequence_type})'.format(**v);

if __name__ == '__main__':
    if len(sys.argv) == 3:
        species, symbol = sys.argv[1:]
    else:
        species, symbol = 'human', 'BRAF'

    run(species, symbol)

