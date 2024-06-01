from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime
import json

NOGIZAKA46 = "乃木坂46"
MEMBERS_LIST = [
    ("山下美月", "Yamashita Mizuki"),
    ("与田祐希", "Yoda Yuuki"),
    ("筒井あやめ", "Tsutsui Ayame"),
    ("菅原咲月", "Sugawara Satsuki"),
    ("川﨑桜", "Kawasaki Sakura"),
    ("賀喜遥香", "Kaki Haruka"),
    ("池田瑛紗", "Ikeda Teresa"),
]
CURRENT_DATETIME = datetime.now()


def main():
    results = list()

    for name in MEMBERS_LIST:
        msg_headers = get_message_headers_by_name(name[0])
        insight = get_insight(msg_headers)
        results.append({"name": name[1], "data": insight})

    print(json.dumps(results))
    
    # print_in_format(results)


def get_base_path():
    return Path(__file__).parent.resolve()


def get_message_headers_by_name(name):
    path = join(get_base_path(), NOGIZAKA46, name)
    files = [f for f in listdir(path) if isfile(join(path, f))]

    s = set()
    for f in files:
        f_name = f.split(".")[0]
        s.add(f_name)

    msg_headers = list()
    for f in s:
        f_name_splited = f.split("_")
        f_date_time = f_name_splited[2]
        msg_header_date = datetime(
            int(f_date_time[0:4]),
            int(f_date_time[4:6]),
            int(f_date_time[6:8]),
            int(f_date_time[9:10]),
            int(f_date_time[10:12]),
            int(f_date_time[12:14]),
        )
        msg_header = (int(f_name_splited[0]), int(f_name_splited[1]), msg_header_date)
        msg_headers.append(msg_header)

    msg_headers.sort(key=lambda msg_header: msg_header[0])

    return msg_headers


def get_diff_datetime_in_days(left_datetime, right_datetime):
    diff = left_datetime - right_datetime
    return diff.days


def get_insight(msg_headers):
    txt_counter, image_counter, video_counter, call_counter = 0, 0, 0, 0
    for msg_h in msg_headers:
        if msg_h[1] == 0:
            txt_counter += 1
        elif msg_h[1] == 1:
            image_counter += 1
        elif msg_h[1] == 2:
            video_counter += 1
        elif msg_h[1] == 3:
            call_counter += 1

    total_active_day = get_diff_datetime_in_days(CURRENT_DATETIME, msg_headers[0][2])
    total_msgs = len(msg_headers)

    avg_msg_per_day = round(total_msgs / total_active_day, 2)
    avg_txt_per_day = round(txt_counter / total_active_day, 2)
    avg_img_per_day = round(image_counter / total_active_day, 2)
    avg_video_per_day = round(video_counter / total_active_day, 2)
    avg_call_per_day = round(call_counter / total_active_day, 2)

    txt_percent = round((txt_counter / total_msgs) * 100, 2)
    image_percent = round((image_counter / total_msgs) * 100, 2)
    video_percent = round((video_counter / total_msgs) * 100, 2)
    call_percent = round((call_counter / total_msgs) * 100, 2)

    insight = {
        "total_active_day": total_active_day,
        "total_msgs": total_msgs,
        "txt_counter": txt_counter,
        "image_counter": image_counter,
        "video_counter": video_counter,
        "call_counter": call_counter,
        "avg_msg_per_day": avg_msg_per_day,
        "avg_txt_per_day": avg_txt_per_day,
        "avg_img_per_day": avg_img_per_day,
        "avg_video_per_day": avg_video_per_day,
        "avg_call_per_day": avg_call_per_day,
        "txt_percent": txt_percent,
        "image_percent": image_percent,
        "video_percent": video_percent,
        "call_percent": call_percent,
    }

    return insight


def print_in_format(results):
    for r in results:
        print(f"-{r["name"]}-")
        print(f"Total active days: {r["data"]["total_active_day"]}")
        print(f"Total message: {r["data"]["total_msgs"]}")
        print(f"Total only Text: {r["data"]["txt_counter"]}")
        print(f"Total image (with and without text): {r["data"]["image_counter"]}")
        print(f"Total video: {r["data"]["video_counter"]}")
        print(f"Total call: {r["data"]["call_counter"]}")
        print("---")
        print("Average per day for each type")
        print("All type, Only text, Image (with and without text), Video, Call")
        print(
            f"{r["data"]["avg_msg_per_day"]}, {r["data"]["avg_txt_per_day"]}, {r["data"]["avg_img_per_day"]}, {r["data"]["avg_video_per_day"]}, {r["data"]["avg_call_per_day"]}"
        )
        print("---")
        print("Message ratio for each type")
        print("Only text, Image (with and without text), Video, Call")
        print(
            f"{r["data"]["txt_percent"]}, {r["data"]["image_percent"]}, {r["data"]["video_percent"]}, {r["data"]["call_percent"]}"
        )
        print()


main()
