import datetime
import os
import re
from collections import defaultdict


def write_yaml():
    return {
        "BASELINE DIRECTORY": "",
        "PROJECT DIRECTORY": "",
        "WAVE LENGTHS": [None, None, None, None],
        "GRADIENT": 30,
        # "RMS": False, TODO: Support RMS
        "ISOTHERMS": [190, 220, 350],
        "TECHNIQUES": {"STA": True, "IR": True, "GC": False, "MS": True},
    }


def write_sheets(frames, method, writer):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_excel(writer, sheet_name=f"{method} {name}", index=False)


def write_csv(frames, method):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_csv(os.path.join("out", f"{name}_{method}.csv"), index=False)


def write_topic_structured_csv(frames, method, out_path):
    tracer = {}
    try:
        os.mkdir(os.path.join(out_path, "data_files_for_acd"))
    except OSError:
        pass
    out_path = os.path.join(out_path, "data_files_for_acd")
    for isograd in frames:
        # Gradient / Isotherm:
        for topic in frames[isograd]:
            # Topic
            i = 0
            for name, frame in frames[isograd][topic].items():
                # Frames
                _path = os.path.join(out_path, f"{name}_{method}.csv")
                if tracer.get(topic):
                    tracer[topic].append(_path)
                else:
                    tracer[topic] = [_path]
                frame.to_csv(_path, index=False)
    return tracer


def csv_list(file_path):
    root_dir = file_path
    files = []
    for dir_, _, files in os.walk(root_dir):
        files = [
            os.path.relpath(os.path.join(root_dir, dirpath, file), root_dir)
            for (dirpath, dirnames, filenames) in os.walk(root_dir)
            for file in filenames
            if re.match("^.*.csv$", file, flags=re.IGNORECASE)
        ]

    compiled_pattern = r".*compiled.*"
    if files:
        compiled_file = list(filter(lambda x: re.search(compiled_pattern, x), files))
        if compiled_file:
            files.remove(compiled_file[0])
    return files


def csv_list_multi(file_path: list, mode="csv"):
    from glob import glob

    files = []
    rms_files = []
    for file in file_path:
        files.append(glob(file + f"\\*.{mode}"))
    files = [f for y in files for f in y if f]
    rms_pattern = r"(RMS Intensity Profile)"
    compiled_pattern = r"(.*compiled.*)"
    if files:
        compiled_file = list(filter(lambda x: re.search(compiled_pattern, x), files))
        rms = list(filter(lambda x: re.search(rms_pattern, x), files))
        files = list(set(files) - set(compiled_file) - set(rms))
        rms_files.extend(rms)
    return {"standard": files, "rms": rms_files}


def name(file):
    pattern = r"[_]([2]\d{6}.*)"
    lims_pattern = r"[_](\d{7})[_]"
    search_string = r"[a-zA-Z].+"
    free_text = re.search(search_string, file[:-4]).group(0)
    lims = re.search(lims_pattern, file).group(1)
    name = "_".join([str(lims), free_text])
    return name


def excel_pathing(path, isograd):
    excel_path = os.path.join(path, f"{isograd}" f"_{datetime.date.today()}.xlsx")
    return excel_path


def find_nearest_non_null(f):
    for col in f.columns:
        df = f[col]
        if df.isnull().any():
            df[df.isnull().idxmax()] = df[df.isnull().idxmin()]


def topic_directories(path) -> (list, list):
    topics = [topic for topic in os.listdir(path) if re.search(r"^Topic", topic)]

    directories = [
        os.path.join(path, topic)
        for topic in topics
        if os.path.isdir(os.path.join(path, topic))
    ]

    return topics, directories


def method_directories(topic_paths, topics, gradient, isotherms, methods):
    full = defaultdict(list)
    temp = defaultdict()
    md = _construct_methods_listing(gradient, isotherms, methods)
    for topic_directory, topic in zip(topic_paths, topics):
        for key in md.keys():
            for item in md[key]:
                full[key].append(os.path.join(topic_directory, item))
        temp[topic] = full.copy()
        full.clear()
    return temp


def method_sorting(method_paths):
    ir_list = defaultdict(list)
    ms_list = defaultdict(list)
    sta_list = defaultdict(list)
    gc_list = defaultdict(list)

    print("Running")
    for topic in method_paths.keys():
        for isograd in method_paths[topic].keys():
            for method in method_paths[topic][isograd]:
                technique = method.split("\\")[-1]
                if technique == "IR":
                    ir_list[isograd].append(method)
                if technique == "STA":
                    sta_list[isograd].append(method)
                if technique == "MS":
                    ms_list[isograd].append(method)
                if technique == "GC":
                    gc_list[isograd].append(method)
    return ir_list, ms_list, sta_list, gc_list


def _construct_methods_listing(gradient, isotherms, methods):
    root = ["Data"]
    type = ["Gradient", ["Gradient", "Isotherm"]][len(isotherms) > 0]
    method_dict = defaultdict(list)
    for m in methods:
        for t in type:
            if t == "Isotherm":
                for i in isotherms:
                    for r in root:
                        method_dict["isotherm"].append(f"{r}\\{t}\\{i}\\{m}")
            else:
                for r in root:
                    method_dict["gradient"].append(f"{r}\\{t}\\{gradient}\\{m}")
                for r in root:
                    method_dict["gradient"].append(f"{r}\\{t}\\{m}")

    return method_dict
