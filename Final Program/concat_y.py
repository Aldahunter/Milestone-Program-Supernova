import numpy as np

num_threads = int(input("How many threads: "))

top_f_ext = '(all_threads)'
bot_f_ext = '_bottom(all_threads)'
file_names = ['w_omega_contour_data',
              'w_omega_contour_data_q',
              'w_omega_contour_data_age']

for f in file_names:
    top = np.loadtxt(f+top_f_ext+'.txt.')
    bot = np.loadtxt(f+bot_f_ext+'.txt.')
    print("Top size:", top.size)
    print("Bottom size:", bot.size)

    both = np.c_[bot, top]
    print("Concatenated size:", both.size)

    np.savetxt(f+'(concat_y).txt', both)
