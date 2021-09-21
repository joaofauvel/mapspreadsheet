from places.search import mass_search
import sys
import os
import json
import argparse


def _exec_queries_list(queries, key, pages, details):
    places = []
    for q in queries:
            if q == '':
                continue
            places.extend(mass_search(q, key, pages, details))
    return places


def exec_queries(queries, key, pages, details):
    if isinstance(queries, list):
        places = _exec_queries_list(queries, key, pages, details)
    elif isinstance(queries, str):
        places = _exec_queries_list(queries.strip().split('\n'), key, pages, details)
    else:
        raise TypeError('{} object is not a valid type'.format(type(queries)))
    return places


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search Google Maps and create spreadsheets through Places API.')
    query_in = parser.add_mutually_exclusive_group(required=True)
    query_in.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), help='File containing queries, separated by a newline. Exclusive with -q.')
    query_in.add_argument('-q', '--query', type=str, nargs='*', help='Query or queries to execute. Exclusive with -i.')
    parser.add_argument('-k', '--key', type=str, default='auth.json', help='Key file or string. If a string is provided, it will be saved automatically to auth.json. Default: auth.json')
    parser.add_argument('-f', '--forget-credentials', action='store_true', help='Whether to forget entered credentials. Entered key will not be saved to auth.json file')
    parser.add_argument('-d', '--fetch-details', action='store_true', help='Whether to fetch details of places from a query. May take much longer, especially when combined with -p 3.')
    parser.add_argument('-p', '--pages', choices=[1,2,3], type=int, default=3, help='Number of pages to fetch from a single query. Default: 3')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    
    args = parser.parse_args()
    
    
    if os.path.exists(args.key):
        key = json.load(open(args.key, 'r'))['application_key']
    else:
        key = args.key
        if not args.forget_credentials:
            credentials = {'application_key': args.key}
            json.dump(credentials, open('auth.json', 'w'))

    if args.query:
        places = exec_queries(args.query, key, args.pages, args.fetch_details)
    
    if args.infile:
        places = exec_queries(args.infile.read(), key, args.pages, args.fetch_details)
    
    args.outfile.write(str(places))
        
    

# places = mass_search(query="construtoras em araçatuba", key=key)

# print(len(places))
