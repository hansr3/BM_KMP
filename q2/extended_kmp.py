import sys
ALPHABET_SIZE = 26
START_ALPHABET = 97

def extended_kmp(txt, pat):
    output = []

    if len(txt) <= 0 or len(pat) <= 0 or len(txt) < len(pat):
        return output
    else:
        pass

#SP_i(x) computation for KMP
#current implementation: regular sp_i
#implementation of SP_i(x) computation might be correct but see later first
#wait for what arun say about how does SP_i(x) work and whats the difference between regualr SP_i(email)
def compute_sp_i(s):
    z = z_algo(s)
    m = len(s)

    #a 2d-list of alphabet_size x len(pat)
    sp = [[0 for _ in range(ALPHABET_SIZE)] for _ in range(m)] #-> use this later for spi(X)
    #sp_i = [0 for _ in range(m)]

    #print("z:",z) #-> debugging purposes only for z algorithm
    for j in range(m-1, 0, -1):
        i = j + z[j] - 1

        #s[z[j]+1] = pat[SPi(x) + 1] = x
        #print(z[j])
        #print(ord(s[z[j]+1].lower()))
        sp[i][ord(s[z[j]].lower()) - START_ALPHABET] = z[j]

    return sp
#z_algorithm main iteration
#need to modify to be able to use wild card
def z_algo(s):
    z = [0 for _ in range(len(s))]
    len_s = len(s)
    l = 0
    r = 0

    #main iteration for z-algo
    for i in range(len_s):

        if i > 0:
            #base case    
            if i == 1:
                #call base_case()
                z[i], l, r = base_case(s,i,r)
            
            #case 1 (explicit comparison, when iteration is outside of any z-box)
            elif i > r:
                z[i], l, r = case_1(s,i,r,l)
            
            #case 2a (if iteration is withing a z-box)
            elif z[i-l] < r-i+1:
                z[i] = z[i-l]
            
            #case 2b (need to do explicit comparison since the inner z-box > the the outer z-box)
            elif z[i-l] >= r - i + 1:
                z[i], l, r = case_2b(s, i, r, l)

            #case 2c


    return z

#base case for z_algo
def base_case(s,k,r):
    start_z_box = 0
    count = 0
    prefix_start = 0
    matched_substr = k
    end_z_box = r

    #do a base comparison from 2nd index till missmatch
    while matched_substr < len(s) and s[matched_substr] == s[prefix_start]:
        count += 1
        matched_substr += 1
        prefix_start += 1

    if count > 0:
        end_z_box = matched_substr - 1 
        start_z_box = k
    return count, start_z_box, end_z_box

#compute z-algo explicitely
def case_1(s, k,r, l):
    start_z_box = l
    count = 0
    prefix_start = 0
    matched_substr = k
    end_z_box = r

    #do comparison until a missmatch occur
    while matched_substr < len(s) and s[matched_substr] == s[prefix_start]:
        
        count += 1
        prefix_start += 1
        matched_substr += 1

    if count > 0:
        end_z_box = matched_substr - 1
        start_z_box = k
    return count, start_z_box, end_z_box 


def case_2b(s,k,r,l):
    start_z_box = k
    count = 0
    prefix_start = r - k + 1
    matched_substr = r + 1
    end_z_box = r

    while matched_substr < len(s) and s[matched_substr] == s[prefix_start]:
        #count += 1
        matched_substr += 1
        prefix_start += 1
    
    total_count = matched_substr - k

    #if count > 0:
    end_z_box = matched_substr - 1

    return total_count, start_z_box, end_z_box

#open and read a file of specified filename
def read_file(filename):
    f = open(filename, 'r')
    f_name = f.readline()
    f.close()

    return f_name

#create a file of specified filename
#write the output of the computation into a file
def write_file(output):
    f = open("output_kmp.txt", 'w')
    f.write(output[0])

    for i in range(1, len(output)):
        f.write("\n")
        f.write(output[i])

    f.close()

if __name__ == "__main__":
    """ text_file_name = sys.argv[1]
    pat_file_name = sys.argv[2]

    text = read_file(text_file_name)
    pat = read_file(pat_file_name) """

    #print(text)
    #print(pat)

    text_1 = "aabcaabxaay"
    text_2 = "bbccaebbcabd"
    print("spi:",compute_sp_i(text_2))
    #print(z_algo(text_1))  #z_algo testing


    """ output = extended_kmp(text, pat)

    write_file(output) """

