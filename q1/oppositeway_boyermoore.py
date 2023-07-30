import sys

#constants
STARTING_ASCII = 97
NUM_ALPHABET = 26

def q2(txt, pat):
    
    return oppositeway_boyermoore(txt, pat)

#allows a char "." which matches with any string in the 26 alphabet 
def oppositeway_boyermoore(txt, pat):
    m = len(pat)
    n = len(txt)
    i = n - m
    pat_i = 0
    z = [0 for _ in range(m)]
    R = None
    z_suffix = None
    matched_suffix = None
    good_suffix = None
    to_shift = 0
    occurence = []


    #compute z_value 
    z = z_algo(pat) #(DONE)

    #compute Rk(x)
    R = compute_R(pat)  #(DONE)

    #compute z_suffix 
    z_suffix = compute_backward_z_suffix(pat) #(DONE)

    #compute good_suffix
    good_suffix = compute_good_suffix(pat)   #(DONE)

    #compute matched_prefix
    matched_suffix = compute_matched_suffix(pat) #(DONE)


    #main iteration of boyer_moore
    while i > -1:

        text_i = i
        k = pat_i
        j = text_i + m - 1 #text_i - (m - 1)    #starting substring region in txt
        while pat_i < m and txt[text_i] == pat[pat_i]:
            text_i += 1
            pat_i += 1
            k = pat_i
        
        
        
        x = txt[j - k]
        if k < m:
            b_shift = bad_char_shift(x, k, R)
            matched, g_shift = good_suffix_shift(good_suffix, matched_suffix,k, m)
        else:
            g_shift = abs(0 - matched_suffix[-3])
            matched = True
        to_shift = max(b_shift, g_shift)

        if matched:
            occurence.insert(0 ,j - m + 1)

        i -= to_shift #remove + 1 myb if got bug
        pat_i = 0

    return occurence

#function to compute Rk(x) value
#need to modify to be able to use wildcard
def compute_R(pat):
    m = len(pat)
    R = [[-1 for _ in range(NUM_ALPHABET)] for _ in range(len(pat))]

    for i in range(m-2 , -1, -1):
        
        # if iteration is at index 1
        if i == m - 2:

            # # store index of the leftmost occurence of a char into R-list
            # occurence of char i + 1 of current iteration
            R[i][ord(pat[i + 1]) - STARTING_ASCII] = i + 1
        # any other iteration
        else:
            # Copy the value of 
            for j in range(NUM_ALPHABET):

                #Copy when value index is available
                if R[i+1][j] > -1:
                    R[i][j] = R[i+1][j]

            # store index of the rightmost occurence of a char into R-list
            # occurence of char i - 1 of current iteration
            R[i][ord(pat[i+1]) - STARTING_ASCII] = i + 1


    return R

#function to compute matched_prefix value
#solution from q7 week 2 tute
def compute_matched_suffix(pat):
    m = len(pat)
    m_prefix = [0 for _ in range(len(pat) + 1)]

    #z_suffix = compute_backward_z_suffix(pat)
    z_suffix = compute_backward_z_suffix(pat)
    
    #print(z_suffix)
    """ for i in range(len(pat) - 1, 0, -1):
        if z[i]+i == len(pat):
            m_prefix[i] = z[i]  #found a new largest suffix that matches its prefix
        else:
            m_prefix[i] = m_prefix[i+1] #otherwise, previously found value is copied """
    
    for i in range(m-1):
        if i - z_suffix[i] == -1:
            m_prefix[i] = z_suffix[i]   #found a new largest prefix that matches its suffix 
        else:
            m_prefix[i] = m_prefix[i-1] #otherwise, previously found value is copied
    #print(m_prefix)
    m_prefix[-2] = len(pat)
    return m_prefix

#function to compute z_suffix
#the backward version of this should be z_values
def compute_backward_z_suffix(pat):
    inv_pat = ""
    inv_z = None
    z_suffix = []
    for i in range(len(pat) - 1, -1, -1):
        inv_pat += pat[i]

    inv_z = z_algo(inv_pat)

    for i in range(len(inv_z) - 1, -1, -1):
        z_suffix.append(inv_z[i])
    
    return z_suffix

#function to compute good_suffix
def compute_good_suffix(pat):
    z_values = z_algo(pat)#compute_backward_z_suffix(pat)
    m = len(pat)
    g_sfx = [0 for _ in range(m+1)]

    print(z_values)
    for p in range(m-1, 0, -1):
        j = z_values[p] - 1
        g_sfx[j] = p

    return g_sfx


#function to compute shfit by bad_char rule
def bad_char_shift(x, k, R):

    #only if there is a missmatch
    if k is not None:
        if R[k][ord(x)-STARTING_ASCII] == -1:
            return 1
        else:
            return abs(k - R[k][ord(x)-STARTING_ASCII])    



#function to compute shift by good_suffix rule
def good_suffix_shift(g_sffx, m_pref, k, m):
    
    #case 1a
    if g_sffx[k+1] > 0:
        return False, abs(0 - g_sffx[k+1])#False, m - g_sffx[k+1]

    #case 1b
    elif g_sffx[k+1] == -1:
        return False, abs(0 - m_pref[k+1])#False, m - m_pref[k+1]

    #case 2 (when the whole substring matches with the pattern)
    elif k >= m:
        return True, abs(0 - m_pref[-3])#True, m - m_pref[1]
    
    #return 0 shift if no cases match
    else:
        return False, 0
        
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

#function to read input from given text_file_name
def read_input(fileName):
    f = open(fileName, 'r')
    content = f.readline()
    f.close

    return content

#function to write into a txt file of given text_file_name
#output = .txt file
def write_output(output):
    f = open('output_oppositeway_boyermoore.txt','w')
    f.write(str(output[0] + 1))
    for i in range(1, len(output)):
        f.write("\n")
        f.write(str(output[i] + 1))
    f.close()

if __name__ == '__main__':

    """ textFileName, patFileName = sys.argv[1], sys.argv[2]

    txt, pat = read_input(textFileName), read_input(patFileName) """

    txt = "abcdabcdabcd"
    pat = "abc"
    output = q2(txt, pat)

    pat_1 = "tbapxab"
    pat_2 = "acababacaba"

    #print(compute_R(pat_1)) #test compute R
    #print(compute_good_suffix(pat_2))
    #print(compute_matched_suffix(pat_2))
    print(output)

    """ write_output(output) """





