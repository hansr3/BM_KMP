import sys

def extended_kmp(s):
    pass

#SP_i computation for KMP
def compute_sp_i(s):
    pass

#z-algorithm computation
def z_algo(s):
    pass

#open and read a file of specified filename
def read_file(filename):
    f = open(filename, 'r')
    f_name = f.readline()
    f.close()

    return f_name

#create a file of specified filename
#write the output of the computation into a file
def write_file(filename):
    f = open(filename, 'w')
    f.write(output[0])

    for i in range(1, len(output)):
        f.write("\n")
        f.write(output[i])

    f.close()

if __name__ == "__main__":
    text_file_name = sys.argv[1]
    pat_file_name = sys.argv[2]

    text = read_file(text_file_name)
    pat = read_file(pat_file_name)

    print(text)
    print(pat)
    
    """ output = extended_kmp(text)

    write_file(output) """

