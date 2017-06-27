import json
from collections import defaultdict
import pickle
import pandas as pd

def rec_dd():
    return defaultdict(rec_dd)

def build_hitting_headings_from_json(file, stat_type):
    d = rec_dd()

    with open(file) as f:
        json_str = f.read()

        for i, v in enumerate(json.loads(json_str)):
            return v[stat_type]

def build_hitting_dict_from_json(file):
    d = rec_dd()

    with open(file) as f:
        json_str = f.read()

        for i, v in enumerate(json.loads(json_str)):
            player_id = v['player_id']
            name = v['name']
            birthdate = v['birthdate']
            d[(player_id, name, birthdate)] = {'base_stats': v['base_stats'],
                                               'adv_hitting_stats': v['adv_hitting_stats'],
                                               'plate_disc_stats': v['plate_disc_stats'],
                                               'fielding_stats': v['fielding_stats'],
                                               'adv_fielding_stats': v['adv_fielding_stats'],
                                               'scouting_stats': v['scouting_stats'],
                                               'value_stats': v['value_stats'],
                                               'win_prob_stats': v['win_prob_stats'],
                                               'bb_stats': v['bb_stats']}

    return d


data = build_hitting_dict_from_json('../player_hitting_stats.json')
df = pd.DataFrame.from_dict(data, orient='index')

df.index.name = ['ID', 'Name', 'Birthdate']


def fix_stats_df(df, stat_type):
    """ Builds and cleans a dataframe for given stat_type.
    :param df: 
    :param stat_type: 
    :return: dataframe
    """
    columns = build_hitting_headings_from_json('../test_headings2.json', stat_type)
    row_length = len(columns)

    # drop rows with no stats for given type
    for i, row in pd.DataFrame(df[stat_type]).iterrows():
        if len(row[0]) < 1:
            df = df.drop(i[0], level=0, axis=0)

    # drop rows of pitchers
    for i, row in df.iterrows():
        if len(df[stat_type][i][0]) != row_length:
            df = df.drop(i[0], level=0, axis=0)
        else:
            if df[stat_type][i][0][0] == '':
                print('none')

    def clean(x):
        """Cleans up case where players player for multiple teams
        in a single season by deleting inserted blank column.
        """
        for i in x.iloc[0]:
            for j in i:
                if j == '\xa0\xa0\xa0\xa0':
                    del i[i.index(j)]
        return pd.DataFrame(x.iloc[0], columns=columns)

    clean = df.groupby(level=[1])[stat_type].apply(clean)

    fix = clean.reset_index(level=1, drop=True)

    return fix

def multiindex_cols(df, stat_type):
    """Sets muliindex on index and columns. Indexes by Player, Season, and Team.
    Adds stat_type level to column names.
    :param df: 
    :param stat_type: 
    :return dataframe: 
    """
    df.index.name = 'Player'
    df = df.reset_index().set_index(['Player', 'Season', 'Team'])
    n = len(df.columns)
    x = [stat_type] * n
    z = list(zip(x, df.columns))
    #print(z)
    cols = pd.MultiIndex.from_tuples(z)
    # # pd.DataFrame(df_dict['base_stats'], columns=cols)
    df.columns = cols
    return df

def make_suffix_cols(df, stat_type):
    """Sets muliindex on index and columns. Indexes by Player, Season, and Team.
    Adds stat_type level to column names.
    :param df: 
    :param stat_type: 
    :return dataframe: 
    """
    df.index.name = 'Player'
    df = df.reset_index().set_index(['Player', 'Season', 'Team'])
    n = len(df.columns)
    x = [stat_type] * n
    z = list(zip(x, df.columns))
    #print(z)
    #cols = pd.MultiIndex.from_tuples(z)
    # # pd.DataFrame(df_dict['base_stats'], columns=cols)
    df.columns = z
    return df

# def make_subset_df(df, stat_type):
#     df1 = df[stat_type].apply(pd.Series)
#     n = len(list(df1.values[0]))
#     c = [stat_type] * n
#     cols = list(zip(c, list(range(n))))
#     columns = pd.MultiIndex.from_tuples(cols)
#     df1.columns = columns
#     return df1

print(make_suffix_cols(fix_stats_df(df, 'base_stats'), 'base_stats'))

def pickle_df(stat_type):
    """
    Builds a pickled file containing a dataframe for a stat type of your choice
    :param stat_type: name of stat field
    :return: 
    """
    filename = 'hitting_' + stat_type + '3.pkl'
    with open(filename, 'wb') as picklefile:
        hdf = make_suffix_cols(fix_stats_df(df, stat_type), stat_type)
        pickle.dump(hdf, picklefile)


stat_types = (['base_stats', 'adv_hitting_stats', 'plate_disc_stats', 'fielding_stats',
               'adv_fielding_stats', 'scouting_stats', 'value_stats', 'win_prob_stats', 'bb_stats'])

for stat_type in stat_types:
    pickle_df(stat_type)

