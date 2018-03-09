from parse_pipeline import ParsePipeline
from feed_pipeline import FeedPipeline
p = ParsePipeline('./final_data')
result = list(p.pair_dicom_contour_file())
f = FeedPipeline(result, 8)

for img,mask in iter(f.next_batch, None):
    print img
    print mask

