from crdatamgt.helpers import data_extraction, workbook_load_path, rename_dictionary, log_format
import pandas as pd
import os
from toolz import interleave
import simplelogging
from pandas.errors import MergeError

formulation_log = simplelogging.get_logger(file_name='formulation.log', console=False, file_format=log_format('simple'))


def _load_formulas(path, write=False):
    wb = workbook_load_path(path, write)
    return wb


def formulation_read(wb, header=False):
    p_header, p_formulation = data_extraction(wb, 'Formulations', header)
    p_formulation.columns = map(str.lower, p_formulation.columns)
    p_formulation.set_index('formulation id', inplace=True)
    p_formulation.rename(columns=rename_dictionary(), inplace=True)
    p_formulation = p_formulation.apply(pd.to_numeric, errors='coerce')

    return [p_formulation, [p_header, p_formulation]][header]


def tests_read(wb, header=False):
    p_header, p_tests_data = data_extraction(wb, 'Tests', header)
    p_tests_data.columns = map(str.lower, p_tests_data.columns)
    p_tests_data.set_index('formulation id', inplace=True)
    return [p_tests_data, [p_header, p_tests_data]][header]


def formulation_load(path):
    wb = _load_formulas(path)
    formulas = formulation_read(wb)
    return formulas


def load_and_update_excel_formulations(new_data, formulation_path):
    """
    This entire bit of code will become difficult to maintain. The entire concept of formulation flexibility should be
    revisited

    :param formulation_path: Excel data to load
    :param new_data: New data from project
    :return: All formulas for all topics multi-dimensional
    """
    if new_data.dropna(how='all').empty:
        return pd.DataFrame()
    new_data = fix_bad_formula_dataframe(new_data, ['test', 'formulation'])

    data_path = os.path.join(formulation_path, 'Formulation table.xlsx')
    writer = pd.ExcelWriter(data_path, engine='openpyxl')
    writer.book = workbook_load_path(formulation_path, True)
    formulation_wb = writer.book

    sheet_formulation = 'Formulations'
    sheet_tests = 'Tests'

    formulation_header, old_formula_data = formulation_read(formulation_wb, True)
    test_header, old_tests = tests_read(formulation_wb, True)

    new_formula_data = new_data.drop_duplicates(subset=new_data.columns.difference(['topic id']))
    new_formula_data = new_formula_data.dropna(how='all', subset=new_formula_data.columns.difference(['formulation']))
    new_formula_data = new_formula_data.set_index('formulation').sort_index()
    new_formula_data = new_formula_data.dropna(how='all')
    new_formula_data = new_formula_data.drop_duplicates()

    try:
        test_set = old_formula_data.merge(new_formula_data, indicator=True, how='outer')
        check = test_set.drop(columns=['test', 'formulation', '_merge', 'topic id'], errors='ignore').sum(
            axis=1).between(100, 100)
        gf = test_set[check]
        new_formulas = gf[gf['_merge'] == 'right_only'].drop(columns=['_merge', 'tests'], errors='ignore')
        new_formulas = new_formulas.drop_duplicates(subset=new_formulas.columns.difference(['test']))
        new_formulas = new_formulas.reset_index().drop(columns='index')
        new_formulas.index += 1
    except MergeError:
        test_set = new_formula_data
        check = test_set.drop(columns=['test', 'formulation', '_merge', 'topic id'], errors='ignore').sum(
            axis=1).between(100, 100)
        gf = test_set[check]
        new_formulas = gf.drop_duplicates()
        new_formulas = new_formulas.drop_duplicates(subset=new_formulas.columns.difference(['test']))
        new_formulas = new_formulas.reset_index()
        new_formulas.loc[:, 'formulation'].fillna(0, inplace=True)
        q = new_formulas.groupby('formulation')
        for a in q.groups[0]:
            new_formulas.loc[a, 'formulation'] = a + 1
        new_formulas.set_index('formulation')

    bf = test_set[~check]
    bf = bf.drop(columns=['formulation', 'test', '_merge'], errors='ignore').dropna(how='all')
    if not bf.empty:
        formulation_log.info(f"Bad Formulas present")

    updated_formulas = old_formula_data.append([new_formulas])
    updated_formulas.reset_index(inplace=True)
    updated_formulas.rename(columns={"index": "formulation id"}, inplace=True)

    generate_test_info(updated_formulas, new_data)

    new_tests = updated_formulas.get(['formulation id', 'test']).fillna('')
    test_groups = new_tests.groupby('test')
    old_tests = old_tests.reset_index()
    for index, test in test_groups:
        if index:
            test = test.replace(index, 'x')
            test = test.rename(columns={'test': index.lower()})
            old_tests = test.merge(old_tests, how='outer', on='formulation id', suffixes=('', '_drop'))
            old_tests = old_tests.drop(columns=f"{index.lower()}_drop", errors='ignore')

        else:
            old_tests = old_tests.merge(test.drop(columns='test'), how='outer')

    old_tests = old_tests.set_index('formulation id').sort_index().reset_index()
    replace_sheet(formulation_wb, sheet_formulation, writer, formulation_header, updated_formulas)
    replace_sheet(formulation_wb, sheet_tests, writer, test_header, old_tests)

    writer.save()
    writer.close()
    return updated_formulas


