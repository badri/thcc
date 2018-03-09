import unittest


from parse_pipeline import ParsePipeline
from feed_pipeline import FeedPipeline, WrongBatchSize


class TestParsePipeline(unittest.TestCase):

    def setUp(self):
        ppl = ParsePipeline('./final_data')
        self.result = list(ppl.pair_dicom_contour_file())
        self.fpl1 = FeedPipeline(self.result, 8)

    def test_wrong_batch_size(self):
        with self.assertRaises(WrongBatchSize):
            fpl = FeedPipeline(self.result, 0)
        
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
