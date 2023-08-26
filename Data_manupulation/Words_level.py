

#Set marks </start> & </end> to better NN training
def setStertEndMarks(vec):
    for i in range(len(vec)):
        vec[i] = " </start> " + vec[i]

        vec[i] = vec[i] + " </end> "

    return vec