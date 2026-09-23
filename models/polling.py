import pandas as pd


def load_polls(file_path):
    polls = pd.read_csv(file_path)
    polls["date"] = pd.to_datetime(polls["date"])
    return polls


def calculate_average(polls, parties):
    averages = {}

    for party in parties:
        averages[party] = polls[party].mean()

    return averages