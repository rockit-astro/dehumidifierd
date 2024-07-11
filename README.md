## Dehumidifier control daemon 

`dehumidifierd` controls power to a dehumidifier (via [powerd](https://github.com/rockit-astro/powerd)) according to the current conditions and dome status.

`dehumidifier` is a commandline utility that controls the dehumidifier daemon.


### Configuration

Configuration is read from json files that are installed by default to `/etc/dehumidifierd`.
A configuration file is specified when launching the dehumidifier server, and the `dehumidifier` frontend will search this location when launched.

```python
{
  "daemon": "onemetre_dehumidifier", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "dehumidifierd@onemetre", # The name to use when writing messages to the observatory log.
  "control_machines": ["OneMetreDome", "OneMetreTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "query_delay": 30, # Humidity query interval in seconds.
  "humidity_daemon": "onemetre_roomalert", # Daemon to query the internal humidity from.
  "humidity_value_key": "internal_humidity", # Key in the daemon's last_measurement dictionary.
  "humidity_valid_key": "internal_humidity_valid", # Key in the daemon's last_measurement dictionary.
  "power_daemon":  "onemetre_power", # Power daemon name for toggling the dehumidifier on and off.
  "power_switch":  "dehumidifier", # Power daemon switch name for the dehumidifier.
  "dome_daemon":  "onemetre_dome", # Dome daemon name for querying the dome state.
  "dome_closed_key": "closed", # Dome daemon key defining whether the dome is closed.
  "humidity_enable_limit": 70, # Enable the dehumidifier when the internal humidity rises above this value.
  "humidity_disable_limit": 65 # Disable the dehumidifier when the internal humidity drops below this value.
}
```

### Initial Installation

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                                  | Description                                                                              |
|------------------------------------------|------------------------------------------------------------------------------------------|
| rockit-dehumidifier-server               | Contains the `dehumidifierd` server and systemd service file.                            |
| observatory-dehumidifier-client          | Contains the `dehumidifier` commandline utility for controlling the dehumidifier server. |
| python3-warwick-observatory-dehumidifier | Contains the python module with shared code.                                             |
| rockit-dehumidifier-data-clasp           | Contains the json configuration for the CLASP telescope.                                 |
| rockit-dehumidifier-data-onemetre        | Contains the json configuration for the W1m telescope.                                   |
| rockit-dehumidifier-data-sting           | Contains the json configuration for the STING telescope.                                 |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now dehumidifierd@<config>
```

where `config` is the name of the json file for the appropriate dome.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart dehumidifierd@<config>
```

### Testing Locally

The dome server and client can be run directly from a git clone:
```
./dehumidifierd config/onemetre.json
DEHUMIDIFIERD_CONFIG_PATH=./config/onemetre.json ./dehumidifier status
```
