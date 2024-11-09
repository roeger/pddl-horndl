import os
import re
import argparse

def read_names():
    path = "benchmarks/robot/original"
    # only read files that starts with TTL
    files = [f for f in os.listdir(path) if f.startswith("TTL")]
    names = [f.split(".")[0] for f in files]
    with open("names.txt", "w") as f:
        # write them into a list
        for i, name in enumerate(names):
            name = re.sub(r'\D', '', name)
            if i == 0:
                f.write("[" + name)
            else:
                f.write(", " + name)
            if i == len(names) - 1:
                f.write("]")

def parse_planner_time(output):
    if re.search(r"Search stopped without finding a solution.", output):
        return ""
    last_line = output.split("\n")[-1]
    time = last_line.split(" ")[-1]
    return time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--csv")
    args = parser.parse_args()
    output = args.output
    output_csv = args.csv
    time = parse_planner_time(output)
    with open(output_csv, "a") as f:
        f.write(time + ",")
