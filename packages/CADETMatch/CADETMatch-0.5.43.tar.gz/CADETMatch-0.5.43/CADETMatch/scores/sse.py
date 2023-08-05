import CADETMatch.util as util
import sys
from addict import Dict
import numpy

name = "SSE"

def get_settings(feature):
    settings = Dict()
    settings.adaptive = False
    settings.badScore = -sys.float_info.max
    settings.meta_mask = True
    settings.count = 1
    return settings

def run(sim_data, feature):
    "sum square error score, this score is NOT composable with other scores, use negative so score is maximized like other scores"
    sim_time_values, sim_data_values = util.get_times_values(sim_data['simulation'], feature)
    selected = feature['selected']

    exp_time_values = feature['time'][selected]
    exp_data_values = feature['value'][selected]

    sse = util.sse(sim_data_values, exp_data_values)

    return ([-sse,], sse, len(sim_data_values), sim_time_values, sim_data_values, exp_data_values, [sse,])

def setup(sim, feature, selectedTimes, selectedValues, CV_time, abstol, cache):
    temp = {}
    temp['peak_max'] = max(selectedValues)
    return temp

def headers(experimentName, feature):
    name = "%s_%s" % (experimentName, feature['name'])
    temp = ["%s_SSE" % name]
    return temp
