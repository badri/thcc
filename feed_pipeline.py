import logging
import random

import numpy as np

import parsing

class WrongBatchSize(Exception):
    """
    Use to handle boundary conditions of batch size.
    """
    pass

class FeedPipeline(object):
    """
    Takes the results from previous parser pipeline and feeds it to a deep learning model.
    Example usage:
        fpl = FeedPipeline(result, 4) # result is got from previous pipeline.
        for img_array,mask_array in iter(fpl.next_batch, None):
            feed_to_model(img_array, mask_array)
    """
    def __init__(self, result, batch_size):
        """
        :param result: The set of image and bool masks from previous pipeline.
        :param batch_size: The size of the batch for each iteration to train the data.
        """
        self.total_size = len(result)
        if batch_size <= 0 or batch_size >= self.total_size:
            raise WrongBatchSize
        self.batch_size = batch_size
        self.result = result
        self.count = 0

    def new_epoch(self):
        """
        Reset the training to a new epoch and reshuffle the data.
        """
        random.shuffle(self.result)
        self.count = 0

    def next_batch(self):
        """
        Returns 2 arrays of images and boolean masks according to batch size.
        """
        images = []
        boolean_masks = []
        while len(images) != self.batch_size:
            if self.count >= self.total_size:
                return None
            dicom_img, icontour_boolean_mask = self.result[self.count][0], self.result[self.count][1]
            self.count = self.count + 1
            if dicom_img is None:
                continue
            images.append(dicom_img)
            boolean_masks.append(icontour_boolean_mask)
        return images, boolean_masks            
