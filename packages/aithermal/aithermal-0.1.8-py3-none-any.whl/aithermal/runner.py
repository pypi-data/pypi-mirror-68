import os
import argparse
import aithermal
import pandas as pd
import xlsxwriter
import simplelogging
import oyaml as yaml


def main():
    log = simplelogging.get_logger(file_name="aithermal.log", console=False)

    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    parameters = os.path.join(os.getcwd(), "project parameters.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="root path")

    try:
        with open(parameters, "r") as stream:
            data_loaded = yaml.safe_load(stream)
    except FileNotFoundError as e:
        data_loaded = aithermal.utils.write_yaml()
        with open("project parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the project parameters.yaml document")
        log.exception(f"{FileNotFoundError} {e}")
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))
    try:
        _run(*decompress(data_loaded))
    except TypeError as e:
        raise e
        print("Please double-check your project parameters.yaml document'")
        log.exception(e)
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))


def decompress(data_loaded):
    wavelenths = data_loaded.get("WAVE LENGTHS")
    gradient = data_loaded.get("GRADIENTS")
    # rms = data_loaded.get("RMS") #TODO: Support RMS
    root = data_loaded.get("DIRECTORY")
    isotherms = data_loaded.get("ISOTHERMS")
    baselines = data_loaded.get("BASELINE DIRECTORY")

    methods = [method for method in data_loaded.get("TECHNIQUES").keys() if method]
    topics, topic_paths = aithermal.topic_directories(root)
    method_paths = aithermal.method_directories(
        topic_paths, topics, gradient, isotherms, methods
    )
    return gradient, method_paths, root, wavelenths, baselines


def _run(gradient, method_paths, root, wavelengths, baseline_path):
    ir_list, ms_list, sta_list, gc_list = aithermal.method_sorting(method_paths)

    sta_frames = aithermal.load_dsc(sta_list, baseline_path=baseline_path, method="tg")
    ir_frames = aithermal.load_dsc(
        ir_list, method="ir", rms=False, wavelengths=wavelengths
    )
    ms_frames = aithermal.load_dsc(ms_list, method="ms", file_type="txt")

    tg_tracer = aithermal.write_topic_structured_csv(sta_frames, "TG", root)
    ir_tracer = aithermal.write_topic_structured_csv(ir_frames, "IR", root)
    ms_tracer = aithermal.write_topic_structured_csv(ms_frames, "MS", root)

    acd_ms_frame = generate_results_csv_acd(ms_tracer, "MS File")
    acd_ir_frame = generate_results_csv_acd(ir_tracer, "IR File")
    acd_tg_frame = generate_results_csv_acd(tg_tracer, "TG File")

    tracers = pd.concat([acd_ms_frame, acd_ir_frame, acd_tg_frame], axis=1)
    tracers["Gradient"] = ",".join([str(x) for x in gradient])
    tracers = tracers.reset_index()
    tracers = tracers.rename(columns={"index": "Name"})
    tracers.to_csv(os.path.join(root, "ACD Trace.csv"), index=False)


def generate_results_csv_acd(frame, prefix):
    return pd.DataFrame.from_dict(frame, orient="index").add_prefix(f"{prefix} ")


if __name__ == "__main__":
    main()
