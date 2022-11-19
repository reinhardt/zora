#!/usr/bin/env python3
from inverter import KostalInverter
from csv import writer
from datetime import datetime
from datetime import timedelta
import argparse
import sqlite3
import subprocess
import os

host = "192.168.178.45"
port = 1502
timeout = 1
unit = 71
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "var/solar.sqlite")
log_path = os.path.join(script_dir, "var/log.csv")
gnuplot_path = os.path.join(script_dir, "gnuplot")
html_path = os.path.join(script_dir, "gecko/html")


def write():
    inverter = KostalInverter(host=host, port=port, timeout=timeout, unit=unit)
    current_time = datetime.now().astimezone().isoformat(timespec="seconds")

    inverter_data = inverter.read_all()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    columns = ", ".join((f"{key} FLOAT" for key in inverter.registers))
    column_names = ", ".join(inverter.registers)
    sql_values = ", ".join((str(v) for v in inverter_data.values()))

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS log(
            Zeit TEXT, {columns}
        )"""
    )
    cur.execute(
        f"""INSERT INTO log (Zeit, {column_names}) VALUES (
            "{current_time}", {sql_values}
        )"""
    )
    con.commit()
    con.close()


def plot(days=2):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    inverter = KostalInverter(host=host, port=port, timeout=timeout, unit=unit)
    column_names = ", ".join(inverter.registers)
    current_time = datetime.now().astimezone()
    cutoff = current_time - timedelta(days=days)
    cutoff_stamp = cutoff.isoformat(timespec="seconds")
    res = cur.execute(
        f"SELECT Zeit, {column_names} FROM log WHERE Zeit > '{cutoff_stamp}';"
    )
    with open(log_path, "w", newline="") as csvfile:
        logwriter = writer(csvfile)
        logwriter.writerows(res.fetchall())

    inverter_fields = list(inverter.registers.keys())
    # registers are 0-indexed but gnuplot is 1-indexed, and Zeit is missing in registers
    idx_production = inverter_fields.index("total_dc_power") + 2
    idx_own_con_battery = inverter_fields.index("own_consumption_battery") + 2
    idx_own_con_pv = inverter_fields.index("own_consumption_pv") + 2
    idx_own_con_grid = inverter_fields.index("own_consumption_grid") + 2
    idx_charge_discharge = inverter_fields.index("battery_charge_discharge") + 2
    idx_grid_feedin = inverter_fields.index("total_active_power_powermeter") + 2

    cmd = (
        "gnuplot",
        "-e",
        f"set terminal png size 1440,960 enhanced font 'helvetica'; "
        f"set output '{html_path}/consumption.png'",
        f"{gnuplot_path}/common.gnuplot",
        "-e",
        f"plot '{log_path}' using 1:(${idx_own_con_pv} - (${idx_charge_discharge} < 0 ? ${idx_charge_discharge} : 0)) with filledcurves y=0 ls 104 title 'Batterie Ladung', "
        f"'' using 1:(${idx_own_con_pv} - (${idx_grid_feedin} < 0 ? ${idx_grid_feedin} : 0)) with filledcurves y=0 ls 105 title 'Einspeisung', "
        f"'' using 1:(${idx_own_con_pv} + ${idx_own_con_battery} + ${idx_own_con_grid}) with filledcurves y=0 ls 115 title 'Verbrauch Netz', "
        f"'' using 1:(${idx_own_con_pv} + ${idx_own_con_battery}) with filledcurves y=0 ls 114 title 'Verbrauch Batterie', "
        f"'' using 1:(${idx_own_con_pv}) with filledcurves y=0 ls 102 title 'Verbrauch solar', "
        f"'' using 1:{idx_production} with lines ls 103 title 'Produktion'",
    )
    subprocess.run(cmd)

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read statistical data from Kostal inverter and plot it"
    )
    parser.add_argument(
        "command",
        metavar="command",
        type=str,
        nargs="?",
        help="command to execute. `write` or `plot`. Empty for both.",
    )
    args = parser.parse_args()

    if not args.command or args.command == "write":
        write()
    if not args.command or args.command == "plot":
        plot()
