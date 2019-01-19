#!/usr/bin/python

#------------------------------------------------------------------------------#
#                                                                              #
#                                                                              #
#                                  SMRT grader                                 #
#               Simple Method for Rating and grading Test results              #
#                                (Antonio Ricco)                               #
#                                                                              #
#------------------------------------------------------------------------------#

#    SMRT 
#    Copyright (C) 2019  Antonio Ricco
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.00
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import fileinput

# to add command line options
import argparse

#from Lib import statistics
import numpy
import math

# erfinv: inverse erf function
from scipy.special import erfinv
#print(sys.version_info)


# trasposition of matrices
# https://stackoverflow.com/questions/4937491/matrix-transpose-in-python#9622534
def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)


# it opens a .csv file with tab as separator and converts it in a matrix list
def csvFileToMatrix(csvFileName, csvFilePath):
    outputMatrix = []

    for line in fileinput.input( csvFilePath + "/" + csvFileName ):
        outputMatrixLine = []
        for k in range(0,line.count("\t")+1):
            outputMatrixLine.append(line.split("\t")[k].rstrip())  # rstrip() removes \n, \r, etc.
        outputMatrix.append(outputMatrixLine)

    return outputMatrix



# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \n
# and rows separated by \n
def matrixToCsvFile(inputMatrix, csvFileName, csvFilePath):
    outputCsvFile = open( csvFilePath + "/" + csvFileName, 'w' )

    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            outputCsvFile.write ( inputMatrix[j][k] + "\t" )
        outputCsvFile.write ( inputMatrix[j][len(inputMatrix[j])-1] + "\n" )

    outputCsvFile.close()




# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \n
# and rows separated by \n
def printMatrix(inputMatrix):
    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            sys.stdout.write(inputMatrix[j][k] + "\t")
        sys.stdout.write(inputMatrix[j][len(inputMatrix[j])-1] + "\n" )
    sys.stdout.write("\n" )



# it converts a numeric grade into an expression, e.g. 7.25 --> 7+, 7.5 --> 7 1/2
# INCOMPLETE
def computeLetterGrade(grade):
   int_, dec_ = math.modf(grade)
   return `int_`


