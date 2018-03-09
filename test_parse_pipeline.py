from os import path
import unittest

from parse_pipeline import ParsePipeline

class TestParsePipeline(unittest.TestCase):

    def test_patient_data(self):
        pl1 = ParsePipeline('./final_data')
        print pl1.patient_data
        self.assertTrue(len(pl1.patient_data) == 5)

    def test_pair_dicom_contour_file(self):
        pl1 = ParsePipeline('./final_data')
        pair = pl1.pair_dicom_contour_file()
        for i in range(10):
            dicom, icont = next(pair)
            self.assertTrue(path.isfile(dicom))
            self.assertTrue(path.isfile(icont))

if __name__ == '__main__':
    unittest.main()
