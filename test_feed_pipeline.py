import unittest


from parse_pipeline import ParsePipeline
from feed_pipeline import FeedPipeline, WrongBatchSize


class TestParsePipeline(unittest.TestCase):

    def setUp(self):
        ppl = ParsePipeline('./final_data')
        self.result = list(ppl.pair_dicom_contour_file())
        self.fpl1 = FeedPipeline(self.result, 8)
        self.valid_dicom_file = './test_data/dicoms/study-1/48.dcm'
        self.invalid_dicom_file = './test_data/dicoms/study-1/invalid.dcm'
        self.valid_icontour_file = './test_data/contourfiles/cf-1/i-contours/IM-0001-0048-icontour-manual.txt'
        self.invalid_icontour_file = './test_data/contourfiles/cf-1/i-contours/invalid-icontour.txt'

    def test_wrong_batch_size(self):
        with self.assertRaises(WrongBatchSize):
            fpl = FeedPipeline(self.result, 0)
        
    def test_convert_tuple_to_img_boolean_mask_invalid_dicom(self):
        (dicom_img, boolean_mask) = self.fpl1.convert_tuple_to_img_boolean_mask(self.invalid_dicom_file, self.valid_icontour_file)
        self.assertIsNone(dicom_img)
        self.assertIsNone(boolean_mask)

    def test_convert_tuple_to_img_boolean_mask_invalid_icontour(self):
        (dicom_img, boolean_mask) = self.fpl1.convert_tuple_to_img_boolean_mask(self.valid_dicom_file, self.invalid_icontour_file)
        self.assertIsNone(dicom_img)
        self.assertIsNone(boolean_mask)

    def test_convert_tuple_to_img_boolean_mask(self):
        (dicom_img, boolean_mask) = self.fpl1.convert_tuple_to_img_boolean_mask(self.valid_dicom_file, self.valid_icontour_file)
        self.assertEqual(dicom_img.shape, boolean_mask.shape)

    def test_feeder_iter(self):
        for img,mask in iter(self.fpl1.next_batch, None):
            self.assertEqual(len(img), self.fpl1.batch_size)
            self.assertEqual(len(mask), self.fpl1.batch_size)

    def test_new_ipoch(self):
        ppl = ParsePipeline('./test_data')
        result = list(ppl.pair_dicom_contour_file())
        fpl1 = FeedPipeline(result, 1)
        for img,mask in iter(fpl1.next_batch, None):
            print img
            print mask

    def test_feeder_iter_ends(self):
        self.fail()
        
if __name__ == '__main__':
    unittest.main()
