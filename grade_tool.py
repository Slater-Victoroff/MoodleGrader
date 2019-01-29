import os
import re
import subprocess
from config import TEMP_DIR

def parse_moodle_output(zip_file):
    _make_if_not_exists(TEMP_DIR)
    unzipper = subprocess.Popen(
        "unzip %s -d %s" % (zip_file, TEMP_DIR),
        shell=True
    )
    unzipper.communicate()

    subsection = zip_file.partition("-")[-1]
    subsection = subsection.rpartition("_")[0]
    name = subsection.replace("_", "")
    _make_if_not_exists(name)
    fix_moodle_output(TEMP_DIR, name)


def fix_moodle_output(assn_dir, outdir):
    for (_, _, filenames) in os.walk(assn_dir):
        for filename in filenames:
            # Remove spaces so we can use this as a package name
            name = filename.split("_")[0].replace(" ", "").replace("-", "")
            _make_if_not_exists("%s/%s" % (outdir, name))
            file_type = filename.split(".")[-1]
            if file_type == "java":
                new_name = filename.split("_")[1]
                source = "%s/%s" % (assn_dir, filename)
                print(filename)
                java_class = open(source, encoding="utf-8", errors="ignore").read()
                modified_class = re.sub(
                    "package (.*?);",
                    "package %s;" % name,
                    java_class,
                    1  # Set to 1 so that we only replace the first instance
                )

                dest = "%s/%s/%s.java" % (outdir, name, new_name)
                with open(dest, "w") as sink:
                    sink.write(modified_class)


def _make_if_not_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

if __name__ == "__main__":
    fix_moodle_output(
        "APCS_DM_F18-Text_Excel_Checkpoint_4_(SV)--3609",
        "TextExcelCP4"
    )
