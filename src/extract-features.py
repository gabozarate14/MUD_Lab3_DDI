#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse

from deptree import *


# Function that builds the path elements using the parameters in terms of
# lemma, relations, tags (PoS) and its combinations

def get_path_elem(tree, path, lemma=False, rel=False, tag=False):
    l = []
    for x in path:
        e = []
        if lemma: e.append(tree.get_lemma(x))
        if rel: e.append(tree.get_rel(x))
        if tag: e.append(tree.get_rel(x))
        l.append("_".join(e))
    return l


# Function that builds the path feature using the parameters in terms of lemma, relations, tags
# (PoS) and its combinations

def get_path_feat(tree, tkE1, tkE2, lemma=False, rel=False, tag=False):
    lcs = tree.get_LCS(tkE1, tkE2)
    path1 = get_path_elem(tree, tree.get_up_path(tkE1, lcs), lemma=lemma, rel=rel, tag=tag)
    path1 = "<".join(path1)

    path2 = get_path_elem(tree, tree.get_down_path(lcs, tkE2), lemma=lemma, rel=rel, tag=tag)
    path2 = ">".join(path2)

    e = []
    if lemma: e.append(tree.get_lemma(lcs))
    if rel: e.append(tree.get_rel(lcs))
    if tag: e.append(tree.get_rel(lcs))

    path = path1 + "<" + "_".join(e) + ">" + path2

    return path, path1, path2


# Convert a pair of drugs and their context in a feature vector
# Receives an execution parameter dictionary that specifies the features to use
def extract_features(tree, entities, e1, e2, exec_params):
    feats = set()

    # get head token for each gold entity
    tkE1 = tree.get_fragment_head(entities[e1]['start'], entities[e1]['end'])
    tkE2 = tree.get_fragment_head(entities[e2]['start'], entities[e2]['end'])
    if tkE1 is not None and tkE2 is not None:

        # # features for tokens in before E1
        lemma_pre = ""
        tag_pre = ""
        word_pre = ""
        tk = tkE1 - 1
        while tk >= 0 and (tree.is_stopword(tk)):
            tk -= 1

        if tk >= 0:
            lemma_pre = tree.get_lemma(tk).lower()
            tag_pre = tree.get_tag(tk)
            word_pre = tree.get_word(tk)

        # features for tokens in between E1 and E2
        tk = tkE1 + 1
        try:
            while (tree.is_stopword(tk)):
                tk += 1
        except:
            return set()

        lemma = tree.get_lemma(tk).lower()
        tag = tree.get_tag(tk)
        word = tree.get_word(tk)

        # features for tokens in after E2
        tk = tkE2 + 1
        while tk < tree.get_n_nodes() - 1 and (tree.is_stopword(tk)):
            tk += 1

        lemma_post = ""
        tag_post = ""
        word_post = ""

        if tk < tree.get_n_nodes() - 1:
            lemma_post = tree.get_lemma(tk).lower()
            tag_post = tree.get_tag(tk)
            word_post = tree.get_word(tk)

        if exec_params['lpre']: feats.add("lpre=" + lemma_pre)
        if exec_params['lib']: feats.add("lib=" + lemma)
        if exec_params['lpost']: feats.add("lpost=" + lemma_post)

        if exec_params['lppre']:
            feats.add("lppre=" + (lemma_pre + "_" + tag_pre if lemma_pre and tag_pre else ""))
        if exec_params['lpib']:
            feats.add("lpib=" + (lemma + "_" + tag if lemma and tag else ""))
        if exec_params['lppost']:
            feats.add("lppost=" + (lemma_post + "_" + tag_post if lemma_post and tag_post else ""))

        if exec_params['wpre']: feats.add("wpre=" + word_pre)
        if exec_params['wib']: feats.add("wib=" + word)
        if exec_params['wpost']: feats.add("wpost=" + word_post)

        if exec_params['eib'] or exec_params['eib_lemma']:
            eib = False
            eib_lemma = ""
            for tk in range(tkE1 + 1, tkE2):
                if tree.is_entity(tk, entities):
                    eib = True
                    eib_lemma = tree.get_lemma(tk)
            # feature indicating the presence of an entity in between E1 and E2
            if exec_params['eib']:
                feats.add('eib=' + str(eib))
            # feature indicating the lemma of the entity in between E1 and E2 if it is present
            if exec_params['eib_lemma']:
                feats.add('eib_lemma=' + str(eib_lemma))

        # features about paths in the tree
        # it would depend on the desired parameters to build the path in terms of lemma,
        # relations, tags (PoS) and its combinations
        if exec_params['path']:
            lemma = "L" in exec_params['path']
            rel = "R" in exec_params['path']
            tag = "T" in exec_params['path']
            path, path1, path2 = get_path_feat(tree, tkE1, tkE2, lemma=lemma, rel=rel, tag=tag)

            feats.add("path1=" + path1)
            feats.add("path2=" + path2)
            feats.add("path=" + path)

        # feature that indicates the entities types
        if exec_params['ent_types']:
            ent_types = set()
            ent_types.add(tree.get_tag(tkE1))
            ent_types.add(tree.get_tag(tkE2))
            feats.add("ent_types=" + ','.join(ent_types))

    return feats


