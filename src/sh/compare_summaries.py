#!/usr/bin/env python

# Compare two summary csv files

import sys

def csvread(filename):
    f = open(filename)

    header = None
    rows = []
    for l in f:
        l = l.replace("\n", "")
        if not header:
            header = l.split(",")
        else:
            rows.append(l.split(","))

    data = {}
    labels = set()
    for r in rows:
        label = r[0]
        if "hap.py" in label:
            # ignore version line
            continue
        if label in labels:
            continue
        labels.add(label)
        for i in xrange(1, len(r)):
            if header[i] not in data:
                data[header[i]] = {}
            try:
                data[header[i]][label] = float(r[i])
            except:
                data[header[i]][label] = r[i]
    f.close()
    return data


def main():
    data1 = csvread(sys.argv[1])
    data2 = csvread(sys.argv[2])

    different_metrics = []

    for metric in ["TRUTH.TOTAL", "QUERY.TOTAL",
                   "TRUTH.TOTAL.TiTv_ratio", "QUERY.TOTAL.TiTv_ratio",
                   "TRUTH.TOTAL.het_hom_ratio", "QUERY.TOTAL.het_hom_ratio",
                   "METRIC.Recall", "METRIC.Precision", "METRIC.Frac_NA"]:
        for field in ["Locations.SNP",
                      "Locations.INDEL"
                      ]:
            field1 = field
            if field1 not in data1[metric]:
                field1 = field1.replace("Locations.", "")
            field2 = field
            if field2 not in data2[metric]:
                field2 = field2.replace("Locations.", "")
            print metric + " / " + field
            print data1[metric][field1]
            print data2[metric][field2]
            if metric.endswith("_ratio") and data1[metric][field1] == "" and data2[metric][field2] == "":
                # allow empty ratio match
                continue
            if ("%.3g" % data1[metric][field1]) != ("%.3g" % data2[metric][field2]):
                different_metrics.append((field,
                                          metric,
                                          ("%.3g" % data1[metric][field1]),
                                          ("%.3g" % data2[metric][field2]),
                                          data2[metric][field2] - data1[metric][field1]))

    if different_metrics:
        print >> sys.stderr, "ERROR -- Metric differences detected:"
        print >> sys.stderr, "-------------------------------------\n"
        for m in different_metrics:
            print >> sys.stderr, "%s / %s: %s != %s difference: %f" % m
        print >> sys.stderr, "-------------------------------------"
        sys.exit(1)


if __name__ == '__main__':
    main()
