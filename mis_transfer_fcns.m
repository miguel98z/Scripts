%I_L1
num_I_L1 = [C1, 0];

den_I_L1 = [C1*C2*L1*R1, C1*L1, C1*R1 + C2*R1, 1];

%I_V1
num_I_V1 = [-C1*C2*L1, 0, -C1 - C2, 0];

den_I_V1 = [C1*C2*L1*R1, C1*L1, C1*R1 + C2*R1, 1];

%v1
num_v1 = [1];

den_v1 = [1];

%v2
num_v2 = [C1*L1, 0, 1];

den_v2 = [C1*C2*L1*R1, C1*L1, C1*R1 + C2*R1, 1];

%v3
num_v3 = [1];

den_v3 = [C1*C2*L1*R1, C1*L1, C1*R1 + C2*R1, 1];

