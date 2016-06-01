import os
from os.path import join as joinp
from nose.tools import eq_, ok_, assert_almost_equal

from bluepyopt.ephys import efeatures
from bluepyopt.ephys.responses import TimeVoltageResponse


def test_EFeature():
    efeature = efeatures.EFeature('name')
    eq_(efeature.name, 'name')


def test_eFELFeature():
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature',
                                     efel_feature_name='voltage_base',
                                     recording_names=recording_names,
                                     stim_start=700,
                                     stim_end=2700,
                                     exp_mean=1,
                                     exp_std=1)

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(os.path.dirname(os.path.abspath(__file__)), 'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response,
                 }

    ret = efeature.calculate_feature(responses, raise_warnings=True)
    assert_almost_equal(ret, -72.069487699766668)

    score = efeature.calculate_score(responses)
    assert_almost_equal(score, 73.05758438592171)

    eq_(efeature.name, 'test_eFELFeature')
    ok_('voltage_base' in str(efeature))
