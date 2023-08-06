import dns.query


class StreamOutbound():
    def __init__(self, ip, port, timeout):
        self._ip = ip
        self._port = port
        self._timeout = timeout

    @classmethod
    def from_dict(cls, outbound_dict):
        ip = outbound_dict['ip']
        port = outbound_dict.get('port', 53)
        timeout = outbound_dict.get('timeout', 60)
        return cls(ip, port, timeout)

    def query(self, dns_message):
        return dns.query.tcp(dns_message, self._ip, port=self._port, timeout=self._timeout)
