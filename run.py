from twisted.internet import reactor
from twisted.web.client import getPage
from functools import partial
from urllib import urlopen

servers = ['http://calm-scrubland-3271.herokuapp.com/',
           'http://evening-ocean-3014.herokuapp.com/',
           'http://mysterious-bayou-8722.herokuapp.com/']

LIMIT = 5
offset = [-LIMIT, ]

urlopen(servers[0] + '/clear')


def make_available(server):
    offset[0] += LIMIT
    print offset[0]
    url = '{server}?offset={offset}&limit={limit}'.format(server=server, offset=offset[0], limit=LIMIT)
    getPage(url).addCallback(partial(getpage_callback, server=server, url=url))


def getpage_callback(html, server, url):
    print 'Server: %s,\n' \
          '\turl is %s,\n' \
          '\tresponse is: %s' % (server, url, html)
    make_available(server)

for s in servers:

    make_available(s)

reactor.run()
