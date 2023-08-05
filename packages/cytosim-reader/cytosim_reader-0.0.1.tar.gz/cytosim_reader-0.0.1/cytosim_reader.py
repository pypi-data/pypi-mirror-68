from typing import List
import os
import tempfile
import subprocess
import numpy as np
import pandas as pd


Lines = str


class CytosimReader:

    def __init__(self, folder: str, report_executable='report'):
        self.folder = os.path.abspath(folder)
        self._folder_reports = os.path.join(folder, 'reports')
        if not os.path.exists(self._folder_reports):
            os.mkdir(self._folder_reports)
        if not os.path.isdir(self._folder_reports):
            msg = 'CytosimReader wants to put reports into folder "{}".'.format(self._folder_reports)
            msg += ' But there is a file with that name! Please move that file if you want to use CytosimReader.'
            raise RuntimeError(msg)
        self.report_exe = report_executable

    def read_report(self, report_identifier: str, clear=False) -> List['ReportBlock']:
        split_report_identifier = report_identifier.split(':')
        split_report_identifier = [s.strip() for s in split_report_identifier]
        fname_report = '_'.join(split_report_identifier) + '.txt'
        fname_report = os.path.join(self._folder_reports, fname_report)

        if clear:
            if os.path.exists(fname_report):
                os.remove(fname_report)
        if not os.path.exists(fname_report):
            self._generate_report(report_identifier, fname_report)

        return CytosimReader._parse_report_file(fname_report)

    def read_end_to_end_distances(self) -> np.ndarray:
        raise NotImplementedError

    @staticmethod
    def _parse_report_file(fname) -> List['ReportBlock']:
        blocks = []
        current_block = []
        with open(fname, 'rt') as fh:
            for line in fh:
                if not line or line.isspace():
                    continue
                if line.startswith('% end'):
                    blocks.append(ReportBlock.parse(current_block))
                    current_block = []
                    continue
                current_block.append(line)
        return blocks

    def _generate_report(self, report_identifier, fname_report):
        command_args = [self.report_exe, report_identifier]
        with open(fname_report, 'wt') as fh:
            subprocess.call(command_args, cwd=self.folder, stdout=fh)

    @staticmethod
    def aggregate(report_blocks: List['ReportBlock']) -> pd.DataFrame:
        cols = report_blocks[0].data.columns
        cols = cols.insert(0, 'time').insert(0, 'frame')
        df = pd.DataFrame(columns=cols)
        for block_i in report_blocks:
            index = block_i.data.index + len(df)
            block_i.data.index = index
            df_i = pd.DataFrame(columns=cols, index=index)
            df_i['time'] = block_i.time
            df_i['frame'] = block_i.frame
            df_i[block_i.data.columns] = block_i.data[block_i.data.columns]
            df = df.append(df_i)
        return df


class ReportBlock:

    def __init__(self, frame: int, time: float, label: str,
                 info: List[str], column_names: str,
                 data_block: str):
        self.frame = frame
        self.time = time
        self.label = label
        self.info = info
        self.data = ReportBlock.read_data(column_names, data_block)

    @staticmethod
    def read_data(column_names: str, data_block: str) -> pd.DataFrame:
        tf = tempfile.TemporaryFile('w+t')
        tf.write(column_names)
        tf.write(data_block)
        tf.seek(0)

        data = pd.read_csv(tf, delim_whitespace=True)
        return data

    @staticmethod
    def parse(block: List[Lines]) -> 'ReportBlock':
        frame = ReportBlock._parse_frame(block[0])
        time = ReportBlock._parse_time(block[1])
        label = ReportBlock._parse_label(block[2])
        first_data_line = None
        for i in range(3, len(block)):
            if block[i].startswith('%'):
                continue
            first_data_line = i
            break
        if first_data_line is None:
            msg = "No data found in this block. CytosimReader can't handle your file. "
            msg += "You can open a new issue on the project page gitlab.gwdg.de/ikuhlem/cytosim-reader "
            raise RuntimeError()
        info = block[3: first_data_line-1]
        column_names = block[first_data_line-1][2:]
        data_block = ''.join(block[first_data_line:])
        return ReportBlock(frame, time, label, info, column_names, data_block)

    @staticmethod
    def _parse_frame(line) -> int:
        s = line.split()
        assert s[1] == 'frame', "This line does not contain the current frame number."
        return int(s[2])

    @staticmethod
    def _parse_time(line) -> float:
        s = line.split()
        assert s[1] == 'time', "This line does not contain the time of the current frame."
        return float(s[2])

    @staticmethod
    def _parse_label(line):
        s = line.split()
        assert s[1] == 'report', "This line does not contain the report label."
        return ' '.join(s[2:])

    def __str__(self):
        return "ReportBlock \"{}\", frame {}".format(self.label, self.frame)

    def __repr__(self):
        return self.__str__()
