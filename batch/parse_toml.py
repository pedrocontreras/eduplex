import toml


def get_models(config_toml):
    with open(config_toml, 'r') as f:
        config = toml.load(f)
    bi_list = config['sbert']['sbert']
    return bi_list


def get_crossencoder(config_toml):
    with open(config_toml, 'r') as f:
        config = toml.load(f)
    cross_list = config['cross-encoder']['cross-encoder']
    return cross_list


def get_models_shortname(model_l):
    l = []
    for s in model_l:
        if s.find('/') != -1:
            l.append(s.partition("/")[2])
        else:
            l.append(s)
    return l


if __name__ == "__main__":
    models_list = get_models('models.toml')
    print(models_list)
    for i in get_models_shortname(models_list):
        print(i)
