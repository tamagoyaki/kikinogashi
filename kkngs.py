import urllib.request
import json
import sys


class QBrowser():
    def __init__(self):
        # to pretend as Mozilla's browser
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(self.opener)

    def get(self, url):
        rv = None
        with urllib.request.urlopen(url) as u:
            rv = u.read()
        return rv

    def getjson(self, url):
        rv = self.get(url)
        if rv:
            rv = json.loads(rv.decode('utf8'))
        return rv


qb = QBrowser()
ct = qb.getjson('https://www.nhk.or.jp/radioondemand/json/index_v3/index.json')
dlist = ct['data_list']

args = len(sys.argv)

if 2 == args and "list" == sys.argv[1]:
    # show program list
    ix = 0
    for data in dlist:
        print(f"{ix} : {data['program_name']}, {data['corner_name']}, "
              f"{data['onair_date']}, {data['detail_json']}")
        ix += 1
elif 2 == args and sys.argv[1].isnumeric():
    # play specified program
    no = int(sys.argv[1])
    url = dlist[no]['detail_json']

    ct = qb.getjson(url)
    main = ct['main']

    for detail in main['detail_list']:
        for file in detail['file_list']:
            print(f"{file['file_name']}")
else:
    print(f'USAGE: {sys.argv[0]} ["list" or numeric string]')
    print(f'')
    print(f'    {sys.argv[0]} list')
    print(f'    {sys.argv[0]} 80')
