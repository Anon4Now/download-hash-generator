import os

import pytest

from resources import vt_check, utils


@pytest.mark.skipif(not utils.get_envs(), reason="if the user doesn't have the .env file created this will fail")
def test_retrieve_virus_total_results():
    notepad_plus_plus_hash = '71c8beb31074c53a59927f1874f0cce19bed8fd3be9edd93164511eb717c581c'
    response_200 = vt_check.retrieve_virus_total_results(
        sha256_hash=notepad_plus_plus_hash,
        api_endpoint=os.getenv('API_ENDPOINT'),
        api_key=os.getenv('API_key'),
        api_key_val=os.getenv('API_KEY_VAL')
    )
    assert response_200[1] == 200

    fake_hash = '71c8beb31074c53a59927f1874f0cce19bed8fd3be9edd93164511eb71111111'
    response_404 = vt_check.retrieve_virus_total_results(
        sha256_hash=fake_hash,
        api_endpoint=os.getenv('API_ENDPOINT'),
        api_key=os.getenv('API_key'),
        api_key_val=os.getenv('API_KEY_VAL')
    )
    assert response_404[1] == 404

