"""
Contains the core parsing and indent functions of avwx
"""

# stdlib
import re
from calendar import monthrange
from copy import copy
from datetime import datetime, timedelta, timezone
from itertools import permutations

# library
from dateutil.relativedelta import relativedelta

# module
from avwx.static.core import (
    CARDINALS,
    CLOUD_LIST,
    CLOUD_TRANSLATIONS,
    FRACTIONS,
    NUMBER_REPL,
    SPECIAL_NUMBERS,
)
from avwx.static.taf import TAF_NEWLINE, TAF_NEWLINE_STARTSWITH
from avwx.structs import Cloud, Fraction, Number, Timestamp, Units


def dedupe(items: list, only_neighbors: bool = False) -> list:
    """
    Deduplicate a list while keeping order
    
    If only_neighbors is True, dedupe will only check neighboring values
    """
    ret = []
    for item in items:
        if (only_neighbors and ret and ret[-1] != item) or item not in ret:
            ret.append(item)
    return ret


def is_unknown(val: str) -> bool:
    """
    Returns True if val represents and unknown value
    """
    if not isinstance(val, str):
        raise TypeError
    if not val or val.upper() in ("UNKN",):
        return True
    for char in val:
        if char not in ("/", "X", "."):
            break
    else:
        return True
    return False


def get_digit_list(alist: [str], from_index: int) -> ([str], [str]):
    """
    Returns a list of items removed from a given list of strings
    that are all digits from 'from_index' until hitting a non-digit item
    """
    ret = []
    alist.pop(from_index)
    while len(alist) > from_index and alist[from_index].isdigit():
        ret.append(alist.pop(from_index))
    return alist, ret


def unpack_fraction(num: str) -> str:
    """
    Returns unpacked fraction string 5/2 -> 2 1/2
    """
    nums = [int(n) for n in num.split("/") if n]
    if len(nums) == 2 and nums[0] > nums[1]:
        over = nums[0] // nums[1]
        rem = nums[0] % nums[1]
        return f"{over} {rem}/{nums[1]}"
    return num


def remove_leading_zeros(num: str) -> str:
    """
    Strips zeros while handling -, M, and empty strings
    """
    if not num:
        return num
    if num.startswith("M"):
        ret = "M" + num[1:].lstrip("0")
    elif num.startswith("-"):
        ret = "-" + num[1:].lstrip("0")
    else:
        ret = num.lstrip("0")
    return "0" if ret in ("", "M", "-") else ret


def spoken_number(num: str) -> str:
    """
    Returns the spoken version of a number

    Ex: 1.2 -> one point two
        1 1/2 -> one and one half
    """
    ret = []
    for part in num.split():
        if part in FRACTIONS:
            ret.append(FRACTIONS[part])
        else:
            ret.append(
                " ".join(NUMBER_REPL[char] for char in part if char in NUMBER_REPL)
            )
    return " and ".join(ret)


def make_number(num: str, repr: str = None, speak: str = None) -> Number:
    """
    Returns a Number or Fraction dataclass for a number string

    NOTE: Numerators are assumed to have a single digit. Additional are whole numbers
    """
    if not num or is_unknown(num):
        return
    # Check special
    if num in SPECIAL_NUMBERS:
        return Number(repr or num, *SPECIAL_NUMBERS[num])
    # Check cardinal direction
    if num in CARDINALS:
        if not repr:
            repr = num
        num = str(CARDINALS[num])
    # Remove spurious characters from the end
    num = num.rstrip("M.")
    num = num.replace("O", "0")
    num = num.replace("+", "")
    # Create Fraction
    if "/" in num:
        nmr, dnm = num.split("/")
        dnm = int(dnm)
        # Multiply multi-digit numerator
        if len(nmr) > 1:
            nmr = int(nmr[:-1]) * dnm + int(nmr[-1])
            num = f"{nmr}/{dnm}"
        else:
            nmr = int(nmr)
        unpacked = unpack_fraction(num)
        spoken = spoken_number(unpacked)
        return Fraction(repr or num, nmr / dnm, spoken, nmr, dnm, unpacked)
    # Handle Minus values with errors like 0M04
    if "M" in num:
        val = num.replace("M", "-")
        while val[0] != "-":
            val = val[1:]
    else:
        val = num
    # Create Number
    if not val:
        return
    val = float(val) if "." in num else int(val)
    return Number(repr or num, val, spoken_number(speak or str(val)))


