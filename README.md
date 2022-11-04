# Prometheus Rasdaemon exporter

### Introduction
This is a Prometheus exporter for rasdaemon.

This tools rely on Rasdaemon to retreive its data.
Rasdaemon is a RAS (Reliability, Availability and Serviceability) logging tool.
Repository available here: http://git.infradead.org/users/mchehab/rasdaemon.git

By default prometheus-rasdaemon-exporter listens on 0.0.0.0:<to be defined>.

### Installation

Using apt:
```
apt-get install prometheus-rasdaemon-exporter
```

Using pip:
```
pip install prometheus-rasdaemon-exporter
```

### Running

A minimal invocation looks like this:

```
prometheus-rasdaemon-exporter
```

`prometheus-rasdaemon-exporter` supports the following arguments:

```
  --db DB              Path to rasdaemon DB
  --address ADDRESS    Address on which to expose metrics and web interface
  --port PORT          Port on which to expose metrics and web interface
  --collector-all      Enable/Disable collecting all errors (default: False)
  --collector-aer      Enable/Disable collecting AER errors (default: True)
  --collector-mce      Enable/Disable collecting MCE errors (default: True)
  --collector-mc       Enable/Disable collecting MC errors (default: True)
  --collector-extlog   Enable/Disable collecting EXTLOG errors (default: False)
  --collector-devlink  Enable/Disable collecting DEVLINK errors (default: False)
  --collector-disk     Enable/Disable collecting DISK errors (default: False)
```



### Metrics

Metrics and labels are returned with the same name as used on rasademon database, to avoid collision they are prefixed with their type (aer, mc, mce etc)
By default, only collecting AER, MC and MCE records are enabled.

```
# HELP aer_events_total Total of AER Events occured
# TYPE aer_events_total counter
aer_events_total{aer_dev_name="0000:02:00.0",aer_err_msg="Bad TLP",aer_err_type="Corrected"} 3.0
aer_events_total{aer_dev_name="0000:02:00.0",aer_err_msg="Receiver Error, Bad TLP",aer_err_type="Corrected"} 1.0
aer_events_total{aer_dev_name="0000:02:00.0",aer_err_msg="",aer_err_type="Uncorrected (Fatal)"} 4.0
aer_events_total{aer_dev_name="0000:02:00.0",aer_err_msg="Completer Abort, Malformed TLP TLP Header: 00000004 00000005 00000006 00000007",aer_err_type="Uncorrected (Non-Fatal)"} 3.0
# HELP mce_record_total Total of MCE record occured
# TYPE mce_record_total counter
mce_record_total{msg="MEMORY CONTROLLER MS_CHANNEL1_ERR Transaction: Memory scrubbing error Corrected patrol scrub error"} 149.0
mce_record_total{msg="MEMORY CONTROLLER RD_CHANNEL1_ERR Transaction: Memory read error"} 5107.0
mce_record_total{msg="MEMORY CONTROLLER RD_CHANNEL1_ERR Transaction: Memory read error Corrected memory read error"} 4958.0
# HELP mc_events_total Total of Memory Controller events occured
# TYPE mc_events_total counter
mc_events_total{err_type="Corrected",label="DIMM_P0_B0"} 2.0

```