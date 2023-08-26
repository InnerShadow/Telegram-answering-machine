
#Set marks </start> & </end> to better NN training
def setStertEndMarks(vec, maxWords):
    for i in range(len(vec)):
        vec[i] = "</start> " + vec[i]

        if len(vec[i].split()) > maxWords - 1:
            splits = vec[i].split()
            vec[i] = ""
            for j in range(maxWords - 1):
                vec[i] += splits[j] + " "

        vec[i] = vec[i] + " </end>"

    return vec


def diableStarEndMarks(vec):
    res = ""
    splits = vec[i].split()
    
    for i in range(len(splits)):
        if splits[i] != "</start>":
            res += splits[i]
        if splits[i] == "</end>":
            break

    return res