def find_first_in_list(txt: str, str_list: [str]) -> int:
    """
    Returns the index of the earliest occurrence of an item from a list in a string

    Ex: find_first_in_list('foobar', ['bar', 'fin']) -> 3
    """
    start = len(txt) + 1
    for item in str_list:
        if start > txt.find(item) > -1:
            start = txt.find(item)
    return start if len(txt) + 1 > start > -1 else -1


def is_timestamp(item: str) -> bool:
    """
    Returns True if the item matches the timestamp format
    """
    return len(item) == 7 and item[-1] == "Z" and item[:-1].isdigit()


def is_timerange(item: str) -> bool:
    """
    Returns True if the item is a TAF to-from time range
    """
    return (
        len(item) == 9 and item[4] == "/" and item[:4].isdigit() and item[5:].isdigit()
    )


STR_REPL = {
    " C A V O K ": " CAVOK ",
    "?": " ",
    '"': "",
    "'": "",
    "`": "",
    ".": "",
    " VTB": " VRB",
    " VBR": " VRB",
    " VBB": " VRB",
    " ERB": " VRB",
    " VRV": " VRB",
    " BRV": " VRB",
    " VRN": " VRB",
    " BRB": " VRB",
    " VEB": " VRB",
    " VFB": " VRB",
    " VAB": " VRB",
    " VAR": " VRB",
    " VRG": " VRB",
    " VRR": " VRB",
    " VGB": " VRB",
    " VRC": " VRB",
    " WBB": " VRB",
    " VR0": " VRB0",
    " VB0": " VRB0",
    " RB0": " VRB0",
    " V0": " VRB0",
    " 0I0": " 090",
    # "Z/ ": "Z ", NOTE: Too broad re pirep
    "KKT ": "KT ",
    "KLT ": "KT ",
    "CALMKT ": "CALM ",
    "N0SIG": "NOSIG",
    " <1/": " M1/",  # <1/4SM <1/8SM
    " /34SM": "3/4SM",
}


def sanitize_report_string(txt: str) -> str:
    """
    Provides sanitization for operations that work better when the report is a string

    Returns the first pass sanitized report string
    """
    txt = txt.upper()
    if len(txt) < 4:
        return txt
    # Standardize whitespace
    txt = " ".join(txt.split())
    # Prevent changes to station ID
    stid, txt = txt[:4], txt[4:]
    # Replace invalid key-value pairs
    for key, rep in STR_REPL.items():
        txt = txt.replace(key, rep)
    # Check for missing spaces in front of cloud layers
    # Ex: TSFEW004SCT012FEW///CBBKN080
    for cloud in CLOUD_LIST:
        if cloud in txt and " " + cloud not in txt:
            start, counter = 0, 0
            while txt.count(cloud) != txt.count(" " + cloud):
                cloud_index = start + txt[start:].find(cloud)
                if len(txt[cloud_index:]) >= 3:
                    target = txt[
                        cloud_index + len(cloud) : cloud_index + len(cloud) + 3
                    ]
                    if target.isdigit() or not target.strip("/"):
                        txt = txt[:cloud_index] + " " + txt[cloud_index:]
                start = cloud_index + len(cloud) + 1
                # Prevent infinite loops
                if counter > txt.count(cloud):
                    break
                counter += 1
    return stid + txt


def extra_space_exists(str1: str, str2: str) -> bool:
    """
    Return True if a space shouldn't exist between two items
    """
    ls1, ls2 = len(str1), len(str2)
    if str1.isdigit():
        # 10 SM
        if str2 in ["SM", "0SM"]:
            return True
        # 12 /10
        if ls2 > 2 and str2[0] == "/" and str2[1:].isdigit():
            return True
    if str2.isdigit():
        # OVC 040
        if str1 in CLOUD_LIST:
            return True
        # 12/ 10
        if ls1 > 2 and str1.endswith("/") and str1[:-1].isdigit():
            return True
        # 12/1 0
        if (
            ls2 == 1
            and ls1 > 3
            and str1[:2].isdigit()
            and "/" in str1
            and str1[3:].isdigit()
        ):
            return True
        # Q 1001
        if str1 in ["Q", "A"]:
            return True
    # 36010G20 KT
    if (
        str2 == "KT"
        and str1[-1].isdigit()
        and (str1[:5].isdigit() or (str1.startswith("VRB") and str1[3:5].isdigit()))
    ):
        return True
    # 36010K T
    if (
        str2 == "T"
        and ls1 >= 6
        and (str1[:5].isdigit() or (str1.startswith("VRB") and str1[3:5].isdigit()))
        and str1[-1] == "K"
    ):
        return True
    # OVC022 CB
    if (
        str2 in CLOUD_TRANSLATIONS
        and str2 not in CLOUD_LIST
        and ls1 >= 3
        and str1[:3] in CLOUD_LIST
    ):
        return True
    # FM 122400
    if str1 in ["FM", "TL"] and (
        str2.isdigit() or (str2.endswith("Z") and str2[:-1].isdigit())
    ):
        return True
    # TX 20/10
    if str1 in ["TX", "TN"] and str2.find("/") != -1:
        return True
    return False


