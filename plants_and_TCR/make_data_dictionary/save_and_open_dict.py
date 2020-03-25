import pickle

from plants_and_TCR.analysis_parameters import directory_information
PATH_OUTPUT = directory_information.DIR_DATA_DICTIONARIES

def save_dict(dict_to_save, dict_name, output_path=PATH_OUTPUT):
    with open(output_path+dict_name+'.pickle', 'wb') as handle:
        pickle.dump(dict_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def open_dict(path, dict_name):
    dict_opened = pickle.load(open(path+dict_name+'.pickle', 'rb'))
    return dict_opened