## --------- MAIN PROGRAM -----------
## --
## -- Usage:  extract_features targetdir
## --
## -- Extracts feature vectors for DD interaction pairs from all XML files in target-dir
## --

ext_feat_exps = [
    # Path experiment
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "L", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "T", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "LR", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "RT", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "LT", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "LRT", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    # Other features test (including only between)
    {"lib": False, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": False, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": True, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": False, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": False, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": True, "eib": True, "eib_lemma": True, "ent_types": True, "path": None, "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    # Other features test (including previous and posterior)
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": True, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": True, "lppre": False, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": True, "lpost": False, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": True, "wpost": False, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": True, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": False, "lpost": False, "wpost": False, "lppost": True},
    # 1.3 result
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": True, "wpre": False, "lppre": False, "lpost": True, "wpost": False , "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": True, "wpre": False, "lppre": False, "lpost": True, "wpost": True, "lppost": False},
    {"lib": True, "wib": True, "lpib": False, "eib": False, "eib_lemma": True, "ent_types": True, "path": "R", "lpre": False, "wpre": False, "lppre": True, "lpost": True, "wpost": True, "lppost": False}

]

if len(sys.argv) < 3:
    print("One parameter of execution is missing")
    sys.exit(1)

# directory with files to process
datadir = sys.argv[1]

# features to extract defined in the ext_feat_exps
exec_params = ext_feat_exps[int(sys.argv[2])]

# process each file in directory
for f in listdir(datadir):

    # parse XML file, obtaining a DOM tree
    tree = parse(datadir + "/" + f)

    # process each sentence in the file
    sentences = tree.getElementsByTagName("sentence")
    for s in sentences:
        sid = s.attributes["id"].value  # get sentence id
        stext = s.attributes["text"].value  # get sentence text
        # load sentence entities
        entities = {}
        ents = s.getElementsByTagName("entity")
        for e in ents:
            id = e.attributes["id"].value
            offs = e.attributes["charOffset"].value.split("-")
            entities[id] = {'start': int(offs[0]), 'end': int(offs[-1])}

        # there are no entity pairs, skip sentence
        if len(entities) <= 1:
            continue

        # analyze sentence
        analysis = deptree(stext)

        # for each pair in the sentence, decide whether it is DDI and its type
        pairs = s.getElementsByTagName("pair")
        for p in pairs:
            # ground truth
            ddi = p.attributes["ddi"].value
            if (ddi == "true"):
                dditype = p.attributes["type"].value
            else:
                dditype = "null"
            # target entities
            id_e1 = p.attributes["e1"].value
            id_e2 = p.attributes["e2"].value
            # feature extraction

            feats = extract_features(analysis, entities, id_e1, id_e2, exec_params)
            # resulting vector
            if len(feats) != 0:
                print(sid, id_e1, id_e2, dditype, "\t".join(feats), sep="\t")