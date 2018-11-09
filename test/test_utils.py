import os
import shutil
import yaml
from vm_support.utils import create_config_file, _set_earth_data_authentication_to_file

BARRAX_POLYGON = "POLYGON((-2.20397502663252 39.09868106889479,-1.9142106223355313 39.09868106889479," \
                 "-1.9142106223355313 38.94504502508093,-2.20397502663252 38.94504502508093," \
                 "-2.20397502663252 39.09868106889479))"
TEST_DIR = './test/test_data/'
DATA_STORES_FILE = 'dummy_data_stores'
DATA_STORES_FILE_EXTENSION = '.yaml'


def test_create_config_file():
    config_file = '{}/config.yaml'.format(TEST_DIR)
    try:
        priors_dir = '{}/priors'.format(TEST_DIR)
        create_config_file(TEST_DIR, BARRAX_POLYGON, '2017-06-01', '2017-06-30', '10', priors_dir)
        assert os.path.exists(config_file)
    finally:
        if os.path.exists(config_file):
            os.remove(config_file)


def test_set_earth_data_authentication():
    data_stores_file = '{}/{}{}'.format(TEST_DIR, DATA_STORES_FILE, DATA_STORES_FILE_EXTENSION)
    data_stores_file_2 = '{}/{}2{}'.format(TEST_DIR, DATA_STORES_FILE, DATA_STORES_FILE_EXTENSION)
    shutil.copyfile(data_stores_file, data_stores_file_2)
    try:
        _set_earth_data_authentication_to_file('fecvghf', 'tvhbg', data_stores_file_2)
        stream = open(data_stores_file_2, 'r')
        data_store_lists = yaml.safe_load(stream)
        for data_store_entry in data_store_lists:
            if data_store_entry['DataStore']['Id'] == 'modis_mcd43a1':
                assert data_store_entry['DataStore']['FileSystem']['parameters']['username'] == 'fecvghf'
                assert data_store_entry['DataStore']['FileSystem']['parameters']['password'] == 'tvhbg'
        stream.close()
    finally:
        os.remove(data_stores_file_2)
