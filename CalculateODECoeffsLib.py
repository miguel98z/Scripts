import sympy as sp

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







