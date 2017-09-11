#
# Extracts the poissons ration form a 3D cube
#
#@date: 2015
#@author: diehl@ins.uni-bonn.de
#

from vtk import *
from numpy import *
import sys
import getopt
import csv
from vtk.util.numpy_support import vtk_to_numpy

def main(argv):

    
    sigma_11 = []
    sigma_22 = []
    sigma_12 = []
    eps_11 = []
    eps_22 = []
    gamma_12 = []
    strain = []
    
    with open('csv/cantilever_deformed.csv', 'rb') as csvfile:
    	spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
	spamreader.next()
	for row in spamreader:
	    strain.append(float(row[len(row) - 1]))
	    gamma_12.append(float(row[len(row) - 2]))
	    eps_22.append(float(row[len(row) - 3]))
	    eps_11.append(float(row[len(row) - 4]))
	    sigma_12.append(float(row[len(row) - 5]))
	    sigma_22.append(float(row[len(row) - 6]))
	    sigma_11.append(float(row[len(row) - 7]))
	    
    reader=vtkXMLUnstructuredGridReader()
    reader.SetFileName("/home/apollon/p108903/Rolland/output_1.vtu")
    reader.Update()

    data=reader.GetOutput()

    # Get the points from the file
    points=data.GetPoints()

    # Get the Coordinates
    numPoints=points.GetNumberOfPoints()
    x=zeros(numPoints)
    y=zeros(numPoints)
    z=zeros(numPoints)

    nx=[]
    ny=[]
    nz=[]

    for i in range(numPoints):
        x[i], y[i], z[i]=points.GetPoint(i)


    diff_eps_xx = []
    diff_eps_yy = []
    diff_gamma_xy = []
    diff_sigma_xx = []
    diff_sigma_yy = []
    diff_sigma_xy = []
    diff_strain_energy = []

    pd_strain_energy = vtk_to_numpy(data.GetPointData().GetArray("Strain_Energy"))
    pd_strain = vtk_to_numpy(data.GetPointData().GetArray("Strain"))
    pd_stress = vtk_to_numpy(data.GetPointData().GetArray("Stress"))
   
   

    for i in range(0,len(strain)):
    
    
    	 diff_eps_xx.append(abs(pd_strain[i][0]+1e-11 - eps_11[i]+1e-11 ) / abs(eps_11[i]+1e-11) )
    	 diff_eps_yy.append(abs(pd_strain[i][1]+1e-11 - eps_22[i]+1e-11 ) / abs(eps_22[i]+1e-11))
         diff_gamma_xy.append(abs(2*pd_strain[i][2]+1e-11 - gamma_12[i]+1e-11 ) / abs(gamma_12[i]+1e-11))
         diff_sigma_xx.append(abs(pd_stress[i][0]+1e-11 - sigma_11[i] +1e-11) / abs(sigma_11[i]+1e-11))
         diff_sigma_yy.append(abs(pd_stress[i][1]+1e-11 - sigma_22[i] +1e-11) / abs(sigma_22[i]+1e-11))
         diff_sigma_xy.append(abs(pd_stress[i][2]+1e-11 - sigma_12[i]+1e-11 ) / abs(sigma_12[i]+1e-11))
	 diff_strain_energy.append(abs( pd_strain_energy[i]-strain[i]) / strain[i] )
	



    # Write the vtk file
    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName("error.vtu");

    # Generate the grid
    grid = vtkUnstructuredGrid()

    # Add points and fields
    points = vtkPoints()
    points.SetNumberOfPoints(len(x))
    points.SetDataTypeToDouble()

    for i in range(len(x)):
        points.InsertPoint(i,x[i],y[i],z[i])

    grid.SetPoints(points)

    disArray = vtkDoubleArray()
    disArray.SetName("eps_xx")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_eps_xx[i]))

    dataOut = grid.GetPointData()

    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("eps_yy")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_eps_yy[i]))
        
    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("eps_xy")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_gamma_xy[i]))
        
    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("sigma_xx")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_sigma_xx[i]))
        
    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("sigma_yy")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_sigma_yy[i]))
        
    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("sigma_xy")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_sigma_xy[i]))
        
    dataOut.AddArray(disArray)
    
    disArray = vtkDoubleArray()
    disArray.SetName("starin_energy")
    disArray.SetNumberOfComponents(1)
    disArray.SetNumberOfTuples(len(strain))

    for i in range(len(strain)):
        disArray.SetTuple1(i,float(diff_strain_energy[i]))
        
    dataOut.AddArray(disArray)
    
    
    writer.SetInputData(grid)

    # Add compression
    writer.GetCompressor().SetCompressionLevel(0)
    writer.SetDataModeToAscii()

    # Write the grid
    writer.Write()


if __name__ == "__main__":
    main(sys.argv[1:])
