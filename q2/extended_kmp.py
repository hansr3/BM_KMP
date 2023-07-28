import sys
ALPHABET_SIZE = 26
START_ALPHABET = 97

def extended_kmp(txt, pat):
    output = []

    if len(txt) <= 0 or len(pat) <= 0 or len(txt) < len(pat):
        return output
    else:
        
        #main KMP iteration starts here

        #pat and txt len
        m = len(pat)
        n = len(txt)

        """ #The last index of pat being compared to j+i-1
        last_pat_txt_index = m - 1 """

        #sp values
        sp = compute_sp_i_x(pat)

        #starting region comparison for txt
        j = 0
        i = 0
        while j < n: #last_pat_txt_index < n
            
            while i < m and j < n and txt[j] == pat[i]: #txt[j_iter] == pat[i]:
                j += 1
                i += 1

            """ if j >= n:
                break """

            #if no missmatch (i.e. pattern occurance found)
            if i == m:
                #append starting of index of occurence based on txt index to output
                #shift by m-SP_i(x)
                output.append(j-m)
                i = i - (m - sp[-1])

            #if missmatch is found between pattern and region of text at position i
            else:
                if j >= n:
                    break
                #shift by i - SP_i(x)
                elif i == 0:      #(if i <= 0 then no choice but to compare the next char in txt)
                    i = 0
                    j += 1
                else:
                    i = i - (i - sp[i-1][ord(txt[j+1])-START_ALPHABET])         # +2 because +1 is x (the missmatched character with y in pat but matches x in txt)
                    j += 1                                                      #+2 passed x

            # the new j + m - 1
            #last_pat_txt_index = j + m - 1
        return output



#SP_i(x) computation for KMP
#current implementation: regular sp_i
#implementation of SP_i(x) computation might be correct but see later first
#wait for what arun say about how does SP_i(x) work and whats the difference between regualr SP_i(email)
def compute_sp_i_x(p):
    z = z_algo(p)
    m = len(p)

    #a 2d-list of alphabet_size x len(pat)
    sp_i_x = [[0 for _ in range(ALPHABET_SIZE)] for _ in range(m-1)] #-> use this later for spi(X)
    sp_i_x.append(0)
    sp = compute_SP_i(p)

    
    for i in range(len(sp_i_x)):
        for j in range(len(sp_i_x[0])):

            #if it's SP_m
            if i == m - 1:
                sp_i_x[i] = sp[i]

            #else SP_i
            else:
                # if the SP[i][x] + 1 == x 
                if p[sp[i] + 1] == chr(j + START_ALPHABET):
                    new_val = sp[i] + 1
                    sp_i_x[i][j] = sp[i] + 1
                    
                # if not
                else:
                    # if sp_i is 0
                    if sp[i] == 0:
                        sp_i_x[i][j] = 0
                    # if not 0 but not x
                    else:
                        #set the SPi(x) value to be SPi-1(x)
                        # this is so that it will be shifted towards
                        # the longest proper suffix that matches its prefix with a char x
                        # from that point
                        sp_i_x[i][j] = sp_i_x[i-1][j]


    return sp_i_x

#function that computes the regular sp_i
def compute_SP_i(s):
    z = z_algo(s)
    m = len(s)

    #SPI array declaration
    sp = [0 for _ in range(m)]

    for j in range(m-1, 0, -1):
        i = j + z[j] - 1
        sp[i] = z[j]

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
    f.write(str(output[0] + 1))

    for i in range(1, len(output)):
        f.write("\n")
        f.write(str(output[i] + 1))

    f.close()

if __name__ == "__main__":
    text_file_name = sys.argv[1]
    pat_file_name = sys.argv[2]

    text = read_file(text_file_name)
    pat = read_file(pat_file_name)

    
    output = extended_kmp(text.lower(), pat.lower())

    write_file(output)

