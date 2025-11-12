import shutil
import sys
import verify

# choose the best found solution from the 8 solvers
suffixes = [1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079,
            1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097,
            1098, 1099, 1100, 1101, 1102, 1103, 1128]

# for each input
for suffix in suffixes:
    bestFoundNum = 0
    bestFoundIdx = -1
    # iterate over all outputs to find best solution
    for i in range(8):
        fileName = "Outputs" + str(i+1) + "/" + str(suffix) + ".txt"

        # find score from solver i+1
        with open(fileName, 'r') as file:
            currentScore = int(file.readline().strip())

        # if it's good, then we select it
        if currentScore > bestFoundNum:
            bestFoundNum = currentScore
            bestFoundIdx = i

    # test to make sure this solution is valid
    bestSolFile = "Outputs" + str(bestFoundIdx+1) + "/" + str(suffix) + ".txt"
    isValid, score, message = verify.verify_solution(f'Inputs/input_group{suffix}.txt', bestSolFile, verbose=False)
    if not isValid:
        print(f'Invalid output found for suffix {suffix} and best output {bestSolFile}.')
        sys.exit(1)

    # print what best solution was, and also copy file to a different directory for easy upload access
    print(f'Best solution for suffix: {suffix} is from solver {bestFoundIdx+1}/8 with score {bestFoundNum}')
    shutil.copy(bestSolFile, "bestOutputs")
