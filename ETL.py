import pandas as pd
import json
from io import StringIO
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()


data_str = None
videos_df = None
df = None

def extract():
    global data_str
    with open('videos.json', 'r') as file:
        data_str = json.loads(file.read())
    data_str = json.dumps(data_str['videos'])


def transform():
    global data_str, videos_df, df
    videos_dfs = []
    df = pd.read_json(StringIO(data_str))
    index_to_id = {}
    for i in df.index:
        index_to_id[df.loc[i]['id']] = i

    def make_df(json_obj):
        data_video_str = json.dumps(json_obj)
        df_video = pd.read_json(StringIO(data_video_str))
        df_video = df_video.drop(columns=['id'])
        df_video['video_id'] = df_video['video_id'].apply(lambda x: index_to_id[x])
        videos_dfs.append(df_video)

    df['snapshots'].apply(make_df)
    videos_df = pd.concat(videos_dfs, ignore_index=True)
    df = df.drop(columns=['id', 'snapshots'])


def load():
    PG_PATH = os.getenv('PG_PATH')
    PG_PATH = PG_PATH[:11] + 'psycopg2' + PG_PATH[18:]
    engine = create_engine(PG_PATH, echo=True)
    df.to_sql('videos', engine, if_exists='append')
    videos_df.to_sql('snapshots', engine, if_exists='append')


def main():
    extract()
    transform()
    load()


if __name__ == '__main__':
    main()