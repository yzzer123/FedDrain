# =========================================================================
# Copyright (C) 2016-2023 LOGPAI (https://github.com/logpai).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

import sys

sys.path.append("../../")
from spell.spell import LogParser
from utils import evaluator
from utils.dataset_splitter import split_chunk
import os

import pandas as pd

input_dir = "../../data/splitted_fed_spell/"  # The input directory of log file
input_dir_test = "../../data/loghub_2k/"
output_dir = "Spell_result_fed_2k/"  # The output directory of parsing results
chunk_num = 7

split_chunk(input_dir_test, input_dir, chunk_num)

benchmark_settings = {
    "HDFS": {
        "log_file": "HDFS/HDFS_2k.log",
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        "regex": [r"\/(?:[a-zA-Z0-9_.-]+\/)+[a-zA-Z0-9_.-]+", r"blk_-?\d+", r"/(\d+\.){3}\d+(:\d+)?", r"(\d+\.){3}\d+(:\d+)?"],
        "tau": 0.78,
        "st": 0.5,
        "depth": 4,
    },
    "Hadoop": {
        "log_file": "Hadoop/Hadoop_2k.log",
        "log_format": "<Date> <Time> <Level> \[<Process>\] <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.64,
        "st": 0.5,
        "depth": 4,
    },
    "Spark": {
        "log_file": "Spark/Spark_2k.log",
        "log_format": "<Date> <Time> <Level> <Component>: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\b[KGTM]?B\b", r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.55,
        "st": 0.5,
        "depth": 4,
    },
    "Zookeeper": {
        "log_file": "Zookeeper/Zookeeper_2k.log",
        "log_format": "<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>",
        "regex": [r"(/|)(\d+\.){3}\d+(:\d+)?"],
        "tau": 0.7,
        "st": 0.5,
        "depth": 4,
    },
    "BGL": {
        "log_file": "BGL/BGL_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [r"\/(?:[a-zA-Z0-9_.-]+\/)+[a-zA-Z0-9_.-]+", r"core\.\d+"],
        "tau": 0.7442,
        "st": 0.5,
        "depth": 4,
    },
    "HPC": {
        "log_file": "HPC/HPC_2k.log",
        "log_format": "<LogId> <Node> <Component> <State> <Time> <Flag> <Content>",
        "regex": [r"=\d+"],
        "tau": 0.7,
        "st": 0.5,
        "depth": 4,
    },
    "Thunderbird": {
        "log_file": "Thunderbird/Thunderbird_2k.log",
        "log_format": "<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.5,
        "st": 0.5,
        "depth": 4,
    },
    "Windows": {
        "log_file": "Windows/Windows_2k.log",
        "log_format": "<Date> <Time>, <Level>                  <Component>    <Content>",
        "regex": [r"0x.*?\s"],
        "tau": 0.7,
        "st": 0.7,
        "depth": 5,
    },
    "Linux": {
        "log_file": "Linux/Linux_2k.log",
        "log_format": "<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"\d{2}:\d{2}:\d{2}"],
        "tau": 0.5,
        "st": 0.39,
        "depth": 6,
    },
    "Android": {
        "log_file": "Android/Android_2k.log",
        "log_format": "<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>",
        "regex": [
            r"(/[\w-]+)+",
            r"([\w-]+\.){2,}[\w-]+",
            r"\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b",
        ],
        "tau": 0.96,
        "st": 0.2,
        "depth": 6,
    },
    "HealthApp": {
        "log_file": "HealthApp/HealthApp_2k.log",
        "log_format": "<Time>\|<Component>\|<Pid>\|<Content>",
        "regex": [],
        "tau": 0.6,
        "st": 0.2,
        "depth": 4,
    },
    "Apache": {
        "log_file": "Apache/Apache_2k.log",
        "log_format": "\[<Time>\] \[<Level>\] <Content>",
        "regex": [r"(\d+\.){3}\d+"],
        "tau": 0.6,
        "st": 0.5,
        "depth": 4,
    },
    "Proxifier": {
        "log_file": "Proxifier/Proxifier_2k.log",
        "log_format": "\[<Time>\] <Program> - <Content>",
        "regex": [
            r"<\d+\ssec",
            r"([\w-]+\.)+[\w-]+(:\d+)?",
            r"\d{2}:\d{2}(:\d{2})*",
            r"[KGTM]B",
        ],
        "tau": 0.85,
        "st": 0.6,
        "depth": 3,
    },
    "OpenSSH": {
        "log_file": "OpenSSH/OpenSSH_2k.log",
        "log_format": "<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>",
        "regex": [r"(\d+\.){3}\d+", r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.8,
        "st": 0.6,
        "depth": 5,
    },
    "OpenStack": {
        "log_file": "OpenStack/OpenStack_2k.log",
        "log_format": "<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>",
        "regex": [r"((\d+\.){3}\d+,?)+", r"/.+?\s", r"\d+"],
        "tau": 0.94,
        "st": 0.6,
        "depth": 10,
    },
    "Mac": {
        "log_file": "Mac/Mac_2k.log",
        "log_format": "<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>",
        "regex": [r"([\w-]+\.){2,}[\w-]+"],
        "tau": 0.74,
        "st": 0.6,
        "depth": 6,
    },
}

bechmark_result = []
for dataset, setting in benchmark_settings.items():
    print("\n=== Evaluation on %s ===" % dataset)
    indir = os.path.join(input_dir, os.path.dirname(setting["log_file"]))
    log_file = os.path.basename(setting["log_file"])
    file_name, file_type = log_file.split(".")
    train_files = [
        f"{file_name}-chunk-{i}.{file_type}" for i in range(chunk_num)
    ]

    parsers = [
        LogParser(
            log_format=setting["log_format"],
            indir=indir,
            outdir=output_dir,
            rex=setting["regex"],
            tau=setting["tau"],
        )
        for i in range(chunk_num)
    ]

    for tparser, file in zip(parsers, train_files):
        tparser.parse(file, output=False)
    
    from feddrain.feddrain import LogMerger

    in_dir_test = os.path.join(input_dir_test, os.path.dirname(setting["log_file"]))
    mergedParser = LogMerger(log_format=setting["log_format"],
            indir=in_dir_test,
            outdir=output_dir,
            rex=setting["regex"],
            depth=setting["depth"],
            st=setting["st"],).merge(parsers)
    mergedParser.parse(log_file, parse_only=True)

    F1_measure, accuracy = evaluator.evaluate(
        groundtruth=os.path.join(in_dir_test, log_file + "_structured.csv"),
        parsedresult=os.path.join(output_dir, log_file + "_structured.csv"),
    )
    bechmark_result.append([dataset, F1_measure, accuracy])

print("\n=== Overall evaluation results ===")
df_result = pd.DataFrame(bechmark_result, columns=["Dataset", "F1_measure", "Accuracy"])
df_result.set_index("Dataset", inplace=True)
print(df_result)
df_result.to_csv("Spell_bechmark_result.csv", float_format="%.6f")