# it computes the grades, i.e. the normalized scores
def makeGrades(number,scores):
   # print number


   positions = []
   positions = [0 for k in range(0,number)]
   for k in range(0,number):
      positions[k:k+1] = [k+1]
   # print positions

   # list with the number of repeated scores for each score
   repetitions = []
   repetitions = [0 for k in range(0,number)]
   for k in range(0,number):
       #repetedScore = float()
       repetitions[k:k+1] = [scores.count(scores[k])]
   # print repetitions

   # difference between successive scores
   delta = []
   delta = [0.0 for k in range(0,number-1)]
   for k in range(0,number-1):
       delta[k:k+1] = [scores[k+1]-scores[k]]
   # print delta


   floatPositions = []
   floatPositions = [float(k+1) for k in range(0,number)]
   #floatPositions[0:1] = [1.0]
   #floatPositions[number-1:number] = [float(number)]
   for k in range(1,number-1):
       if repetitions[k] == 1:
           floatPositions[k:k+1] = [float(k) + 1.0 - .5*(delta[k] - delta[k-1])/(delta[k] + delta[k-1])]
       else:
           if delta[k-1] != 0.0:
              av = 0.0 #float(positions[k])/float(repetitions[k]) partial average
              #print av
              for j in range(0,repetitions[k]):
                 av = av + float(positions[k+j])/float(repetitions[k]) # average over the repeated positions
              #print av
              if k + repetitions[k] +1 > number:
                 print "over"
              if k + repetitions[k] +1 < number:
                 for j in range(0,repetitions[k]):
                    floatPositions[k+j:k+j+1] = [av - (.5*repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]
                 #[av - (.5/repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]
              else:
                  for j in range(0,repetitions[k]):
                    floatPositions[k+j:k+j+1] = [av]
                 #[av - (.5/repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]

   # print floatPositions


   grades = []
   grades = [0.0 for k in range(0,number)]
   roundgrades = []
   roundgrades = [0.0 for k in range(0,number)]
   roundgrades0 = []
   roundgrades0 = [0.0 for k in range(0,number)]


   for k in range(0,number):
      grades[k:k+1] = [math.sqrt(2)*standardDev*erfinv((2/float(number))*(floatPositions[k]-.5)-1.0)+average]
      roundgrades[k:k+1] = [round(4*grades[k], 0)/4]
      roundgrades0[k:k+1] = [round(grades[k], 0)]
      # print roundgrades[k]

   print "Grades without rounding: "
   print grades
   print
   # rounded to 0 decimals (entrance test)
   return roundgrades0

   # rounded in .25 steps (common test)
   # return roundgrades

   # Grades without rounding
   #return grades


def makeGradesMatrix(tSortedDataMatrix, grades):

   stringGrades = [`grade` for grade in grades]
   tSortedDataMatrix.append(stringGrades)


   gradesMatrix = transposed(tSortedDataMatrix)

   # for k in range(0, len(grades)):
   #    gradesLine = []
   #    gradesLine.append(`k+1`)
   #     # gradesLine.append(`grades[k]`)
   #     gradesLine.append(`roundgrades[k]`)
   #    # gradesLine.append(computeLetterGrade(grades[k]))
   #    gradesMatrix.append(gradesLine)

   print "Matrix of the grades: "
   print gradesMatrix
   return gradesMatrix



def main():


        #### LIST OF CONSTANTS ####

    global mainpath
    mainpath = os.getcwd()

        #### COMMAND LINE OPTIONS ####
    parser = argparse.ArgumentParser()
    # parser.parse_args()
    parser.add_argument("project", help="the project filename")
    args = parser.parse_args()
    projectFileName = args.project
    # pprint args.project
    print "projectFileName: " + projectFileName + "\n"


    global projectMatrix
    projectMatrix = csvFileToMatrix(projectFileName, mainpath)
    print "projectMatrix: \n" + `projectMatrix` + "\n\n"
    # sys.stdout
    # matrixToCsvFile(projectMatrix, `sys.stdout`, "")

    # PROJECT NAME, TYPE
    global projectName, projectType
    projectName = projectMatrix[0][1]
    projectType = projectMatrix[1][1]

    # AVERAGE AND STANDARD DEVIATION OF THE RESULTS
    global average, standardDev
    average = float(projectMatrix[2][1]) # 7.0
    print "Average: " + `average`
    standardDev = float(projectMatrix[3][1]) # 1.2
    print "Standard deviation: " + `standardDev`


    # INPUT FILE NAMES
    #dataFileName = raw_input("dataFileName: ")
    #dataFileName = "1A-verifica-mat2-data.csv"
    dataFileName = projectMatrix[7][1]
    print "File of data: " + dataFileName

    #OUTPUT FILE NAMES
    dataFileOutName = projectMatrix[11][1]
    #print "File of data-out " + dataFileName + ":"


    # matrix with names and scores of the students from dataFile
    global dataMatrix
    dataMatrix = csvFileToMatrix(dataFileName, mainpath + "/input" )
    #print `dataMatrix` + "\n"
    #printMatrix(dataMatrix)

    # number of grades
    global number
    number = len(dataMatrix)
    print "Number of grades: " + `number` + "\n"

    #### END LIST OF CONSTANTS ####


    #tDataMatrix = transposed(dataMatrix)
    #print tDataMatrix

    #sortedDataMatrix = sorted(dataMatrix, key=lambda scores: float(scores[2]))
    #print sortedDataMatrix

    # tSortedDataMatrix = transposed(sortedDataMatrix)
    tSortedDataMatrix = transposed(sorted(dataMatrix, key=lambda scores: float(scores[2])))
    #print tSortedDataMatrix

    # names and scores to be transformed in grades, contained in datafile
    # names = tDataMatrix[1]
    scores = map(float, tSortedDataMatrix[2])
    # print "Sorted scores: " + `scores` + "\n"

    print "Average score: " + `round(numpy.mean(scores),1)` # + "\n"
    print "Standard deviation of the scores: " + `numpy.std(scores, ddof=1)` + "\n"


    grades = makeGrades(number, scores)
    #roundgrades = grades


    #gradesMatrix =
    #print makeGradesMatrix(grades)
    gradesMatrix = makeGradesMatrix(tSortedDataMatrix, grades)

    matrixToCsvFile(gradesMatrix, dataFileOutName, mainpath + "/output" )

    #print "Sorted grades: " + `grades`

    #printMatrix(grades)







print "***************  SMRT grader ****************\n"

main()
