import logging

import numpy as np

import parsing

class WrongBatchSize(Exception):
    pass

class FeedPipeline(object):

    def __init__(self, result, batch_size):
        self.total_size = len(result)
        if batch_size <= 0 or batch_size >= self.total_size:
            raise WrongBatchSize
        self.batch_size = batch_size
        self.result = result
        self.count = 0

    def new_epoch(self):
        np.random.shuffle(self.result)
        self.count = 0

    def next_batch(self):
        images = []
        boolean_masks = []
        while len(images) != self.batch_size:
            if self.count >= self.total_size:
                return None
            dicom_img, icontour_boolean_mask = self.convert_tuple_to_img_boolean_mask(*self.result[self.count])
            self.count = self.count + 1
            if dicom_img is None:
                continue
            images.append(dicom_img)
            boolean_masks.append(icontour_boolean_mask)
        return images, boolean_masks
                
                
    def convert_tuple_to_img_boolean_mask(self, dicom_file, icontour_file):
        dcm_dict = parsing.parse_dicom_file(dicom_file)
        if dcm_dict is None:
            logging.warning('Dicom file invalid: ' + dicom_file)
            return (None, None)
        dicom_img = dcm_dict['pixel_data']
        coords_lst = parsing.parse_contour_file(icontour_file)
        if len(coords_lst) == 0:
            logging.warning('Inner contour file empty: ' + icontour_file)
            return (None, None)
        icontour_boolean_mask = parsing.poly_to_mask(coords_lst, dicom_img.shape[0], dicom_img.shape[1])
        return (dicom_img, icontour_boolean_mask)
            
            
        
