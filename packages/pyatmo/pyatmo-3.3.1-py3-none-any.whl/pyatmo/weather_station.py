import logging
import time

from .exceptions import NoDevice
from .helpers import _BASE_URL, fixId, todayStamps

LOG = logging.getLogger(__name__)

_GETMEASURE_REQ = _BASE_URL + "api/getmeasure"
_GETSTATIONDATA_REQ = _BASE_URL + "api/getstationsdata"


class WeatherStationData:
    """
    List the Weather Station devices (stations and modules)
    Args:
        authData (ClientAuth): Authentication information with a working access Token
    """

    def __init__(self, authData, urlReq=None):
        """Initialize the weather station class."""
        self.urlReq = urlReq or _GETSTATIONDATA_REQ
        self.authData = authData
        resp = self.authData.post_request(url=self.urlReq)
        if resp is None or "body" not in resp:
            raise NoDevice("No weather station data returned by Netatmo server")
        try:
            self.rawData = fixId(resp["body"].get("devices"))
        except KeyError:
            LOG.debug("No <body> in response %s", resp)
            raise NoDevice("No weather station data returned by Netatmo server")
        if not self.rawData:
            raise NoDevice("No weather station available")
        self.stations = {d["_id"]: d for d in self.rawData}
        self.modules = {}
        for item in self.rawData:
            if "modules" not in item:
                item["modules"] = [item]
            for m in item["modules"]:
                if "module_name" not in m:
                    if m["type"] == "NHC":
                        m["module_name"] = m["station_name"]
                    else:
                        continue
                self.modules[m["_id"]] = m
                self.modules[m["_id"]]["main_device"] = item["_id"]
        self.default_station = list(self.stations.values())[0]["station_name"]

    def modulesNamesList(self, station=None, station_id=None):
        """Return a list of all modules for a given or all stations."""
        res = set()
        station_data = None
        if station_id is not None:
            station_data = self.stationById(station_id)
        elif station is not None:
            station_data = self.stationByName(station)
        if station_data is not None:
            res.add(station_data.get("module_name", station_data.get("type")))
            for m in station_data["modules"]:
                res.add(m.get("module_name", m.get("type")))
        else:
            res.update([m["module_name"] for m in self.modules.values()])
            for s in self.stations.values():
                res.add(s.get("module_name", s.get("type")))
        return list(res)

    def getModules(self, station=None, station_id=None):
        """Return a dict or modules for a given or all stations."""
        res = {}
        station_data = None
        if station_id is not None:
            station_data = self.stationById(station_id)
        elif station is not None:
            station_data = self.stationByName(station)
        if station_data is not None:
            stations = [self.stations[station_data["_id"]]]
        else:
            stations = self.stations.values()
        for s in stations:
            res[s["_id"]] = {
                "station_name": s["station_name"],
                "module_name": s.get("module_name", s.get("type")),
                "id": s["_id"],
            }

            for m in s["modules"]:
                res[m["_id"]] = {
                    "station_name": m.get("station_name", s["station_name"]),
                    "module_name": m.get("module_name", m.get("type")),
                    "id": m["_id"],
                }
        return res

    def stationByName(self, station=None):
        """Return station by name."""
        if not station:
            station = self.default_station
        for i, s in self.stations.items():
            if s["station_name"] == station:
                return self.stations[i]
        return None

    def stationById(self, sid):
        """Return station by id."""
        return None if sid not in self.stations else self.stations[sid]

    def moduleByName(self, module_name, station=None):
        """Return module by name."""
        s = None
        if station:
            s = self.stationByName(station)
            if not s:
                return None
            if s["module_name"] == module_name:
                return s
        else:
            for s in self.stations.values():
                if "module_name" in s:
                    if s["module_name"] == module_name:
                        return s
                    break
        for m in self.modules:
            module = self.modules[m]
            if module["module_name"] == module_name:
                if not s or module["main_device"] == s["_id"]:
                    return module
        return None

    def moduleById(self, mid, sid=None):
        """Return module by id."""
        s = self.stationById(sid) if sid else None
        if mid in self.modules:
            if s:
                for module in s["modules"]:
                    if module["_id"] == mid:
                        return module
            else:
                return self.modules[mid]

    def monitoredConditions(self, module=None, moduleId=None):
        """Return monitored conditions for given module(s)."""
        if moduleId:
            mod = self.moduleById(moduleId)
            if not mod:
                mod = self.stationById(moduleId)
        elif module:
            mod = self.moduleByName(module)
            if not mod:
                mod = self.stationByName(module)
        else:
            return None
        conditions = []
        if not mod:
            return conditions
        for cond in mod.get("data_type", []):
            if cond == "Wind":
                # the Wind meter actually exposes the following conditions
                conditions.extend(
                    ["WindAngle", "WindStrength", "GustAngle", "GustStrength"]
                )
            elif cond == "Rain":
                conditions.extend(["Rain", "sum_rain_24", "sum_rain_1"])
            else:
                conditions.append(cond)
        if mod["type"] in ["NAMain", "NHC"]:
            # the main module has wifi_status
            conditions.append("wifi_status")
        else:
            # assume all other modules have rf_status, battery_vp, and battery_percent
            conditions.extend(["rf_status", "battery_vp", "battery_percent"])
        if mod["type"] in ["NAMain", "NAModule1", "NAModule4", "NHC"]:
            conditions.extend(["min_temp", "max_temp"])
        if mod["type"] in [
            "NAMain",
            "NAModule1",
            "NAModule2",
            "NAModule3",
            "NAModule4",
            "NHC",
        ]:
            conditions.append("reachable")
        return conditions

    def lastData(self, station=None, exclude=0, byId=False):
        """Return data for a given station and time frame."""
        key = "_id" if byId else "module_name"
        if station is not None:
            stations = [station]
        elif byId:
            stations = [s["_id"] for s in list(self.stations.values())]
        else:
            stations = [s["station_name"] for s in list(self.stations.values())]
        # Breaking change from Netatmo : dashboard_data no longer available if station lost
        lastD = {}
        for st in stations:
            s = self.stationById(st) if byId else self.stationByName(st)
            if not s or "dashboard_data" not in s:
                LOG.info("No dashboard data for station %s", st)
                continue
            # Define oldest acceptable sensor measure event
            limit = (time.time() - exclude) if exclude else 0
            ds = s["dashboard_data"]
            if key in s and ds["time_utc"] > limit:
                lastD[s[key]] = ds.copy()
                lastD[s[key]]["When"] = lastD[s[key]].pop("time_utc")
                lastD[s[key]]["wifi_status"] = s["wifi_status"]
                lastD[s[key]]["reachable"] = s["reachable"]
            for module in s["modules"]:
                if "dashboard_data" not in module or key not in module:
                    continue
                ds = module["dashboard_data"]
                if "time_utc" in ds and ds["time_utc"] > limit:
                    lastD[module[key]] = ds.copy()
                    lastD[module[key]]["When"] = lastD[module[key]].pop("time_utc")
                    # For potential use, add battery and radio coverage information to module data if present
                    for i in (
                        "rf_status",
                        "battery_vp",
                        "battery_percent",
                        "reachable",
                        "wifi_status",
                    ):
                        if i in module:
                            lastD[module[key]][i] = module[i]
        return lastD

    def checkNotUpdated(self, station=None, delay=3600):
        """Check if a given station has not been updated."""
        res = self.lastData(station)
        ret = []
        for mn, v in res.items():
            if time.time() - v["When"] > delay:
                ret.append(mn)
        return ret if ret else None

    def checkUpdated(self, station=None, delay=3600):
        """Check if a given station has been updated."""
        res = self.lastData(station)
        ret = []
        for mn, v in res.items():
            if time.time() - v["When"] < delay:
                ret.append(mn)
        return ret if ret else None

    def getMeasure(
        self,
        device_id,
        scale,
        mtype,
        module_id=None,
        date_begin=None,
        date_end=None,
        limit=None,
        optimize=False,
        real_time=False,
    ):
        postParams = {"device_id": device_id}
        if module_id:
            postParams["module_id"] = module_id
        postParams["scale"] = scale
        postParams["type"] = mtype
        if date_begin:
            postParams["date_begin"] = date_begin
        if date_end:
            postParams["date_end"] = date_end
        if limit:
            postParams["limit"] = limit
        postParams["optimize"] = "true" if optimize else "false"
        postParams["real_time"] = "true" if real_time else "false"
        return self.authData.post_request(url=_GETMEASURE_REQ, params=postParams)

    def MinMaxTH(self, station=None, module=None, frame="last24"):
        if not station:
            station = self.default_station
        s = self.stationByName(station)
        if not s:
            s = self.stationById(station)
            if not s:
                return None
        if frame == "last24":
            end = time.time()
            start = end - 24 * 3600  # 24 hours ago
        elif frame == "day":
            start, end = todayStamps()
        if module and module != s["module_name"]:
            m = self.moduleByName(module, s["station_name"])
            if not m:
                m = self.moduleById(s["_id"], module)
                if not m:
                    return None
            # retrieve module's data
            resp = self.getMeasure(
                device_id=s["_id"],
                module_id=m["_id"],
                scale="max",
                mtype="Temperature,Humidity",
                date_begin=start,
                date_end=end,
            )
        else:  # retrieve station's data
            resp = self.getMeasure(
                device_id=s["_id"],
                scale="max",
                mtype="Temperature,Humidity",
                date_begin=start,
                date_end=end,
            )
        if resp:
            T = [v[0] for v in resp["body"].values()]
            H = [v[1] for v in resp["body"].values()]
            return min(T), max(T), min(H), max(H)
        return None
