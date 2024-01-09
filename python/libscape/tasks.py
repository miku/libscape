import os
from gluish.task import BaseTask
from gluish.utils import shellout
from gluish.format import Zst
import xdg_base_dirs

# default_data_home is the default fs location for all task artifacts
default_data_home = os.path.join(xdg_base_dirs.xdg_data_home(), "libscape")

# task_tag is a unique tag, will appear in each filename
task_tag = "tag-{}".format(datetime.today())

# config contains configurable values for keys
config = {
    "oai": "https://archive.org/download/oai_harvest_2023-11-01/2023-11-01-metha-oai.ndjson.zst",
    # TODO: crossref: use newer version from: https://archive.org/details/crossref-2023-12-01 when available
    "crossref": "https://archive.org/download/crossref-2023-07-13/crossref-2023-07-13.ndjson.zst",
    # rclone aws:/openalex-snaphot sync dir
    "openalex": "/home/tir/code/miku/refnotes/data/openalex-snapshot",
}



class Task(BaseTask):
    # allow the user to override data home with environment variable
    BASE = os.environ.get("LIBSCAPE_DATA_HOME", default_data_home)
    tag = luigi.Parameter(task_tag)


class OAIDownload(Task):
    def run(self):
        output = shellout("wget -O {output} -c {url}", url=urls["oai"])
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=Zstd)


class CrossrefDownload(Task):
    def run(self):
        output = shellout("wget -O {output} -c {url}", url=urls["crossref"])
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=Zstd)


class OpenAlexWorksSnapshot(Task):
    """
    This requires rclone. It should run separately, we only want the path to
    the snapshot here to build a single file version.

    $ rclone sync --transfers=8 --checkers=16 -P aws:/openalex openalex-snapshot

    $ du -hs *
    30G     authors
    261M    concepts
    25M     funders
    151M    institutions
    893M    merged_ids
    6.7M    publishers
    76M     sources
    370G    works
    """
    def run(self):
        output = shellout("""
                          find {dir} -type f -name "*gz" |
                          parallel -j 8 zcat |
                          zstd -c9 >> {output}
                          """, dir=config["openalex"])
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=Zstd)


class DataCiteDownload(Task):
    pass


class PubmedDownload(Task):
    pass


class RGDownload(Task):
    pass


class DOAJDownload(Task):
    pass


class OpenLibraryDownload(Task):
    pass


class DBLPDownload(Task):
    pass
