import os
import tempfile
from pageloader import download
from pageloader.download import render_name
from PIL import Image

#
# def test_corrected_downloading(test_url, test_filename):
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         download(test_url, tmpdirname)
#         subdir_name = render_name(test_url, 'subdir')
#         subdir_path = os.path.join(tmpdirname, subdir_name)
#         flag = True
#         for file in os.listdir(subdir_path):
#             try:
#                 file_path = os.path.join(subdir_path,file)
#                 image = Image.open(file_path).verify()
#             except:
#                 flag = False
#         assert flag == True