def fix_bad_formula_dataframe(new_data, frames_to_append):
    new_data.columns = map(str.lower, new_data.columns)
    new_data.rename(columns=rename_dictionary(), inplace=True)
    forced_numeric = pd.DataFrame(new_data.drop(columns=frames_to_append, errors='ignore')).astype(float).fillna(0.0)
    new_data = pd.concat([forced_numeric, new_data.get(frames_to_append)], axis=1)
    return new_data


def form_return(updated_data, old_data):
    if updated_data.dropna(how='all').empty:
        return pd.DataFrame()

    updated_data.columns = map(str.lower, updated_data.columns)
    updated_data.rename(columns=rename_dictionary(), inplace=True)
    data = updated_data.drop(columns=['test', 'units', 'formulation'], errors='ignore')
    data = data.dropna(how='all', subset=data.columns.difference(['topic id']))

    try:
        check_bad_data(data)
    except:
        pass

    if not data.empty:

        data = generate_formula_id(data, old_data.set_index('formulation id').drop(columns='test'))

        data_no_ID = data.drop(columns='formulation id', errors='ignore')
        max_formulation = data_no_ID.groupby(['topic id']).max().rename(
            columns={x: f'{x} Max' for x in data_no_ID.columns})
        min_formulation = data_no_ID.groupby(['topic id']).min().rename(
            columns={x: f'{x} Min' for x in data_no_ID.columns})
        formulation_min_max = pd.concat([max_formulation, min_formulation], axis=1)[
            list(interleave([max_formulation, min_formulation]))]

        topic_frames = data.groupby('topic id')
        for id, topic in topic_frames:
            listID = [d for d in topic.get('formulation id') if d]
            stringID = ', '.join([str(int(y)) for y in listID])
            formulationID = pd.DataFrame({'topic id': id, 'formulation id': [stringID]}).set_index('topic id')
            formulationgroup = formulation_group(topic)
            formulation_min_max.loc[formulationID.index, 'formulation id'] = formulationID
            formulation_min_max.loc[formulationID.index, 'Formulation Group'] = formulationgroup
        formulation_return = formulation_min_max.reset_index().rename(columns={'topic id': 'Topic ID'})
        return formulation_return


def check_bad_data(data):
    topics = data.groupby('topic')
    for k, v in topics.items():
        if not v.drop(columns=['test', 'topic id'], errors='ignore').dropna(how='all').empty:
            if v.drop(columns=['formulation', 'test', 'topic id'], errors='ignore').dropna(how='all').empty:
                formulation_log.info(f"Formulation information is missing in Topic ID:  <<{v.index.values}>>")


def generate_formula_id(data, old_data):
    data = fix_bad_formula_dataframe(data, ['topic id'])
    for index in data.index:
        rr = pd.DataFrame(data.drop(columns=['topic id', 'formulation id'], errors='ignore').loc[index]).transpose()
        zz = old_data.reset_index().merge(rr, how='inner').get('formulation id')
        data.loc[index, 'formulation id'] = zz.values
    return data


def generate_test_info(data, old_data):
    for index in data.index:
        rr = pd.DataFrame(data.drop(columns=['test', 'formulation id'], errors='ignore').loc[index]).transpose()
        zz = old_data.reset_index().merge(rr, how='inner').get('test').dropna().drop_duplicates()
        if not zz.empty:
            data.loc[index, 'test'] = zz.values


def formulation_group(formulas):
    temp_formulation_group = []
    formulas = formulas.set_index('topic id')
    result = formulas.drop(columns=['formulation', 'test', 'units', 'formulation id'], errors='ignore').mean().round(-1)
    fc = pd.DataFrame(result[result > 10]).transpose()
    fc.columns = map(str.lower, fc.columns)
    fc.rename(columns=rename_dictionary(), inplace=True)
    for item in fc:
        temp_formulation_group.append(f"{item} {fc[item].values[0]}")
    fg = ' '.join(temp_formulation_group)
    return pd.DataFrame({'Formulation Group': [fg], 'topic id': list(set(formulas.index))}).set_index('topic id')


def replace_sheet(wb, sheet, writer, header, data):
    idx = wb.sheetnames.index(sheet)
    wb.remove(wb.worksheets[idx])
    header.to_excel(writer, sheet, index=False, header=False)
    data.drop(columns=['test', 'formulation', 'units', 'topic id'], errors='ignore').to_excel(writer, sheet,
                                                                                              startrow=header.shape[0],
                                                                                              startcol=0,
                                                                                              index=False)
