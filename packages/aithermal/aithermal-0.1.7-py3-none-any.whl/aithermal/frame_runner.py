import os
import re
import pandas as pd
from aithermal.utils import csv_list_multi


def derivative(df):
    df = df.iloc[40:]
    delta = df[["Time", "Unsubtracted Weight"]].diff().dropna()
    delta["Unsubtracted Weight"] = (
        delta["Unsubtracted Weight"].ewm(span=50).mean().div(delta["Time"])
    )
    delta = (
        pd.concat([delta, df["Sample Temperature"]], axis=1)
        .dropna()
        .drop(columns=["Time", "Sample Temperature"], errors="ignore")
    )
    delta.rename(columns={"Unsubtracted Weight": "Derivative Weight"}, inplace=True)
    return delta


def percentage(df, column):
    percent = df[column]
    percent = percent.div(percent.max())
    percent = percent.multiply(100)
    return percent


def correct(data_frame, baseline_frame, column):
    data = data_frame
    if baseline_frame:
        data = data_frame[column]
        correction = baseline_frame[column]
        data = data - correction
    return data


def baseline_load(file_path: str, columns_to_use=None):
    baselines = os.listdir(file_path)
    gradient_data = {}
    isotherm_data = {}
    gradient = [file for file in baselines if "Gradient" in file]
    isotherm = [file for file in baselines if "Isotherm" in file]
    for file in gradient:
        full = os.path.join(file_path, file)
        data_frame = pd.read_csv(full, engine="python", usecols=columns_to_use)
        gradient_data = data_frame
    for file in isotherm:
        temp = os.path.splitext(file)[0].split(" ")[-1]
        full = os.path.join(file_path, file)
        data_frame = pd.read_csv(full, engine="python", usecols=columns_to_use)
        isotherm_data[temp] = data_frame

    return {"gradient": gradient_data, "isotherm": isotherm_data}


def wl_ext(frame, wavelength):
    wave_list = []
    for wl in wavelength:
        try:
            wave_list.append(frame[wl])
        except KeyError:

            def jitter(jitter_frame, n):
                return n if n in jitter_frame.columns else jitter(jitter_frame, n + 1)

            wave_list.append(frame[jitter(frame, wl + 1)])
    extracted_frame = pd.DataFrame(wave_list).transpose().reset_index()
    extracted_frame["index"] = (
        extracted_frame["index"].astype(float).map(lambda x: x / 60).round(3)
    )
    extracted_frame.rename(columns={"index": "Time"}, inplace=True)
    return extracted_frame


def load_dsc(
    path, method, baseline_path=None, rms=False, wavelengths=None, file_type="csv"
):
    gradient = path.get("gradient")
    isotherm = path.get("isotherm")
    gradient_files = csv_list_multi(gradient, file_type)
    isotherm_files = csv_list_multi(isotherm, file_type)

    gradient_args = {"data": gradient_files.get("standard"), "method": method}
    isotherm_args = {"data": isotherm_files.get("standard"), "method": method}

    if method == "tg":
        gradient_args["columns"] = [
            "Time",
            "Unsubtracted Weight",
            "Sample Temperature",
            "Unsubtracted Heat Flow",
        ]
        isotherm_args["columns"] = [
            "Time",
            "Unsubtracted Weight",
            "Sample Temperature",
            "Unsubtracted Heat Flow",
        ]

        gradient_args["baseline_path"] = baseline_path
        isotherm_args["baseline_path"] = baseline_path

    if method == "ir":
        gradient_args["wavelength"] = [wave for wave in wavelengths if wave]
        isotherm_args["wavelength"] = [wave for wave in wavelengths if wave]
        if rms:
            gradient_args["rms"] = gradient_files.get("rms")
            isotherm_args["rms"] = gradient_files.get("rms")
    if method == "gc":
        gradient_args["data"] = [
            tic_file
            for tic_file in gradient_files.get("standard")
            if "tic" in tic_file.lower()
        ]
        isotherm_args["data"] = [
            tic_file
            for tic_file in gradient_files.get("standard")
            if "tic" in tic_file.lower()
        ]

    gradient_dictionary = helper(**gradient_args)
    isotherm_dictionary = helper(**isotherm_args)

    return {"gradient": gradient_dictionary, "isotherm": isotherm_dictionary}


def helper(**kwargs):
    data_files = kwargs.get("data")
    method = kwargs.get("method")
    wavelength = kwargs.get("wavelength")
    rms = kwargs.get("rms")
    columns_to_use = kwargs.get("columns")
    baseline = kwargs.get("baseline_path")

    topic_pattern = r"\\(Topic.*?)\\"
    isotherm_pattern = r"(Isotherm.*?)(\d{1,})"
    frame_dictionary = {}

    for file in data_files:
        data_frame = pd.DataFrame()

        if method == "ir" and wavelength:
            data_frame = ir_runner(file, wavelength)

        if method == "tg":
            data_frame = tg_runner(baseline, columns_to_use, file, isotherm_pattern)

        if method == "ms":
            data_frame = ms_runner(file)

        topic_name, name = naming(file, isotherm_pattern, topic_pattern)

        if method == "ms":
            ion = os.path.splitext(file.split("\\")[-1])[0]
            name = " ".join([name, "-", ion])

        if frame_dictionary.get(topic_name):
            frame_dictionary[topic_name][name] = data_frame
        else:
            frame_dictionary[topic_name] = {name: data_frame}

    return frame_dictionary


def ms_runner(file):
    data_frame = pd.read_table(
        file, sep="\s+", header=None, names=["Time", "Absorbance"]
    )
    data_frame["Absorbance"] = data_frame["Absorbance"].ewm(span=5).mean()
    return data_frame


def tg_runner(baseline, columns_to_use, file, isotherm_pattern):
    data_frame = pd.read_csv(file, engine="python", usecols=columns_to_use)
    deriv = derivative(data_frame)
    percent = percentage(data_frame, ["Unsubtracted Weight"])
    percent.rename(columns={"Unsubtracted Weight": "Percent Weight"}, inplace=True)
    baseline_frames = baseline_load(baseline, columns_to_use)
    if "Isotherm" in file:
        isotherm = re.search(isotherm_pattern, file)[2]
        corrective_frame = baseline_frames.get("isotherm").get(isotherm)
    else:
        corrective_frame = baseline_frames.get("gradient")
    baseline_corrected = correct(
        data_frame, corrective_frame, ["Unsubtracted Heat Flow"]
    )
    baseline_corrected.rename(
        columns={"Unsubtracted Heat Flow": "Corrected Heat Flow"}, inplace=True
    )
    data_frame = pd.concat([data_frame, deriv, percent, baseline_corrected], axis=1)
    return data_frame


def ir_runner(file, wavelength):
    data_frame = pd.read_csv(file, engine="python", header=3).dropna().transpose()
    header = data_frame.iloc[0]
    header = header.astype(float).astype(int)
    data_frame = data_frame[1:]
    data_frame.columns = header
    data_frame = wl_ext(data_frame, wavelength)
    return data_frame


def naming(file, isotherm_pattern, topic_pattern):
    topic_name = re.search(topic_pattern, file)[1]
    topic_name = topic_name.replace("Topic", "").strip()
    if "Isotherm" in file:
        isotherm = re.search(isotherm_pattern, file)[2]
        name = " ".join([topic_name, "-", isotherm])
    else:
        name = " ".join([topic_name, "-", "Gradient"])
    return topic_name, name
