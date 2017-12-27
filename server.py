from twisted.internet import reactor
from twisted.names import client, dns, server
from twisted.names.dns import CNAME


class HostAliasesResolver(object):
    """
    A resolver which tries to answer from host aliases.
    """

    def __init__(self, resolver, filename):
        self.hosts = {}
        self.resolver = resolver

        with open(filename) as f:
            for line in map(str.strip, f):
                if line.startswith('#'):
                    continue

                try:
                    alias, target = line.split()
                    if not target.startswith('#'):
                        self.hosts[alias] = target
                except ValueError:
                    pass

        print(self.hosts)

    def query(self, query, timeout=None):
        print(query)
        if query.type == dns.A:
            alias = query.name.name.decode()
            target = self.hosts.get(alias)
            if target is not None:
                print('{} --> {}'.format(alias, target))
                return self.respond(alias, target)

        return self.resolver.query(query, timeout)

    def respond(self, alias, target):
        def resolve(result):
            answers, authority, additional = result

            cname = dns.RRHeader(
                type=CNAME,
                name=alias.encode(),
                payload=dns.Record_CNAME(name=target.encode()))

            answers = [cname] + answers
            return answers, authority, additional

        return self.resolver.query(dns.Query(target, dns.A)) \
            .addCallback(resolve)


def main():
    resolver = client.Resolver(servers=[('80.80.80.80', 53)])

    factory = server.DNSServerFactory(
        clients=[
            HostAliasesResolver(resolver, filename='/etc/host.aliases'),
        ]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)
    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())
