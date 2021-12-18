import json


def get_output_filename():
    fname = "data/promos.json"
    return fname


def load_promos(fname=None):
    if fname is None:
        fname = get_output_filename()

    with open(fname, "r", encoding="utf8") as f:
        data = json.load(f)

    return data


def save_promos(data, fname=None):
    if fname is None:
        fname = get_output_filename()

    with open(fname, "w", encoding="utf8") as f:
        json.dump(data, f)

    return


if __name__ == "__main__":
    fname = get_output_filename()
    print(fname)
