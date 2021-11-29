import cProfile, pstats, io
import re


def profile_csv(fnc):

    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        result = io.StringIO()

        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=result).sort_stats(sortby)
        ps.print_stats()

        result = result.getvalue()

        result = "ncalls" + result.split("ncalls")[-1]
        rows = [",".join(line.rstrip().split(None, 5)) for line in result.split("\n")]
        rows[0] = rows[0].replace(":lineno(function)", ",,line,function")
        for i, row in enumerate(rows):
            search1 = re.search("C:\\\\(.+[\\\\/])+", row)
            if not search1 is None:
                row = row.replace(search1.group(0), "")
            search2 = re.search(":(\\d+)\\((\\w+)\\)", row)
            if not search2 is None:
                row = row.replace(search2.group(0), f",,{search2.group(1)},{search2.group(2)}")
            rows[i] = row

        table = "\n".join(rows)

        with open("profile.csv", "w+") as f:
            # f=open(result.rsplit('.')[0]+'.csv','w')
            f.write(table)
            f.close()

        return retval

    return inner


def profile_console(fnc):

    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
