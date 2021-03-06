import json
from dataclasses import dataclass
from sacred import Experiment
from sacred.observers import MongoObserver, SlackObserver
import os

def setup_experiment(experiment_name):
    mongo_uri = 'mongodb://mongo_user:mongo_password@localhost:27017/sacred?authSource=admin'
    ex = Experiment(experiment_name, save_git_info=False)
    ex.observers.append(MongoObserver(url=mongo_uri,
                                          db_name='sacred'))
    slack_obs = SlackObserver.from_config(os.environ['SLACK_CONFIG'])
    ex.observers.append(slack_obs)
    return ex

def load_file(filename):
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            data.append(json.loads(line.strip()))
    return data

def to_list(tensor):
    return tensor.detach().cpu().tolist()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

