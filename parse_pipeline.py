from os import path
import csv
import glob
import logging

import parsing

class ParsePipeline(object):
    
    def __init__(self, data_dir):
        self._data_dir = data_dir
        self.patient_data = self.get_patient_data(path.join(self._data_dir, 'link.csv'))

    def get_patient_data(self, filename):
        patient_data = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                patient_data.append((row['patient_id'], row['original_id']))
        return patient_data

    def pair_dicom_contour_file(self):
        for patient_id, original_id in self.patient_data:
            icontour_glob = path.join(self._data_dir, 'contourfiles', original_id, 'i-contours/*.txt')
            # Use glob iteratively if there are lots of files
            icontour_paths = glob.iglob(icontour_glob)
            for icontour_file in icontour_paths:
                parts = path.basename(icontour_file).split('-')
                dicom_num = parts[2].lstrip('0')
                dicom_file = path.join(self._data_dir, 'dicoms', patient_id, dicom_num + '.dcm')
                if path.isfile(dicom_file):
                    yield (dicom_file, icontour_file)

    def convert_tuple_to_img_boolean_mask(self, dicom_file, icontour_file):
        dcm_dict = parsing.parse_dicom_file(dicom_file)
        if dcm_dict is None:
            logging.warning('Dicom file invalid: ' + dicom_file)
            return None, None, None
        dicom_img = dcm_dict['pixel_data']

        coords_lst = parsing.parse_contour_file(cipath)
        if len(coords_lst) == 0:
            logging.warning('Inner contour file empty: ' + cipath)
            return None, None, None
        icontour_boolean_mask = parsing.poly_to_mask(coords_lst, dicom_img.shape[0], dicom_img.shape[1])
        return (dicom_img, icontour_boolean_mask)
        
