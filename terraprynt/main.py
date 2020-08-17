import hcl2
import hcl
import os
import pprint
import pandas as pd
import numpy as np
import svgwrite
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=4)

dir_path = os.path.dirname(os.path.realpath(__file__))
file_list = []
file_list.append(f"{dir_path}{os.sep}demo{os.sep}subnets.tf")
file_list.append(f"{dir_path}{os.sep}demo{os.sep}servers.tf")
file_list.append(f"{dir_path}{os.sep}demo{os.sep}network.tf")
full_file = f"{dir_path}{os.sep}full_file.tf"

all_files = ""
for file in file_list:
    with open(file, "r") as f:
        all_files += f.read()
# obj = hcl.load(all_files)
with open(full_file, "w+") as ff:
    ff.write(all_files)


# hcl.parser.DEBUG = True
with open(full_file, "r") as fp:
    obj = hcl.load(fp)

# pp.pprint(obj)
resources = []
# pp.pprint(obj["resource"]["aws_eip"]["example_machine"]["instance"])
for resource_type, value in obj["resource"].items():
    # print(resource_type)
    for resource_name, value_resource in value.items():
        df = pd.DataFrame.from_dict(value_resource, orient="index")
        df = df.reset_index()
        df = df.rename(columns={"index": "feature_key", 0: "feature_value"})
        df["resource_name"] = resource_type
        df["resource_key"] = f"{resource_type}.{resource_name}"
        resources.append(df)

df_result = pd.concat(resources)
df_resources = df_result[["resource_key"]].drop_duplicates()
dict_cnt = {}
for resource in df_resources["resource_key"]:
    print(resource)
    filter_cnt = df_result["feature_value"].str.contains(resource).sum()
    dict_cnt[resource] = filter_cnt
    print(dict_cnt)
df_resources["level_y"] = df_resources["resource_key"].map(dict_cnt)

df_resources["level_x"] = df_resources.groupby(["level_y"]).cumcount()
print(tabulate(df_result, headers="keys", tablefmt="psql"))
print(tabulate(df_resources, headers="keys", tablefmt="psql"))


def calc_pos(
    size=(250, 70), lvl=(0, 0), object_distance=(100, 200), start_pos=(10, 10)
):
    x = start_pos[0] + size[0] * lvl[0] + object_distance[0] * lvl[0]
    y = start_pos[1] + size[1] * lvl[1] + object_distance[1] * lvl[1]
    return (x, y)


def calc_text_in_rect(position, size, text, text_factor):
    x = (position[0] + size[0] / 2) - len(text) * text_factor
    y = position[1] + size[1] / 2
    return (x, y)


dwg = svgwrite.Drawing("test.svg", profile="tiny", viewBox=("0 0 2000 1000"))

rect_size = (450, 70)
start_position = (50, 50)
text_factor = 3.5

dict_rect = {}
# rect_pos.append(calc_pos(size=rect_size, lvl=(0, 0), start_pos=start_position))
for index, row in df_resources.iterrows():
    dict_rect[row["resource_key"]] = calc_pos(
        size=rect_size, lvl=(row["level_x"], row["level_y"]), start_pos=start_position,
    )

for rect_text, rect_p in dict_rect.items():
    print(rect_text)
    print(rect_p)
    rect = dwg.rect(
        insert=rect_p,
        size=rect_size,
        stroke=svgwrite.rgb(10, 10, 16, "%"),
        fill="white",
    )
    text = dwg.text(
        rect_text, insert=calc_text_in_rect(rect_p, rect_size, rect_text, text_factor),
    )
    dwg.add(rect)
    dwg.add(text)

# write svg file to disk
dwg.save()

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("test.svg")
renderPM.drawToFile(drawing, "test.png", fmt="PNG")
