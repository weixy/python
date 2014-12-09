import unittest
from ..utils.svg.data import ReportData

# Create your tests here.


def extract_csv(file_name):
    with open(file_name) as f:
        content = f.readlines()
    lines = []
    for line in content:
        l = line.split(',')
        lines.append(tuple(float(x) if '.' in x else int(x) for x in l))
    return lines

SAMPLE_DATA_INDEX = ['id',
                     'Average Response Time (sec)',
                     'Minimum Response Time (sec)',
                     'Maximum Response Time (sec)',
                     'Current Threads Number',
                     ]


class DataAnalystTest(unittest.TestCase):

    def setUp(self):
        self.test_data = extract_csv('reporting/samples/sample_data.csv')
        self.data_dict = SAMPLE_DATA_INDEX

    def test_can_load_sample_data(self):
        self.assertGreater(len(self.test_data), 0)

    def test_initial_report_data_obj(self):
        rep_data = ReportData(self.data_dict, self.test_data)
        self.assertTrue(rep_data.is_index_data_matched())
        sep_tables = rep_data.separated_tables()
        self.assertTrue(len(sep_tables) == 4)
        self.assertTrue(sep_tables[0]['title'] == 'Average Response Time (sec)')


if __name__ == '__main__':
    unittest.main(warnings='ignore')