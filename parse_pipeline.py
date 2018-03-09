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
                patient_data.append((str.strip(row['patient_id']), str.strip(row['original_id'])))
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
                    yield (dicom_file, icontour_file)

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

pl1 = ParsePipeline('./final_data')

results = []

def collect_results(lst):
    print lst
    results.extend(lst)

def pipeline_wrapper():
    return list(pl1.pair_dicom_contour_file())

if __name__ == '__main__':
    gen = pl1.pair_dicom_contour_file()
    print list(gen)
    for i in gen:
        results.append(i)
