cimport numpy as np
import numpy as np

# this file uses cython to speedup certain calculations for the kendall tau distance and weighted mean


# computes tau itself
def tau_cy(np.ndarray[np.int_t, ndim=1] r1, np.ndarray[np.int_t, ndim=1] r2, double penalty):

    cdef double tau = 0

    # create view
    cdef int r1_len = r1.size



    for i in range(r1_len):
        for j in range(r1_len):
            tau = tau +  (r1[i] < r1[j] and r2[i] > r2[j] or
                         r1[i] > r1[j] and r2[i] < r2[j]) \
                  + penalty * (r1[i] == r1[j] and r2[i] != r2[j] or
                               r1[i] != r1[j] and r2[i] == r2[j])

    return tau

# computes the tau-matrix
def tau_matrix_cy(np.ndarray[np.int_t, ndim=1] r1, np.ndarray[np.int_t, ndim=1] r2, double penalty):
    mat = np.zeros((len(r1), len(r1)))

    # create view
    cdef np.ndarray[np.double_t, ndim=2] mat_view = mat
    cdef int r1_len = r1.size



    for i in range(r1_len):
        for j in range(r1_len):
            mat_view[i,j] = (r1[i] < r1[j] and r2[i] > r2[j] or
                         r1[i] > r1[j] and r2[i] < r2[j]) \
                  + penalty * (r1[i] == r1[j] and r2[i] != r2[j] or
                               r1[i] != r1[j] and r2[i] == r2[j])

    return mat


# computes changes after changing the bucket
def try_bucket_cy(np.ndarray[np.int_t, ndim=1] r1, np.ndarray[np.int_t, ndim=1] r2, np.ndarray[np.int_t, ndim=1] r_med,
                  np.ndarray[np.double_t, ndim=2] mat_r1_py, np.ndarray[np.double_t, ndim=2] mat_r2_py, int value, int bucket_index, double penalty, new_bucket):
#     # create copies so we dont change anything important
    r_med_new_py = r_med.copy()
    mat_r1_py = mat_r1_py.copy()
    mat_r2_py = mat_r2_py.copy()

    # setup variables and views
    cdef int r_med_new_len = len(r_med_new_py)
    cdef np.ndarray[np.int_t, ndim=1] r_med_new = r_med_new_py
    cdef np.ndarray[np.double_t, ndim=2] mat_r1 = mat_r1_py
    cdef np.ndarray[np.double_t, ndim=2] mat_r2 = mat_r2_py

    # create new array
    if new_bucket:
        # move all values in bucket new_index
        move_idx = r_med_new >= bucket_index
        r_med_new[move_idx] = r_med_new[move_idx] + 1

    # set new index
    r_med_new[value] = bucket_index

    # update matrices
    for i in range(r_med_new_len):
        mat_r1[value, i] = (r1[value] < r1[i] and r_med_new[value] > r_med_new[i] or
                            r1[value] > r1[i] and r_med_new[value] < r_med_new[i]) \
                            + penalty * (r1[value] == r1[i] and r_med_new[value] != r_med_new[i] or
                               r1[value] != r1[i] and r_med_new[value] == r_med_new[i])
        mat_r1[i, value] =  mat_r1[value, i]
        mat_r2[value, i] = (r2[value] < r2[i] and r_med_new[value] > r_med_new[i] or
                            r2[value] > r2[i] and r_med_new[value] < r_med_new[i]) \
                            + penalty * (r2[value] == r2[i] and r_med_new[value] != r_med_new[i] or
                               r2[value] != r2[i] and r_med_new[value] == r_med_new[i])
        mat_r2[i, value] = mat_r2[i, value]

    # update tau
    tau_r1 = np.sum(mat_r1)
    tau_r2 = np.sum(mat_r2)

    # return everything
    return r_med_new_py, mat_r1_py, mat_r2_py, tau_r1, tau_r2


