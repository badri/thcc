import os
import csv
import glob
import logging

import parsing

class ParsePipeline(object):
    
    def __init__(self, data_dir):
        self._data_dir = data_dir
        self.patient_data = self.get_patient_data(os.path.join(self._data_dir, 'link.csv'))

    def get_patient_data(self, filename):
        patient_data = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #TODO: throw exception if patient_id or original_id directory does not exist?
                patient_data.append((row['patient_id'], row['original_id']))
        return patient_data

    def pair_dicom_contour_file(self):
        for patient_id, original_id in self.patient_data:
            contour_dir = os.path.join(self._data_dir, 'contourfiles', original_id)
            dicom_dir = os.path.join(self._data_dir, 'dicoms', patient_id)
            icontour_glob = os.path.join(contour_dir, 'i-contours/*.txt')
            # Use glob iteratively if there are lots of files
            icontour_paths = glob.iglob(icontour_glob)
            for icontour_file in icontour_paths:
                dicom_file = self.find_dicom_file_for_icontour_file(dicom_dir, icontour_file)
                if dicom_file:
                    yield self.convert_tuple_to_img_boolean_mask(dicom_file, icontour_file)

    def find_dicom_file_for_icontour_file(self, dicom_dir, icontour_file):
        parts = os.path.basename(icontour_file).split('-')
        try:
            dicom_num = parts[2].lstrip('0')
        except IndexError:
            return None
        dicom_file = os.path.join(dicom_dir, dicom_num + '.dcm')
        if os.path.isfile(dicom_file):
            return dicom_file
        #TODO: probably write a debug log saying no dicomfile found for icontour_file
        return None

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
