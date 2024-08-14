#Note : The matay should have elements of the field GF(2) -- Only 0/1 
def fast_guass(mat): #m rows and n columns

    m_row = len(mat)
    n_col = len(mat[0])

    pivot = [False]*m_row
    pivot_found = False
    pivot_col_to_row = {}
    
    for j in range(n_col):
        pivot_found = False
        #Look for pivot
        for i in range(m_row):
            #Pivot Found at row i and column j
            if(mat[i][j] == 1):
              pivot[i] = True
              pivot_col_to_row[j]=i
              pivot_found = True
              break
          
        if (pivot_found == True):

            for k in range(n_col):
                
                #Pivot row
                if(k == j):
                    continue

                if (mat[i][k] == 1):
                    for row_index in range(m_row):
                        mat[row_index][k] = (mat[row_index][j] + mat[row_index][k])%2
                        
    return (mat,pivot,pivot_col_to_row)

def has_dependent_rows(original_mat):
    mat, pivot, _ = fast_guass(original_mat)

    m_row = len(mat)
    
    for i in range(m_row):
        if (pivot[i] == False):
            return True
        
    return False