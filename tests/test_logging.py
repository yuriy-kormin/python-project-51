import os
import tempfile
# import logging
# from re import search
from pageloader import download


LOGNAME = 'log'


def test_log_isset(test_url, simple_html_content, requests_mock):
    requests_mock.get(test_url, text=simple_html_content)
    with tempfile.TemporaryDirectory() as tmpdir:
        download(test_url, tmpdir)
        log_path = os.path.join(tmpdir, LOGNAME)
        # print (os.listdir(tmpdir))
        assert os.path.isfile(log_path)

#
# def test_log_content(test_url, simple_html_content, test_filename,
#                      requests_mock):
#     requests_mock.get(test_url, text=simple_html_content)
#     with tempfile.TemporaryDirectory() as tmpdir:
#         download(test_url, tmpdir)
#         log_path = os.path.join(tmpdir, LOGNAME)
#         log_content = read_file(log_path)
#         assert search(fr'{test_url}\n', log_content)
#         assert search(fr'{tmpdir}\n', log_content)
#         assert search(fr'{test_filename}\n', log_content)
# #
#
# def test_caplog(caplog, test_url):
#     with tempfile.TemporaryDirectory() as tmpdir,
#     caplog.at_level(logging.DEBUG):
#         download(test_url, tmpdir)
#         print('its caplog', caplog.record_tuples)
#         assert False
#         for record in caplog.records:
#             assert record == '1cca1'
