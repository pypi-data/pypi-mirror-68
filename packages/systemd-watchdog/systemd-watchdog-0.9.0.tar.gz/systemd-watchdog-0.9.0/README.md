# systemd_watchdog

![](https://img.shields.io/pypi/l/systemd-watchdog)
![](https://img.shields.io/pypi/v/systemd-watchdog.svg)
![](https://img.shields.io/travis/com/aarondmarasco/systemd-watchdog)
![](https://img.shields.io/badge/tested%20versions-3.5%7C3.6%7C3.7%7C3.8%7Cpypy3-success)
![](https://img.shields.io/pypi/wheel/systemd-watchdog.svg)
![](https://img.shields.io/pypi/pyversions/systemd-watchdog.svg)

sd_notify(3) and sd_watchdog_enabled(3) client functionality implemented in Python 3 for writing Python daemons

## Install
```
$ pip install systemd-watchdog
```
or
```
$ git clone ...
$ make install
```

## Usage

```python
import systemd_watchdog

wd = systemd_watchdog.watchdog()
if not wd.enabled():
    # Then it's probably not running is systemd with watchdog enabled
    raise Exception("Watchdog not enabled")

# Report a status message
wd.status("Starting my service...")
time.sleep(3)

# Report that the program init is complete
wd.ready()
wd.status("Waiting for web requests...")
wd.notify()
time.sleep(3)

# Compute time between notifications
timeout_half_sec = int(float(wd.timeout) / 2e6)  # Convert us->s and half that
time.sleep(timeout_half_sec)
wd.notify()

# Report an error to the service manager
wd.notify_error("An irrecoverable error occured!")
# The service manager will probably kill the program here
time.sleep(3)
```

## Public Interface
### `systemd_watchdog.watchdog` - commonly used properties and methods
#### `ping`
The only method required for the simplest implementation; combines `notify_due` with `notify()` to _only_ send "alive" notifications at reasonable intervals.

Returns boolean indicating if a message was sent or not.

#### `beat`
Alias for `ping()` if you prefer heartbeat terminology.

#### `ready()`
Report ready service state, _i.e._ completed init (only needed with `Type=notify`).

#### `status(msg)`
Send a service status message.

### `systemd_watchdog.watchdog` - less-used properties and methods
#### `is_enabled`
Boolean property stating whether watchdog capability is enabled.

#### `timeout`
Property reporting the number of microseconds (int) before process will be killed.

It is recommended that you call `notify()` once roughly half of this interval has passed (see `notify_due`).

#### `timeout_td`
Property that is the same as `timeout` but presented as `datetime.timedelta` for easier manipulation.

#### `notify_due`
Boolean property indicating more than half of the watchdog interval has passed since last update.

#### `notify()`
Report a healthy service state. Other calls, _e.g._ `status()` do *not* reset the watchdog.

#### `notify_error(msg=None)`
Report an error to the watchdog manager. This program will likely be killed upon receipt.

If `msg` is provided, it will be reported as a status message prior to the error.


## History
Aaron D. Marasco May 2020
 * Forked from the sd-notify project <https://github.com/stigok/sd-notify>
 * Additional contributors can be found in GitHub repository history

## License

See `LICENSE` file