_cloud_group = "(" + "|".join(CLOUD_LIST) + ")"
CLOUD_SPACE_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"(?=.+)" + _cloud_group + r"\d{3}(\w{2,3})?$",  # SCT010BKN021
        r"M?\d{2}\/M?\d{2}$",  # BKN01826/25
    )
]


def extra_space_needed(item: str) -> int:
    """
    Returns the index where the string should be separated or None
    """
    # For items starting with cloud list
    if item[:3] in CLOUD_LIST:
        for pattern in CLOUD_SPACE_PATTERNS:
            sep = pattern.search(item)
            if sep is None:
                continue
            if sep.start():
                return sep.start()
    # Connected timestamp
    for loc, check in ((7, is_timestamp), (9, is_timerange)):
        if len(item) > loc and check(item[:loc]):
            return loc
    # Connected to wind
    if len(item) > 5 and "KT" in item and not item.endswith("KT"):
        sep = item.find("KT")
        if sep > 4:
            return sep + 2
    # TAF newline connected to previous element
    for key in TAF_NEWLINE:
        if key in item and not item.startswith(key):
            return item.find(key)
    for key in TAF_NEWLINE_STARTSWITH:
        if key in item and not item.startswith(key):
            sep = item.find(key)
            if item[sep + len(key) :].isdigit():
                return sep


ITEM_REMV = [
    "AUTO",
    "COR",
    "NSC",
    "NCD",
    "$",
    "KT",
    "M",
    ".",
    "RTD",
    "SPECI",
    "METAR",
    "CORR",
    "TTF",
]
ITEM_REPL = {"CALM": "00000KT"}
VIS_PERMUTATIONS = ["".join(p) for p in permutations("P6SM")]
VIS_PERMUTATIONS.remove("6MPS")


