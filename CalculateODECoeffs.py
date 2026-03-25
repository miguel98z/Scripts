import sympy as sp

#Define symbols
u1, u2, u3, u4 = sp.symbols('u1 u2 u3 u4')
a11, a12, a13, a14 = sp.symbols('a11 a12 a13 a14')
a21, a22, a23, a24 = sp.symbols('a21 a22 a23 a24')
a31, a32, a33, a34 = sp.symbols('a31 a32 a33 a34')
a41, a42, a43, a44 = sp.symbols('a41 a42 a43 a44')
b11, b12, b13, b14 = sp.symbols('b11 b12 b13 b14')
b21, b22, b23, b24 = sp.symbols('b21 b22 b23 b24')
b31, b32, b33, b34 = sp.symbols('b31 b32 b33 b34')
b41, b42, b43, b44 = sp.symbols('b41 b42 b43 b44')

s = sp.symbols('s')

def GenCoeffsNum(numMatrix,uVector,matrixName):

    # hacemos el determinante
    det_matrix = numMatrix.det()


    polyList = []
    coeffsNamesListUx = []
    eqStringsListUx = []
    listAll = []
    for u in uVector:
        # Recoger por entradas al sistema u1, u2..
        poly = sp.expand(det_matrix).coeff(u)

        # agrupamos el polinomio en la forma as^3, bs^2.. cs^0
        poly_sorted = poly.as_poly(s)

        #sacamos los coeficientes Nax Nbx Ncx
        polyList.append(poly_sorted.all_coeffs())

    nPolys = list(range(1,len(polyList)+1))
    nCoeffsinOnePoly = list(range(len(polyList[0])))
    nCoeffsinOnePoly.reverse()

    for poly,i in zip(polyList,uVector):
       
        for coef,j in zip(poly,nCoeffsinOnePoly):
            coeffsNamesListUx.append("coef_"+ str(i) +"_s"+str(j))
            eqStringsListUx.append("coef_"+ str(i)+"_s"+ str(j) + " = " + str(coef)+";")
        d = dict(zip(coeffsNamesListUx,eqStringsListUx))
        listAll.append(d)
        coeffsNamesListUx.clear()
        eqStringsListUx.clear()
        

        

    return listAll

def GenCoeffsDen(denMatrix,matrixName):

    det_matrix = denMatrix.det()

    poly_sorted = det_matrix.as_poly(s)


    coeffsList = poly_sorted.all_coeffs()

    nCoeffsinPoly = list(range(len(coeffsList)))
    nCoeffsinPoly.reverse()

    coeffsNamesList = []
    eqStringsList = []
    for coef,j in zip(coeffsList,nCoeffsinPoly):
        coeffsNamesList.append("coef_denA_s"+ str(j))
        eqStringsList.append("coef_denA_s"+ str(j) + " = " + str(coef)+";")
    d = dict(zip(coeffsNamesList,eqStringsList))
    return d




def GenOutputCoeffs(denCalculations,numCalculations,targetVariable):
    denCoeffsNamesList = list(denCalculations.keys())
    leadTerm = denCoeffsNamesList[0]
    denCoeffsNamesListNoLeadTerm = denCoeffsNamesList[1:]
    

    keyList = []
    coeffsList = []
    for poly in numCalculations:
        keyList.extend(list(poly.keys()))     

    # Apply sorted() using the explicit function
    sorted_lst = sorted(keyList, key=sorting_key)

    coeffsNamesList = []
    eqStringsList = []
    for k in sorted_lst:
        sufix = k.split("coef")[1]
        coeffsNamesList.append(targetVariable +"K"+sufix)
        eqStringsList.append(targetVariable +"K"+sufix + " = " +  k + "/" + leadTerm +";")


    for term in denCoeffsNamesListNoLeadTerm:
        sufix = term.split("_")[2]
        coeffsNamesList.append(targetVariable + "K" + "_" + targetVariable +"_" + sufix)
        eqStringsList.append(targetVariable + "K" + "_" + targetVariable +"_" + sufix+ " = " + "-"+ term + "/" + leadTerm +";")

    d = dict(zip(coeffsNamesList,eqStringsList))
    return d

def ExportCoeffs(numCoeffsList,denCoeffsDict,outputCoeffsDict):
    #export numerator coeffs
    for polyDict in numCoeffsList:
        for numCoeff in polyDict.values():
            print(numCoeff+"\n")

    #export denominator coeffs
    for denCoeff in denCoeffsDict.values():
        print(denCoeff+"\n")
    
    #export denominator coeffs
    for outputCoeff in outputCoeffsDict.values():
        print(outputCoeff+"\n")
    pass

