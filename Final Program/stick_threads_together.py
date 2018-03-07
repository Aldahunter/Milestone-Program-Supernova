import numpy as np

num_threads = int(input("How many threads: "))

file_names = ['w_omega_contour_data_bottom',
              'w_omega_contour_data_bottom_q',
              'w_omega_contour_data_bottom_age']

for f in file_names:
    thread_data, row_size = {}, 0
    for n in range(num_threads):
        thread_data[n] = np.loadtxt((f+"({},{}).txt").format(n, int(num_threads)))
        print(thread_data[n].shape)
        row_size += thread_data[n].shape[0]
    print(row_size)

    all_arr = np.empty((row_size, thread_data[0].shape[1]))
    print(all_arr.shape)


    for n in range(num_threads):
        all_arr[n::num_threads] = thread_data[n]

    print(all_arr.shape)
    np.savetxt(f+"(all_threads).txt", all_arr)

# cor_arr = np.loadtxt("w_omega_contour_data(0,1).txt")
#
# if np.array_equal(all_arr, cor_arr): print(True)
# else: print(False)
