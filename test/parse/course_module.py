import json
import pickle

from include.logger import *
from docx2python import docx2python
from include.utils import exist, create_directory


def replace_de_char(st):
    # see https://unicode-table.com/en/alphabets/german/
    st = st.replace("\u201e", "")
    st = st.replace("\u201c", "")
    st = st.replace("\u00C4", "Ä")
    st = st.replace("\u00e4", "ä")
    st = st.replace("\u00D6", "Ö")
    st = st.replace("\u00F6", "ö")
    st = st.replace("\u00DC", "Ü")
    st = st.replace("\u00FC", "ü")
    st = st.replace("\u1E0E", "ẞ")
    st = st.replace("\u00DF", "ß")
    return st


def remove_chars(st):
    char_rmv = ["--", "\t", "     ", "      "]
    for char in char_rmv:
        st = st.replace(char, " ")

    st = replace_de_char(st)
    return st


def get_file_list(path):
    files_arr = os.listdir(path)
    return files_arr


def use_pypdfocr(file_loc):
    return


def process_dir(dir_in, dir_out):
    return


def process_file(filein):
    return


def pickle2df(f):
    # read the pickle file
    pickle_file = open(f, 'rb')
    # unpickle the dataframe
    df = pickle.load(pickle_file)
    # close file
    pickle_file.close()

    return df


def course2df(f):
    """
    Takes a docx course module in english and part the contents to a pandas dataframe. Resulting df has minimum
    text cleaning, thus it can be considered to be raw and needs further processing

    :param f: docx course module en english
    :return: pandas dataframe, df[0] = module name;
                               df[1] = qualifications targets (description only);
                               df[2] = module contents.
    """

    doc_result = docx2python(f)
    list_mod_name = []
    list_qualifications = []
    list_mod_content = []
    logging.debug("parsing course modules to dataframe")
    for i in doc_result.body:
        for j in i:
            # print(str(j[1:-1])) # @note this prints only the embedded table with contents/topics
            str_cur = str(j[0:1])
            module_title = ''
            if "Module Name" in str_cur:
                for x in j:
                    mod = " ".join(x).strip()
                    mod = remove_chars(mod)
                    if "Module Name" in mod:
                        module_name = mod
                    else:
                        module_title = mod
                list_mod_name.append(module_title)

            qualification_content = ''
            if "Qualification Targets" in str_cur:
                for x in j:
                    qua_target = " ".join(x).strip()
                    qua_target = remove_chars(qua_target)
                    if "Qualification Targets" in qua_target:
                        qualification_target = qua_target
                    else:
                        qualification_content = qua_target
                list_qualifications.append(qualification_content)

            module_contents = ''
            if "Module Contents" in str_cur:
                for x in j:
                    m_contents = " ".join(x).strip()
                    m_contents = remove_chars(m_contents)
                    if "Module Contents" in m_contents:
                        module_contents_name = m_contents
                    else:
                        module_contents = m_contents
                list_mod_content.append(module_contents)

    # for x in range(len(list_mod_content)):
    #    print(list_mod_content[x],)
    #    print('-------------------------')
    logging.debug("saving module titles")
    df = pd.DataFrame(list_mod_name)
    logging.debug("saving qualification contents")
    df[1] = list_qualifications
    logging.debug("saving module contents")
    df[2] = list_mod_content

    return df


def course2df_de(f):
    """
    Takes a docx course module in english and part the contents to a pandas dataframe. Resulting df has minimum
    text cleaning, thus it can be considered to be raw and needs further processing

    :param f: docx course module en english
    :return: pandas dataframe, df[0] = module name;
                               df[1] = qualifications targets (description only);
                               df[2] = module contents.
    """

    doc_result = docx2python(f)
    list_mod_name = []
    list_qualifications = []
    list_mod_content = []
    logging.debug("parsing course modules to dataframe")
    for i in doc_result.body:
        for j in i:
            # print(str(j[1:-1])) # @note this prints only the embedded table with contents/topics
            str_cur = str(j[0:1])
            module_title = ''
            if "Modulname" in str_cur:
                for x in j:
                    mod = " ".join(x).strip()
                    mod = remove_chars(mod)
                    if "Modulname" in mod:
                        module_name = mod
                    else:
                        module_title = mod
                list_mod_name.append(module_title)

            qualification_content = ''
            if "Qualifikationsziele" in str_cur:
                for x in j:
                    qua_target = " ".join(x).strip()
                    qua_target = remove_chars(qua_target)
                    if "Qualifikationsziele" in qua_target:
                        qualification_target = qua_target
                    else:
                        qualification_content = qua_target
                list_qualifications.append(qualification_content)

            module_contents = ''
            if "Modulinhalte" in str_cur:
                for x in j:
                    m_contents = " ".join(x).strip()
                    m_contents = remove_chars(m_contents)
                    if "Modulinhalte" in m_contents:
                        module_contents_name = m_contents
                    else:
                        module_contents = m_contents
                list_mod_content.append(module_contents)

    # for x in range(len(list_mod_content)):
    #    print(list_mod_content[x],)
    #    print('-------------------------')
    logging.debug("saving module titles")
    df = pd.DataFrame(list_mod_name)
    logging.debug("saving qualification contents")
    df[1] = list_qualifications
    logging.debug("saving module contents")
    df[2] = list_mod_content

    return df


def df2json(df, f_out):
    if not exist(f_out):
        create_directory(os.path.dirname(f_out))

    with open(f_out, 'w') as f:
        json_object = json.loads(df.to_json(orient='index'))
        json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False)
        f.write(json_formatted_str)

    # print(df_course.iloc[0, 2])  # this slice the df.iloc[row,col] => df.iloc[0, 2] is the first row, third item.


def json2dict(json_f):
    """
    Converts a json file to a dictionary.
    notice that this works for the course module data structure. Access individual records as follows:
        dt["0"]["0"]
        dt is a dictionary where:
           ["0"]["0"], the first ["0"] corresponds to the "index" which is a numerical value;
                     and the second ["0"] corresponds to the module name
                     if the second field is ["1"] corresponds to the qualification target and so on.
    Usage:
        json_file = "data/tmp/imacs.json"
        dct = json2dict(json_file)
        for k, v in dct.items():
            print(k, v[str(0)])  # print all keys and module names

    :param json_f: json file
    :return: dictionary
    """
    with open(json_f, encoding='windows-1252') as jf:
        dt = json.load(jf)

    return dt
