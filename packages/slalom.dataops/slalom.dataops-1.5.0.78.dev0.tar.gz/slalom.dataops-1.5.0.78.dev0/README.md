# dataops-tools

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slalom.dataops.svg)](https://pypi.org/project/slalom.dataops/) [![PyPI version](https://badge.fury.io/py/slalom.dataops.svg)](https://badge.fury.io/py/slalom.dataops) [![CI/CD Badge (master)](https://github.com/slalom-ggp/dataops-tools/workflows/CI/CD%20Builds/badge.svg)](https://github.com/slalom-ggp/dataops-tools/actions?query=workflow%3A%22CI/CD%20Builds%22) [![Docker Publish (latest)](<https://github.com/slalom-ggp/dataops-tools/workflows/Docker%20Publish%20(latest)/badge.svg>)](https://github.com/slalom-ggp/dataops-tools/actions?query=workflow%3A%22Docker+Publish+%28latest%29%22)

Reusable tools, utilities, and containers that accelerate data processing and DevOps.

## Installation

Compatible with Python 3.7 and 3.8.

```bash
pip install slalom.dataops
```

## Running via Command Line

After installing via pip, you will have access to the following command line tools:

| Command   | Description                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------- |
| `s-spark` | Run Spark programs and Jupyter notebooks (natively, containerized via docker, or remotely via ECS). |
| `s-infra` | Run Terraform IAC (Infrastructure-as-Code) automation.                                              |

## Testing

```bash
> python
```

```python
import dock_r, sparkutils; dock_r.smart_build("containers/docker-spark/Dockerfile", "local-spark", push_core=False); dock_r.smart_build("Dockerfile", "local-dataops", push_core=False); spark = sparkutils.get_spark(dockerized=True)
```
