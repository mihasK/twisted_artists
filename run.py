from twisted.internet import reactor
from twisted.web.client import getPage
from functools import partial
from urllib import urlopen


servers = ['http://calm-scrubland-3271.herokuapp.com/',
           'http://evening-ocean-3014.herokuapp.com/',
           'http://mysterious-bayou-8722.herokuapp.com/',
           'http://whispering-sands-1197.herokuapp.com/',
           'http://migrate-artists.herokuapp.com/',
           'http://migrate-artists2.herokuapp.com/']


LIMIT = 5
offset = [-LIMIT, ]

urlopen(servers[0] + '/clear')

def load_server(server, offs):
    url = '{server}?offset={offset}&limit={limit}'.format(server=server, offset=offs, limit=LIMIT)


    deffered = getPage(url)
    deffered.addCallback(partial(getpage_callback, server=server, url=url))
    # deffered.addErrback(partial(error_handler, server=server, offset=offs))


def make_available(server):
    offset[0] += LIMIT
    print offset[0]
    load_server(server, offset[0])


def getpage_callback(html, server, url):
    print 'Server: %s,\n' \
          '\turl is %s,\n' \
          '\tresponse is: %s' % (server, url, html)
    if html == 'Migrated: 0':
        reactor.stop()
    make_available(server)


def error_handler(error, server, offs):
    print 'Server ' + server + ' is broken'
    print error
    load_server(server, offs)


for s in servers:

    make_available(s)

reactor.run()