# Explicit function to build the sorting key
def sorting_key(string):
    # 1) Split by '_s' to extract the degree at the end
    s_part = string.split('_s')           # ['coef_u1', '2']
    degree_str = s_part[1]                # '2'
    degree = int(degree_str)              # 2

    # 2) Split by '_u' to extract the u index
    u_part = string.split('_u')           # ['coef', '1_s2']
    remaining = u_part[1]                 # '1_s2'
    u_number_str = remaining.split('_')[0]  # '1'
    u_number = int(u_number_str)            # 1

    # 3) Return the sorting tuple:
    #    - degree as negative → descending order
    #    - u_number as is → ascending order
    return (-degree, u_number)







#Define u vector
uVector = [u1, u2, u3, u4]

#Define matrix
numAI1 = sp.Matrix([
    [u1, a12+b12*s, a13+b13*s, a14+b14*s],
    [u2, a22+b22*s, a23+b23*s, a24+b24*s],
    [u3, a32+b32*s, a33+b33*s, a34+b34*s],
    [u4, a42+b42*s, a43+b43*s, a44+b44*s]
])

#Define matrix
numAI2 = sp.Matrix([
    [a11+b11*s, u1, a13+b13*s, a14+b14*s],
    [a21+b21*s, u2, a23+b23*s, a24+b24*s],
    [a31+b31*s, u3, a33+b33*s, a34+b34*s],
    [a41+b41*s, u4, a43+b43*s, a44+b44*s]
])
#Define matrix
numAI3 = sp.Matrix([
    [a11+b11*s, a12+b12*s, u1, a14+b14*s],
    [a21+b21*s, a22+b22*s, u2, a24+b24*s],
    [a31+b31*s, a32+b32*s, u3, a34+b34*s],
    [a41+b41*s, a42+b42*s, u4, a44+b44*s]
])
#Define matrix
numAI4 = sp.Matrix([
    [a11+b11*s, a12+b12*s, a13+b13*s, u1],
    [a21+b21*s, a22+b22*s, a23+b23*s, u2],
    [a31+b31*s, a32+b32*s, a33+b33*s, u3],
    [a41+b41*s, a42+b42*s, a43+b43*s, u4]
])

denA = sp.Matrix([
    [a11+b11*s, a12+b12*s, a13+b13*s, a14+b14*s],
    [a21+b21*s, a22+b22*s, a23+b23*s, a24+b24*s],
    [a31+b31*s, a32+b32*s, a33+b33*s, a34+b34*s],
    [a41+b41*s, a42+b42*s, a43+b43*s, a44+b44*s]
])

denCalculations = GenCoeffsDen(denA,"denominator")

numI4Calculations = GenCoeffsNum(numAI4,uVector,"Numerator I4")
outputCoeffs = GenOutputCoeffs(denCalculations,numI4Calculations,"I4")
ExportCoeffs(numI4Calculations,denCalculations,outputCoeffs)

'''

numI1Calculations = GenCoeffsNum(numAI1,uVector,"Numerator I1")
outputCoeffs = GenOutputCoeffs(denCalculations,numI1Calculations,"I1")
ExportCoeffs(numI1Calculations,denCalculations,outputCoeffs)

numI2Calculations = GenCoeffsNum(numAI2,uVector,"Numerator I2")
outputCoeffs = GenOutputCoeffs(denCalculations,numI2Calculations,"I2")
ExportCoeffs(numI2Calculations,denCalculations,outputCoeffs)

numI3Calculations = GenCoeffsNum(numAI3,uVector,"Numerator I3")
outputCoeffs = GenOutputCoeffs(denCalculations,numI3Calculations,"I3")
ExportCoeffs(numI3Calculations,denCalculations,outputCoeffs)

'''



#get degree

'''

KI1_1s =  -coef_denA_s2/coef_denA_s3 ;
Ku1_1s =  coef_u1_s2/coef_denA_s3 ;
Ku2_1s =  coef_u2_s2/coef_denA_s3 ;
Ku3_1s =  coef_u3_s2/coef_denA_s3 ;
KI1_2s =  -coef_denA_s1/coef_denA_s3 ;
Ku1_2s =  coef_u1_s1/coef_denA_s3 ;
Ku2_2s =  coef_u2_s1/coef_denA_s3 ;
Ku3_2s =  coef_u3_s1/coef_denA_s3 ;
KI1_3s =  -coef_denA_s0/coef_denA_s3 ;
Ku1_3s =  coef_u1_s0/coef_denA_s3 ;
Ku2_3s =  coef_u2_s0/coef_denA_s3 ;
Ku3_3s =  coef_u3_s0/coef_denA_s3 ;
'''

