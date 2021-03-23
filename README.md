## Dehumidifier control daemon 
Part of the observatory software for the Warwick La Palma telescopes.

`dehumidifierd` controls power to a dehumidifier (via [powerd](https://github.com/warwick-one-metre/powerd)) according to the current conditions and dome status.

`dehumidifier` is a commandline utility that controls the dehumidifier daemon.

`python3-warwick-observatory-dehumidifer` is a python module with the common dehumidifier code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `onemetre-dehumidifier-server`, the `dehumidifierd` must be enabled using:
```
sudo systemctl enable dehumidifierd@onemetre
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start dehumidifierd@onemetre
```