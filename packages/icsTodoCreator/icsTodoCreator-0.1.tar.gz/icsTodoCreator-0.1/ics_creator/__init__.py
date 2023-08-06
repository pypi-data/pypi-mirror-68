from typing import List
import random
import string
from datetime import datetime, timedelta


def get_random_letter(options: str = string.ascii_lowercase + string.digits):
    return random.choice(options)


def get_random_uid() -> str:
    return "-".join(
        [
            "".join([get_random_letter() for i in range(8)]),
            "".join([get_random_letter() for i in range(4)]),
            "".join([get_random_letter() for i in range(4)]),
            "".join([get_random_letter() for i in range(4)]),
            "".join([get_random_letter() for i in range(12)]),
        ]
    )


class Event:
    def __init__(
            self,
            summary: str,
            _type: str = "VTODO",
            uid: str = get_random_uid(),
            created: str = datetime.now().strftime("%Y%m%dT%H%M%S"),
            last_modified: str = datetime.now().strftime("%Y%m%dT%H%M%S"),
            dtstamp: str = (datetime.now()).strftime("%Y%m%dT%H%M%S"),
            dtstart: str = (datetime.now()).strftime("%Y%m%dT%H%M%S"),
            due: str = None,
            status: str = "NEEDS-ACTION",
            percent_complete: [str, int, float] = 0,
            priority: [str, int] = 0,
            categories: [List[str], str] = None,
            description: str = None):
        val = locals().copy()
        self.val = {
            x.lstrip("_").replace("_", "-"): (
                val[x] if type(val[x] == str)
                else (",".join(val[x]) if val[x] is not None else "")
            )
            for x in val if val[x] if x != "self"
        }

    def __iter__(self):
        return self.val.__iter__()

    def __getitem__(self, item):
        return self.val.__getitem__(item)

    def __str__(self):
        return "\n".join(
            [
                "BEGIN:" + self.val["type"],
                "\n".join(
                    [x.upper() + ":" + str(self.val[x] or 0)
                     for x in self.val
                     if x != "type"]
                ),
                "END:" + self.val["type"],
            ]
        )


def write_tasks(header: dict = None,
                filename: str = "output.ics",
                tasks: List[Event] = None):
    header = header or {
        "version": "2.0",
        "calscale": "GREGORIAN",
        "prodid": "-//SabreDAV//SabreDAV//EN",
        "x-wr-calname": "icsToDoCreator",
        "refresh-interval;value=duration": "PT4H",
        "x-published-ttl": "PT4H"
    }
    file = open(filename, "w")
    file.write("BEGIN:VCALENDAR\n")
    file.write("\n".join([x.upper() + ":" + header[x] for x in header]) + "\n")
    for t in tasks:
        file.write(str(t) + "\n")
    file.write("END:VCALENDAR\n")


def example():
    write_tasks(
        filename="output.ics",
        tasks=[
            Event(
                f"Test Model 0.{i+1}",
                description="url://to.file/download",
                categories="test print",
                uid=get_random_uid(),

            )
            for i in range(2)
        ]
    )


if __name__ == "__main__":
    example()
