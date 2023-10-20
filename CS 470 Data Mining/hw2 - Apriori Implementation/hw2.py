import itertools
import sys

# read file and prep
textfile = sys.argv[1]
minSup = int(sys.argv[2])
textfile = open(textfile, 'r', encoding='utf-8')
db = {}
db_temp = {}
freq_count = {}
temp_count = {}
count = 1
count2 = 1

# creating freq_count baseline and populating db

for instance in textfile:

    row = ()
    for value in instance.strip().split():
        row += (int(value),)

    # each list of purchase is a set
    updateSet = set()
    for x in row:
        updateSet.add(x)
    db.update({count: updateSet})

    
    for x in row: #candidate generation
        if x in freq_count:
            freq_count.update({x: freq_count.get(x) + 1})
        else:
            freq_count.update({x: 1})

    count = count + 1
    # keep only frequent candidates
for candidates in freq_count:

    if freq_count.get(candidates) >= minSup:
        temp_count.update({candidates: freq_count.get(candidates)})

for row in db:

    if db.get(row) in list(temp_count.keys()):
        db_temp.update({count2: db.get(row)})
        count2 = count2 +1
    db = db_temp.copy()

freq_count = temp_count.copy()

# recursive function for candidate gen, prune, and check
def recur_generation(minSup, db):
    while db: 
        db_temp.clear()
        freq_count_local = {}
        temp_count_here = {}
        count3 = 1

        # wipes items from db that do not contain any frequent sets above minSupport
        for row in list(db.keys()):
            candidate_storage = db[row]
            
            if not candidate_storage:
                db.pop(row)
                continue

            # optimization idea -- prevents over generation of candidates
            # instead of traditional level by level, we iterate through db and generate candidates as we go


            if isinstance(list(db.get(row))[0], int): 
                possible_candidates = set(
                    itertools.combinations(sorted(candidate_storage), 2))
            else: # since all items in db satisfies minSup, any two sets differring by one item are automatically a candidate
                possible_candidates = set()
                for set1, set2 in itertools.product(candidate_storage, candidate_storage):
                    if len(set(set1) - set(set2)) == 1:
                        union_set = tuple(sorted(set(set1).union(set2)))
                        possible_candidates.add(union_set)


            # reduce db size after each generation
            if not possible_candidates:
                db.pop(row)
                continue

            # pruning, keep candidates that has all subsets minSup
            possible_candidates_temp = set()
            if len(list(possible_candidates)[0]) > 2:
                for candidate_gen in list(possible_candidates):
                    if set(itertools.combinations(candidate_gen, len(candidate_gen) - 1)).issubset(candidate_storage):
                        possible_candidates_temp.add(candidate_gen)
                possible_candidates = possible_candidates_temp.copy()

            # any new set that satisfies minSup must be considered for generation of more candidates
            db.update({row: set(possible_candidates)})

            # track freq counts
            for candidate_gen in possible_candidates:
                if candidate_gen not in freq_count_local:
                    freq_count_local.update({candidate_gen: 1})
                else:
                    freq_count_local.update(
                        {candidate_gen: freq_count_local.get(candidate_gen) + 1})

        # keep only the frequent sets
        for candidate_gen in list(freq_count_local.keys()):
            if freq_count_local.get(candidate_gen) >= minSup:
                temp_count_here.update({candidate_gen: freq_count_local.get(candidate_gen)})
        freq_count_local = temp_count_here.copy()

        if not freq_count_local:
            break

        #updating the db
        for row in db:
            if db.get(row) in list(temp_count_here.keys()):
                db_temp.update({count3: db.get(row)})
                count3 = count3 +1
        db = db_temp.copy()
        
        freq_count.update(freq_count_local)


def output():
    #sorting data
    list_output = list(freq_count.keys())
    for i in range(len(list_output)):
        if isinstance(list_output[i], int):
            list_output[i] = (list_output[i],)
    list_output = sorted(list_output)

    #writing the data into text file
    output_file = open(sys.argv[3], "w")
    for i in range(len(list_output)):
        freq_set = list_output[i] if len(
            list_output[i]) > 1 else list_output[i][0]

        output_str = ""
        if isinstance(freq_set, int):
            output_str = str(freq_set)
        else:
            for idx, item in enumerate(freq_set):
                if idx == 0:
                    output_str = str(item)
                else:
                    output_str += " " + str(item)
        output_str += " (%d) " % freq_count[freq_set]

        output_file.write(output_str)
        output_file.write("\n")

def create(): # creates a seperate dictionary for the user to search for frequent sets of specific sizes
    emptylist = {}
    freq_count_ordinated = {}
    last_key = len(list(freq_count.keys())[-1])

    for i in range(1, last_key+1):
        emptylist = freq_count.copy()

        for strings in reversed(list(freq_count.keys())):
            if i == 1:
                if isinstance(strings, tuple):
                    emptylist.pop(strings)
            else:
                if isinstance(strings, tuple):
                    if len(strings) != i:
                        emptylist.pop(strings)
                else:
                    emptylist.pop(strings)

    freq_count_ordinated.update({i: emptylist})

    # Can access freq sets of specific length with freq_count_ordinated
    # print(freq_count_ordinated.get(5))



recur_generation(minSup, db)
output()
#create is to used to create a dictionary to organize freq_counts
#create()