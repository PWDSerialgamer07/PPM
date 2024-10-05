from rich.console import Console
from rich import print
from rich.console import Console
from rich.box import Box
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
import datetime
import os
from time import sleep
import psutil

console = Console()
layout = Layout()


def make_clock():
    """Create a small clock panel for the top-right corner."""
    time_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    tw, th = console.size
    # Cpanel = Panel(time_str, title="Clock", expand=True, box=Box.NONE)
    return time_str


def make_layout():
    layout.split_column(
        Layout(make_clock(), name="clock", size=1),
        Layout(name="everything"),
    )
    layout["everything"].split_row(
        Layout(name="stats", ratio=1),
        Layout(name="graphs+processes", ratio=4)
    )
    layout["graphs+processes"].split_column(
        Layout(name="graphs", ratio=1),
        Layout(get_processes(), name="processes", ratio=1),
    )
    return layout


def get_processes():
    table = Table(title="Processes")
    table.add_column("PID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", justify="center", style="magenta", no_wrap=True)
    table.add_column("CPU %", justify="center", style="green", no_wrap=True)
    table.add_column("MEM %", justify="center", style="blue", no_wrap=True)
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            table.add_row(
                str(proc.info['pid']),  # PID is an integer
                proc.info['name'] or "N/A",  # Name can be None sometimes
                # CPU percentage as a float
                f"{proc.info['cpu_percent']:.2f}%",
                # Memory percentage as a float
                f"{proc.info['memory_percent']:.2f}%"
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return table


def main():
    make_layout()
    with Live(layout, console=console, refresh_per_second=10, screen=True) as live:
        while True:
            layout["clock"].update(make_clock())
            sleep(1)


if "__main__" == __name__:
    main()