def sanitize_report_list(wxdata: [str], remove_clr_and_skc: bool = True) -> [str]:
    """
    Sanitize wxData

    We can remove and identify "one-off" elements and fix other issues before parsing a line
    """
    for i, item in reversed(list(enumerate(wxdata))):
        ilen = len(item)
        # Remove elements containing only '/'
        if is_unknown(item):
            wxdata.pop(i)
            continue
        # Remove empty wind /////KT
        if item.endswith("KT") and is_unknown(item[:-2]):
            wxdata.pop(i)
            continue
        # Remove RE from wx codes, REVCTS -> VCTS
        elif ilen in [4, 6] and item.startswith("RE"):
            wxdata[i] = item[2:]
        # Fix a slew of easily identifiable conditions where a space does not belong
        elif i and extra_space_exists(wxdata[i - 1], item):
            wxdata[i - 1] += wxdata.pop(i)
        # Remove spurious elements
        elif item in ITEM_REMV:
            wxdata.pop(i)
        # Remove 'Sky Clear' from METAR but not TAF
        elif remove_clr_and_skc and item in ["CLR", "SKC"]:
            wxdata.pop(i)
        # Replace certain items
        elif item in ITEM_REPL:
            wxdata[i] = ITEM_REPL[item]
        # Remove amend signifier from start of report ('CCA', 'CCB',etc)
        elif ilen == 3 and item.startswith("CC") and item[2].isalpha():
            wxdata.pop(i)
        # Fix inconsistent 'P6SM' Ex: TP6SM or 6PSM -> P6SM
        elif ilen > 3 and item[-4:] in VIS_PERMUTATIONS:
            wxdata[i] = "P6SM"
        # Fix misplaced KT 22022KTG40
        elif ilen == 10 and "KTG" in item and item[:5].isdigit():
            wxdata[i] = item.replace("KTG", "G") + "KT"
        # Fix backwards KT Ex: 06012G22TK
        if (
            ilen >= 7
            and (item[:3].isdigit() or item[:3] == "VRB")
            and item.endswith("TK")
        ):
            wxdata[i] = item[:-2] + "KT"
        # Fix gust double G Ex: 360G17G32KT
        elif ilen > 10 and item.endswith("KT") and item[3] == "G":
            wxdata[i] = item[:3] + item[4:]
        # Fix leading character mistypes in wind
        elif (
            ilen > 7
            and not item[0].isdigit()
            and not item.startswith("VRB")
            and item.endswith("KT")
            and not item.startswith("WS")
        ):
            while not item[0].isdigit() and not item.startswith("VRB"):
                item = item[1:]
            wxdata[i] = item
        # Fix non-G gust Ex: 14010-15KT
        elif ilen == 10 and item.endswith("KT") and item[5] != "G":
            wxdata[i] = item[:5] + "G" + item[6:]
        # Fix leading digits on VRB wind Ex: 2VRB02KT
        elif (
            ilen > 7
            and item.endswith("KT")
            and "VRB" in item
            and item[0].isdigit()
            and "Z" not in item
        ):
            while item[0].isdigit():
                item = item[1:]
            wxdata[i] = item
        # Fix wind T
        elif not item.endswith("KT") and (
            (
                ilen == 6
                and item[5] in ["K", "T"]
                and (
                    item[:5].isdigit()
                    or (item.startswith("VRB") and item[:3].isdigit())
                )
            )
            or (
                ilen == 9
                and item[8] in ["K", "T"]
                and item[5] == "G"
                and (item[:5].isdigit() or item.startswith("VRB"))
            )
        ):
            wxdata[i] = item[:-1] + "KT"
        # Fix joined TX-TN
        elif ilen > 16 and len(item.split("/")) == 3:
            if item.startswith("TX") and "TN" not in item:
                tn_index = item.find("TN")
                wxdata.insert(i + 1, item[:tn_index])
                wxdata[i] = item[tn_index:]
            elif item.startswith("TN") and item.find("TX") != -1:
                tx_index = item.find("TX")
                wxdata.insert(i + 1, item[:tx_index])
                wxdata[i] = item[tx_index:]
        # Fix situations where a space is missing
        sep = extra_space_needed(item)
        if sep:
            wxdata.insert(i + 1, item[sep:])
            wxdata[i] = item[:sep]
    wxdata = dedupe(wxdata, only_neighbors=True)
    return wxdata


def is_possible_temp(temp: str) -> bool:
    """
    Returns True if all characters are digits or 'M' (for minus)
    """
    for char in temp:
        if not (char.isdigit() or char == "M"):
            return False
    return True


def get_station_and_time(wxdata: [str]) -> ([str], str, str):
    """
    Returns the report list and removed station ident and time strings
    """
    if not wxdata:
        return wxdata, None, None
    station = wxdata.pop(0)
    if not wxdata:
        return wxdata, station, None
    qtime = wxdata[0]
    if wxdata and qtime.endswith("Z") and qtime[:-1].isdigit():
        rtime = wxdata.pop(0)
    elif wxdata and len(qtime) == 6 and qtime.isdigit():
        rtime = wxdata.pop(0) + "Z"
    else:
        rtime = None
    return wxdata, station, rtime


def get_wind(wxdata: [str], units: Units) -> ([str], Number, Number, Number, [Number]):
    """
    Returns the report list and removed:
    Direction string, speed string, gust string, variable direction list
    """
    direction, speed, gust = "", "", ""
    variable = []
    if wxdata:
        item = copy(wxdata[0])
        for rep in ["(E)"]:
            item = item.replace(rep, "")
        for replacements in (("O", "0"), ("/", ""), ("LKT", "KT"), ("GG", "G")):
            item = item.replace(*replacements)
        # 09010KT, 09010G15KT
        if (
            item.endswith("KT")
            or item.endswith("KTS")
            or item.endswith("MPS")
            or item.endswith("KMH")
            or (
                (
                    len(item) == 5
                    or (len(item) >= 8 and item.find("G") != -1)
                    and item.find("/") == -1
                )
                and (
                    item[:5].isdigit()
                    or (item.startswith("VRB") and item[3:5].isdigit())
                )
            )
        ):
            # In order of frequency
            if item.endswith("KT"):
                item = item.replace("KT", "")
            elif item.endswith("KTS"):
                item = item.replace("KTS", "")
            elif item.endswith("MPS"):
                units.wind_speed = "m/s"
                item = item.replace("MPS", "")
            elif item.endswith("KMH"):
                units.wind_speed = "km/h"
                item = item.replace("KMH", "")
            direction = item[:3]
            if "G" in item:
                g_index = item.find("G")
                gust = item[g_index + 1 :]
                speed = item[3:g_index]
            else:
                speed = item[3:]
            direction = item[:3]
            wxdata.pop(0)
    # Separated Gust
    if (
        wxdata
        and 1 < len(wxdata[0]) < 4
        and wxdata[0][0] == "G"
        and wxdata[0][1:].isdigit()
    ):
        gust = wxdata.pop(0)[1:]
    # Variable Wind Direction
    if (
        wxdata
        and len(wxdata[0]) == 7
        and wxdata[0][:3].isdigit()
        and wxdata[0][3] == "V"
        and wxdata[0][4:].isdigit()
    ):
        variable = [make_number(i, speak=i) for i in wxdata.pop(0).split("V")]
    # Convert to Number
    direction = make_number(direction, speak=direction)
    speed = make_number(speed.strip("BV"))
    gust = make_number(gust)
    return wxdata, direction, speed, gust, variable


