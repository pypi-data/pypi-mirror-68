# Netlink Tracer

Netlink is a socket-based interface used for communication between the Linux
kernel and userspace applications.

`tracenl` is a proof-of-concept tool for monitoring and decoding Netlink
messages at a process level. It is implemented as a thin wrapper around
[python-ptrace](https://github.com/vstinner/python-ptrace) and
[pyroute2](https://pyroute2.org/).

## Installation

Install with `pip`:

```
$ pip install tracenl
```

## Usage

Typical usage:

```
$ tracenl -- iw dev

[4292] sendmsg(fd=3, msg=0x00007ffcc5215100, flags=0x0000000000000000) = 32 (0x0000000000000020)
  {'attrs': [('NL80211_ATTR_WIPHY_NAME', 'nl80211')],
   'cmd': 3,
   'header': {'flags': 5,
              'length': 32,
              'pid': 1786777796,
              'sequence_number': 1589321889,
              'type': 16},
   'reserved': 0,
   'version': 1}

[4292] recvmsg(fd=3, msg=0x00007ffcc5215090, flags=0x0000000000000022) = 2316 (0x000000000000090c)
  {'attrs': [('NL80211_ATTR_WIPHY_NAME', 'nl80211'),
             ('NL80211_ATTR_WIPHY', 29),
             ('NL80211_ATTR_IFINDEX', 1),
             ('NL80211_ATTR_IFNAME', ''),
             ('NL80211_ATTR_IFTYPE', 278),
             ('NL80211_ATTR_MAC', '14:00:01:00:08:00'),
             ('NL80211_ATTR_KEY_DATA', '....')],
...
```

## Limitations

In its current state, `tracenl` has significant limitations:

- Only decodes nl80211 messages.
- No support for attaching to running processes.
- Unattractive console output
