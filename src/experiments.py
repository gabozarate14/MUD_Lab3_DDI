# Defining the parameters of fature extraction experiments

EXPERIMENTS = [
    # Path experiment
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","L"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","R"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","RT"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","LT"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","LRT"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    # Other features test (including only between)
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": False, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": False, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": False, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": False, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": None, "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    # Other features test (including previous and posterior)
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": True, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": True, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": True, "lpost": False, "wpost": False, "lppost": False},
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": True, "wpost": False, "lppost": False},
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": True, "lppost": False},
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": True},
    # 1.3 result
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": False, "lppre": True, "lpost": False, "wpost": False, "lppost": True},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": False, "wpre": True, "lppre": False, "lpost": False, "wpost": True, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": ["LR","T"], "lpre": True, "wpre": False, "lppre": False, "lpost": True, "wpost": False, "lppost": False}

]