def get_visibility(wxdata: [str], units: Units) -> ([str], Number):
    """
    Returns the report list and removed visibility string
    """
    visibility = ""
    if wxdata:
        item = copy(wxdata[0])
        # Vis reported in statue miles
        if item.endswith("SM"):  # 10SM
            if item in ("P6SM", "M1/4SM", "M1/8SM"):
                visibility = item[:-2]
            elif item[:-2].isdigit():
                visibility = str(int(item[:-2]))
            elif "/" in item:
                visibility = item[: item.find("SM")]  # 1/2SM
            wxdata.pop(0)
            units.visibility = "sm"
        # Vis reported in meters
        elif len(item) == 4 and item.isdigit():
            visibility = wxdata.pop(0)
            units.visibility = "m"
        elif (
            7 >= len(item) >= 5
            and item[:4].isdigit()
            and (item[4] in ["M", "N", "S", "E", "W"] or item[4:] == "NDV")
        ):
            visibility = wxdata.pop(0)[:4]
            units.visibility = "m"
        elif len(item) == 5 and item[1:].isdigit() and item[0] in ["M", "P", "B"]:
            visibility = wxdata.pop(0)[1:]
            units.visibility = "m"
        elif item.endswith("KM") and item[:-2].isdigit():
            visibility = item[:-2] + "000"
            wxdata.pop(0)
            units.visibility = "m"
        # Vis statute miles but split Ex: 2 1/2SM
        elif (
            len(wxdata) > 1
            and wxdata[1].endswith("SM")
            and "/" in wxdata[1]
            and item.isdigit()
        ):
            vis1 = wxdata.pop(0)  # 2
            vis2 = wxdata.pop(0).replace("SM", "")  # 1/2
            visibility = str(int(vis1) * int(vis2[2]) + int(vis2[0])) + vis2[1:]  # 5/2
            units.visibility = "sm"
    return wxdata, make_number(visibility)


def sanitize_cloud(cloud: str) -> str:
    """
    Fix rare cloud layer issues
    """
    if len(cloud) < 4:
        return cloud
    if not cloud[3].isdigit() and cloud[3] not in ("/", "-"):
        if cloud[3] == "O":
            cloud = cloud[:3] + "0" + cloud[4:]  # Bad "O": FEWO03 -> FEW003
        elif cloud[3] != "U":  # Move modifiers to end: BKNC015 -> BKN015C
            cloud = cloud[:3] + cloud[4:] + cloud[3]
    return cloud


def make_cloud(cloud: str) -> Cloud:
    """
    Returns a Cloud dataclass for a cloud string

    This function assumes the input is potentially valid
    """
    els = {"type": None, "base": None, "top": None, "modifier": None}
    _c = sanitize_cloud(cloud).replace("/", "")
    # Separate top
    topi = _c.find("-TOP")
    if topi > -1:
        els["top"], _c = _c[topi + 4 :], _c[:topi]
    # Separate type
    ## VV003
    if _c.startswith("VV"):
        els["type"], _c = _c[:2], _c[2:]
    ## FEW010
    elif len(_c) >= 3 and _c[:3] in CLOUD_LIST:
        els["type"], _c = _c[:3], _c[3:]
    ## BKN-OVC065
    if len(_c) > 4 and _c[0] == "-" and _c[1:4] in CLOUD_LIST:
        els["type"] += _c[:4]
        _c = _c[4:]
    # Separate base
    if len(_c) >= 3 and _c[:3].isdigit():
        els["base"], _c = _c[:3], _c[3:]
    elif len(_c) >= 4 and _c[:4] == "UNKN":
        _c = _c[4:]
    # Remainder is considered modifiers
    if _c:
        els["modifier"] = _c
    # Nullify unknown elements and convert ints
    for k, v in els.items():
        if not isinstance(v, str):
            continue
        if is_unknown(v):
            els[k] = None
        elif v.isdigit():
            els[k] = int(v)
    # Make Cloud
    return Cloud(cloud, **els)


