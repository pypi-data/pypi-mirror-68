

<div align="center" style="text-align:center">
  
# SRE Logging
  
Common logging setup package for SRE python programs.

If you have a Python
program that's gonna be anywhere near production, or is in any way
'mission critical', it should use this package so that it can plug into
our DataDog log analysis very easily.

<img align="center" src="https://img.shields.io/github/workflow/status/glasswall-sre/sre-logging/CI">
<img align="center" src="https://img.shields.io/codecov/c/github/glasswall-sre/sre-logging">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=sre-loggin&metric=alert_status">

</div>



## Installation
```bash
pip install srelogging
```

## Usage
In your program, as soon as the application starts, you'll want to call
`srelogging.configure_logging()`:
```python
import srelogging

# ...

srelogging.configure_logging()
```

Additionally, if you want to specify any custom logging
config (in Python logging [dictConfig format](https://docs.python.org/3.7/library/logging.config.html#logging-config-dictschema))
then you can specify a file path in the arguments to `configure_logging()`:

```python
srelogging.configure_logging("logging_config.yml")
```

```yaml
# contents of logging_config.yml
version: 1
formatters:
  default:
    class: srelogging.UTCFormatter
    format: "%(asctime)s.%(msecs)03dZ [%(levelname)s] <%(module)s.py:%(lineno)d> %(message)s"
    datefmt: "%Y-%m-%d %H:%M:%S"
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: default
    stream: ext://sys.stdout
root:
  level: WARNING
  handlers: [console]

```
