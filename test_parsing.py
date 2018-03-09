import unittest
import numpy as np
import parsing

class TestParsing(unittest.TestCase):

    def test_parse_dicom_valid(self):
        dcm_dict = parsing.parse_dicom_file('test_data/dicoms/study-1/48.dcm')
        self.assertIsNotNone(dcm_dict)

    def test_parse_dicom_invalid(self):
        dcm_dict = parsing.parse_dicom_file('test_data/dicoms/study-1/invalid.dcm')
        self.assertIsNone(dcm_dict)

    def test_parse_i_contour_valid(self):
        coords = parsing.parse_contour_file('test_data/contourfiles/cf-1/i-contours/IM-0001-0048-icontour-manual.txt')
        self.assertTrue(len(coords) > 0)

    def test_parse_i_contour_invalid(self):
        coords = parsing.parse_contour_file('test_data/contourfiles/cf-1/i-contours/invalid-icontour.txt')
        self.assertTrue(len(coords) == 0)

    def test_poly_to_mask_valid(self):
        dcm_dict = parsing.parse_dicom_file('test_data/dicoms/study-1/48.dcm')
        coords = parsing.parse_contour_file('test_data/contourfiles/cf-1/i-contours/IM-0001-0048-icontour-manual.txt')
        dicom_img = dcm_dict['pixel_data']
        boolean_mask = parsing.poly_to_mask(coords, dicom_img.shape[0], dicom_img.shape[1])
        #TODO: check if contents of boolean mask are correct
        self.assertTrue(boolean_mask.shape == dicom_img.shape)

    def test_poly_to_mask_invalid(self):
        self.fail()
        
if __name__ == '__main__':
    unittest.main()
