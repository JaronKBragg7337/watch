"""Shared bits for the MSI-side writers. Reads keys from ~/.secrets/keys.env; never prints them."""
from __future__ import annotations
import datetime as dt, pathlib, zoneinfo
ROOT = pathlib.Path(__file__).resolve().parent.parent
TZ = zoneinfo.ZoneInfo("America/Indiana/Indianapolis")
SKIP = {"collectors", "brief", "market-feed"}


def today():
    return dt.datetime.now(TZ)


def keys():
    p = pathlib.Path.home() / ".secrets" / "keys.env"; out = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1); out[k.strip()] = v.strip().strip('"')
    return out


def captures_for(day):
    """Every capture written for `day` by any collector/reader, as (writer, text)."""
    out = []
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name not in SKIP:
            f = d / f"{day}.md"
            if f.exists():
                out.append((d.name, f.read_text(encoding="utf-8")))
    return out
