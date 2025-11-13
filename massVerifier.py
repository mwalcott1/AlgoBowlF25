import verify
# Verify other team's output to our problem

suffixes = [1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079,
            1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097,
            1098, 1099, 1100, 1101, 1102, 1103, 1128]

for suffix in suffixes:
    # I think this is how the files will be names
    fileName = f'externOutputs/output_group{suffix}.txt'

    # test to see if other team's solution is valid
    isValid, score, message = verify.verify_solution(f'Inputs/input_group{suffix}.txt', fileName, verbose=False)
    if not isValid:
        print(f'Invalid output found for suffix {suffix}. with message: {message}')
    else:
        print(f'Suffix {suffix} gives valid output')
