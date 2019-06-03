# serverchecks

Python 3 module for fast, parallel execution of health checks on a broad range
of popular Internet infrastructure protocols with multi-protocol alerting capabilities.
Implemented in pure Python (no shell commands called) using `asyncio` library.


## Install
The module comes in a number of flavours that provide additional features using
third-party Python libraries.
<table>
<tr><th>Flavour</th><th>Features</th><th>Install</th>

<tr><td>Core
<td>
Checks:
<ul>
<li>TCP
<li>DNS (basic)
<li>TLS
<li>URL
<li>POP3
<li>SMTP
<li>IMAP
</ul>
Alerts:
<ul>
<li>Console
<li>SMTP
</td>
<td>
<code>pip3 instal serverchecks</code>
</td>

<tr><td>DNS
<td>Checks:
<ul>
<li>DNS (full)
</ul>
<td>
<code>pip3 instal serverchecks[dns]</code>
</td>

<tr><td>DNSSEC
<td>Checks:
<ul>
<li>DNSSEC
<li>DNS (full)
</ul>
<td>
<code>pip3 instal serverchecks[dnssec]</code>
</td>

<tr><td>XMPP
<td>Alerts:
<ul>
<li>XMPP
</ul>
<td>
<code>pip3 instal serverchecks[xmpp]</code>
</td>

<tr><td>Telegram
<td>Alerts:
<ul>
<li>Telegram
</ul>
<td>
<code>pip3 instal serverchecks[telegram]</code>
</td>

<tr><td>Matrix
<td>Alerts:
<ul>
<li>Matrix
</ul>
<td>
<code>pip3 instal serverchecks[matrix]</code>
</td>

</table>


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