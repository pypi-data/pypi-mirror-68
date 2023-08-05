from mathx.vectorize import *

def test_subarray_axes():
    ##       
    array=np.array([1,2,3])
    arrays=(array,)
    elements=list(subarrays(arrays,iteration_axes=(-1,)))
    assert elements[1][0]==2
    ##
    elements=list(subarrays(arrays,iteration_axes=()))
    assert elements[0][0] is array
    ##
    array0=np.array([0,1,2])
    array1=np.array([0,1])[:,None]
    elements=list(subarrays((array0,array1),iteration_axes=(-1,)))
    assert np.array_equal(elements[1][0],np.array([1])) and np.array_equal(elements[1][1],array1)
    ##
    elements=list(subarrays((array0,array1),subarray_axes=(-2,)))
    assert np.array_equal(elements[1][0],np.array([1])) and np.array_equal(elements[1][1],array1)
    ##
    elements=list(subarrays((array0,array1),iteration_axes=(-2,)))
    assert np.array_equal(elements[1][0],array0) and np.array_equal(elements[1][1],np.array([[1]]))
    ## Assignment
    array0=np.array([[0,1,2],[3,4,5],[6,7,8]])
    array1=np.array([[0,1,2],[3,4,5]])
    array2=np.array([0,1,2])
    array2_orig=array2.copy()
    for (sub0,sub1,sub2) in subarrays((array0,array1,array2),iteration_axes=(-1,)):
        print(sub0,sub1,sub2)
        sub2[:]+=sub0.sum()+sub1.sum()
    assert np.array_equal(array2,array2_orig+array0.sum(0)+array1.sum(0))
    ##
   
    
    ##
if __name__=="__main__":
    test_subarray_axes()