def get_clouds(wxdata: [str]) -> ([str], list):
    """
    Returns the report list and removed list of split cloud layers
    """
    clouds = []
    for i, item in reversed(list(enumerate(wxdata))):
        if item[:3] in CLOUD_LIST or item[:2] == "VV":
            cloud = wxdata.pop(i)
            clouds.append(make_cloud(cloud))
    # Attempt cloud sort. Fails if None values are present
    try:
        clouds.sort(key=lambda cloud: (cloud.base, cloud.type))
    except TypeError:
        clouds.reverse()  # Restores original report order
    return wxdata, clouds


def get_flight_rules(vis: Number, ceiling: Cloud) -> int:
    """
    Returns int based on current flight rules from parsed METAR data

    0=VFR, 1=MVFR, 2=IFR, 3=LIFR

    Note: Common practice is to report IFR if visibility unavailable
    """
    # Parse visibility
    if not vis:
        return 2
    if vis.repr == "CAVOK" or vis.repr.startswith("P6"):
        vis = 10
    elif vis.repr.startswith("M"):
        vis = 0
    # Convert meters to miles
    elif len(vis.repr) == 4:
        vis = vis.value * 0.000621371
    else:
        vis = vis.value
    # Parse ceiling
    cld = ceiling.base if ceiling else 99
    # Determine flight rules
    if (vis <= 5) or (cld <= 30):
        if (vis < 3) or (cld < 10):
            if (vis < 1) or (cld < 5):
                return 3  # LIFR
            return 2  # IFR
        return 1  # MVFR
    return 0  # VFR


def get_ceiling(clouds: [Cloud]) -> Cloud:
    """
    Returns ceiling layer from Cloud-List or None if none found

    Assumes that the clouds are already sorted lowest to highest

    Only 'Broken', 'Overcast', and 'Vertical Visibility' are considered ceilings

    Prevents errors due to lack of cloud information (eg. '' or 'FEW///')
    """
    for cloud in clouds:
        if cloud.base and cloud.type in ("OVC", "BKN", "VV"):
            return cloud
    return None


def parse_date(
    date: str, hour_threshold: int = 200, time_only: bool = False
) -> datetime:
    """
    Parses a report timestamp in ddhhZ or ddhhmmZ format

    If time_only, assumes hhmm format with current or previous day

    This function assumes the given timestamp is within the hour threshold from current date
    """
    # Format date string
    date = date.strip("Z")
    if not date.isdigit():
        return
    if time_only:
        if len(date) != 4:
            return
        ihour = 0
    else:
        if len(date) == 4:
            date += "00"
        if len(date) != 6:
            return
        ihour = 2
    # Create initial guess
    now = datetime.now(tz=timezone.utc)
    day = now.day if time_only else int(date[0:2])
    # Handle situation where next month has less days than current month
    # Shifted value makes sure that a month shift doesn't happen twice
    shifted = False
    if day > monthrange(now.year, now.month)[1]:
        now += relativedelta(months=-1)
        shifted = True
    try:
        guess = now.replace(
            day=day,
            hour=int(date[ihour : ihour + 2]) % 24,
            minute=int(date[ihour + 2 : ihour + 4]) % 60,
            second=0,
            microsecond=0,
        )
    except ValueError:
        return
    # Handle changing months if not already shifted
    if not shifted:
        hourdiff = (guess - now) / timedelta(minutes=1) / 60
        if hourdiff > hour_threshold:
            guess += relativedelta(months=-1)
        elif hourdiff < -hour_threshold:
            guess += relativedelta(months=+1)
    return guess


def make_timestamp(timestamp: str, time_only: bool = False) -> Timestamp:
    """
    Returns a Timestamp dataclass for a report timestamp in ddhhZ or ddhhmmZ format
    """
    if timestamp:
        return Timestamp(timestamp, parse_date(timestamp, time_only=time_only))
