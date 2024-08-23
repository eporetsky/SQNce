import os
import glob
import pandas as pd


meta = pd.read_csv("rnaseq_samples_meta.tsv", sep="\t", encoding="ISO-8859-1")
meta  = meta.groupby("experiment_acc").count()[["sample_acc"]]
meta = meta.to_dict()["sample_acc"]

genotypes = ["AtCol-0",
             "Bd21",
             "TaCS",
             "ZmB73",
             "MdGDDH13",
             "VvPN40024",]

for geno in genotypes:
    for fl in glob.glob(os.path.join(geno, "counts", "*.counts.tsv")):
        acc_name = os.path.basename(fl).replace(".counts.tsv", "")
        counts = pd.read_csv(fl, sep="\t")
        n_samples = len(counts.columns) - 1 # ignore index col

        if acc_name in meta.keys():
            if n_samples == meta[acc_name]:
                #print(f"{geno} {acc_name}: PASS ({n_samples})")
                continue
            else:
                print("{} {}: MISMATCH ({}!={})".format(geno, acc_name, meta[acc_name], n_samples))
                #print(f"{geno} {acc_name}: MISMATCH ({meta[acc_name]}!={n_samples})")
        else:
            print("{} {}: MISSING ({})".format(geno, acc_name, n_samples))
            #print(f"{geno} {acc_name}: MISSING ({n_samples})")
