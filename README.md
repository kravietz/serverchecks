# serverchecks

Python 3 module for fast, parallel execution of health checks on a broad range
of popular Internet infrastructure protocols with multi-protocol alerting capabilities.
Implemented in pure Python (no shell commands called) using `asyncio` library.


## Install
The module comes in a number of flavours that provide additional features using
third-party Python libraries.

| Flavor | Features                                                                      | Install                          |
|--------|-------------------------------------------------------------------------------|----------------------------------|
| Core   | Checks: TCP, DNS (basic), TLS, URL, POP3, SMTP, IMAP. Alerts: console ,SMTP  | `pip3 install serverchecks`        |
| DNS    | Checks: DNS (full)                                                            | `pip3 install serverchecks[dns]`   |
| DNSSEC | Checks: DNSSEC, DNS (full)                                                    | `pip3 install serverchecks[dnssec]` |
| XMPP   | Alerts: XMPP                                                                  | `pip3 install serverchecks[xmpp]`  |
| Telegram| Alerts: Telegram                                                             | `pip3 install serverchecks[telegram]` |
| Matrix | Alerts: Matrix                                                                | `pip3 install serverchecks[matrix]` | 

Shortcut to install all flavors:

```
pip3 install serverchecks[dnssec,xmpp,telegram,matrix]
```

## Usage
Create a basic configuration file `checks.yaml`:

```yaml
verbose: yes
alert_mode: always

alerts:
  console:
  - dummy:

checks:
  basicdns:
  - fqdn: webcookies.org
  - fqdn: ipsec.pl
```

Run:
```
python -m serverchecks.main test.yaml

```

Sample output:
```
$ python -m serverchecks.main test.yaml

Initialized alert class <Console>
2 tests completed in 0.03 seconds, 2 successful, 0 failed
✓ webcookies.org 94.130.162.156
✓ ipsec.pl 98.143.148.71
```