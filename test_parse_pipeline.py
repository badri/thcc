from os import path
import unittest

from parse_pipeline import ParsePipeline

class TestParsePipeline(unittest.TestCase):

    def setUp(self):
        # TODO: change to test_data
        self.pl1 = ParsePipeline('./final_data')
        self.valid_dicom_file = './test_data/dicoms/study-1/48.dcm'
        self.invalid_dicom_file = './test_data/dicoms/study-1/invalid.dcm'
        self.valid_icontour_file = './test_data/contourfiles/cf-1/i-contours/IM-0001-0048-icontour-manual.txt'
        self.invalid_icontour_file = './test_data/contourfiles/cf-1/i-contours/invalid-icontour.txt'
        
    def test_patient_data(self):
        self.assertTrue(len(self.pl1.patient_data) == 5)

    def test_find_dicom_file_for_icontour_file_invalid_icontour_file_hyphen(self):
        pl = ParsePipeline('./test_data')
        ret = pl.find_dicom_file_for_icontour_file('./test_data/dicoms/study-2', './test_data/contourfiles/cf-2/i-contours/invalid-icontour.txt')
        self.assertIsNone(ret)

    def test_find_dicom_file_for_icontour_file_invalid_icontour_file_nohyphen(self):
        pl = ParsePipeline('./test_data')
        ret = pl.find_dicom_file_for_icontour_file('./test_data/dicoms/study-2', './test_data/contourfiles/cf-2/i-contours/invalidicontour.txt')
        self.assertIsNone(ret)

    def test_find_dicom_file_for_icontour_file_non_existent(self):
        pl = ParsePipeline('./test_data')
        ret = pl.find_dicom_file_for_icontour_file('./test_data/dicoms/study-2', './test_data/contourfiles/cf-2/i-contours/IM-0001-0147-icontour-manual.txt.txt')
        self.assertIsNone(ret)

    def test_find_dicom_file_for_icontour_file(self):
        pl = ParsePipeline('./test_data')
        ret = pl.find_dicom_file_for_icontour_file('./test_data/dicoms/study-2', './test_data/contourfiles/cf-2/i-contours/IM-0001-0140-icontour-manual.txt.txt')
        self.assertEqual(ret, './test_data/dicoms/study-2/140.dcm')
        ret = pl.find_dicom_file_for_icontour_file('./test_data/dicoms/study-2', './test_data/contourfiles/cf-2/i-contours/IM-0001-0127-icontour-manual.txt.txt')
        self.assertEqual(ret, './test_data/dicoms/study-2/127.dcm')

    def test_pair_dicom_contour_file(self):
        #TODO: add corresponding test data
        pair = self.pl1.pair_dicom_contour_file()
        for i in range(10):
            dicom_file, icontour_file = next(pair)
            # TODO: add more testing criteria, if filenames are similar

if __name__ == '__main__':
    unittest.main()
