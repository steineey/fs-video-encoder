import os
from os import path
import json
from pathlib import Path
from time import time, sleep
from encoder import mp4_encode
from log import Log

def parse_config(config_fp: str):
    return json.load(open(config_fp, "r"))

def encode_dir(src_dir: str, src_ext: list, log: Log):

    print(f"[{src_dir}] encode videos in dir")
    
    # directory for compressed videos
    cmp_dir = src_dir + "c"

    for f in os.listdir(src_dir):

        # filename without extension
        fn, ext = f.split(".")
        if ext not in src_ext:
            continue

        # compressed file path
        cmp_fp = path.join(cmp_dir, f"{fn}.mp4")
        Path(cmp_dir).mkdir(parents=True, exist_ok=False,)
        if(path.isfile(cmp_fp) == True):
            continue

        # source file path
        src_fp = path.join(src_dir, f)

        # temporary file path
        tmp_fp = path.join("tmp", f"{fn}.mp4")
        
        print(f"[{fn}] encode video file...")

        # encode file if file is not yet encoded
        rc = mp4_encode(src_fp, tmp_fp)

        if(rc == 0):
            # encoding exited with code 0
            os.rename(tmp_fp, cmp_fp)
            log.encoded_insert(src_fp)

def delete_encoded_src(log: Log, thresh_ms: int = 3600):
    ts = int(time()) - thresh_ms
    print(f"delete uncompressed files older than '{ts}'")
    
    for encoded in log.encoded_select(ts):
        fn = encoded[0]
        print(f"[{fn}] remove src file after encoded")
        os.remove(fn)
        log.encoded_deleted(fn)

def main():
    cfg = parse_config("config.json")
    log = Log(cfg["logdb"])
    while True:
        for src in cfg["src"]:
            encode_dir(src["dir"], src["ext"], log)
        delete_encoded_src(log, 30)
        sleep(5)

if __name__ == "__main__":
    main()