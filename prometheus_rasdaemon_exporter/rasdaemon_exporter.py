#!/usr/bin/env python3

import argparse
import sqlite3
import time
import sys

from typing import Iterator, List, Tuple
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, CounterMetricFamily


class RASCollector:
    query: str

    def __init__(self, database: sqlite3.Connection):
        self.database = database

    def poll_db(self) -> List[Tuple[str, int]]:
        events_cur = self.database.execute(self.query)
        events = events_cur.fetchall()
        return events

    def collect(self) -> Iterator[CounterMetricFamily]:
        events = self.poll_db()
        count = self.get_count()
        for event in events:
            count.add_metric(event[:-1], event[-1])
        yield count

    def get_count(self) -> CounterMetricFamily:
        raise NotImplementedError


# class ARMCollector(RASCollector): pass
# Not implemented yet, need something to test it


class EXTLOGCollector(RASCollector):
    query = "select etype, severity, count(*) from extlog_event group by etype, severity"

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "extlog_event",
            "Total of devlink event occured",
            labels=["extlog_etype", "extlog_severity"]
        )


class DEVLINKCollector(RASCollector):
    query = "select dev_name, count(*) from devlink_event group by dev_name"

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "devlink_event",
            "Total of devlink event occured",
            labels=['devlink_dev_name']
        )


class DISKCollector(RASCollector):
    query = "select dev, count(*) from disk_errors group by dev"

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "disk_errors",
            "Total of disk errors occured",
            labels=['disk_dev']
        )


class MCECollector(RASCollector):
    query = "select error_msg, count(*) from mce_record group by error_msg"

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "mce_record",
            "Total of MCE record occured",
            labels=['mce_msg']
        )


class MCCollector(RASCollector):
    query = "select err_type, label, count(*) from mc_event group by err_type, label"

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "mc_events",
            "Total of Memory Controller events occured",
            labels=["mc_err_type", "mc_label"]
        )


class AERCollector(RASCollector):
    query = (
        "select err_type, err_msg, dev_name, count(*)"
        "from aer_event group by err_type, err_msg, dev_name"
    )

    def get_count(self) -> CounterMetricFamily:
        return CounterMetricFamily(
            "aer_events",
            "Total of AER Events occured",
            labels=["aer_err_type", "aer_err_msg", "aer_dev_name"]
        )


def main():
    COLLECTORS = [
        ("aer", True, AERCollector),
        ("mce", True, MCECollector),
        ("mc", True, MCCollector),
        ("extlog", False, EXTLOGCollector),
        ("devlink", False, DEVLINKCollector),
        ("disk", False, DISKCollector),
    ]

    parser = argparse.ArgumentParser(
        description="Exporter for rasademon (experimental)",
        epilog=(
            "Available error collection will depend on the flags used during the compilation"
            " of rasdaemon, some collectors might not work on default installations"
        )
    )

    parser.add_argument(
        "--db",
        help="Path to rasdaemon DB",
        default="/var/lib/rasdaemon/ras-mc_event.db"
    )
    parser.add_argument(
        "--address",
        help="Address on which to expose metrics and web interface",
        default=""
    )

    parser.add_argument(
        "--port",
        help="Port on which to expose metrics and web interface",
        default=9445,
        type=int
    )
    parser.add_argument(
        "--collector-all",
        help="Enable/Disable collecting all errors (default: False)",
        action="store_true"
    )

    for collector, state, cls in COLLECTORS:
        parser.add_argument(
            f"--collector-{collector}",
            help=f"Enable/Disable collecting {collector.upper()} errors (default: {state})",
            action=f"store_{str(not state).lower()}"
        )

    args = parser.parse_args()

    try:
        DB = sqlite3.connect(f"file:{args.db}?mode=ro", check_same_thread=False)
    except sqlite3.OperationalError as e:
        print(f"Cannot connect to {args.db}: {e}")
        sys.exit(1)

    for collector, state, cls in COLLECTORS:
        if args.collector_all or getattr(args, f"collector_{collector}"):
            #  mypy you do it wrong
            REGISTRY.register(cls(DB))  # type: ignore

    start_http_server(args.port, addr=args.address)
    print(f"Starting http server on {args.address}:{args.port}")
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
