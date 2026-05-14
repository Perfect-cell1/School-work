import time


# =========================
# LOAD DATA FROM FILE
# =========================
def load_data(filename):
    data = []
    try:
        with open(filename, "r") as file:
            for line in file:
                row = line.strip().split(",")
                if len(row) != 7:
                    continue
                
                try:
                    
                    v_id = row[0]
                    v_name = row[1]
                    year_week = row[2]
                    vegan = int(row[3])
                    meat = int(row[4])
                    onions = float(row[5])
                    ketchup = int(row[6]) 

                    # --- SIMPLE VALIDATION LOGIC ---

                    # 1. Vendor ID: 2 letters, underscore, 3 digits, all caps
                    if not re.match(r"^[A-Z]{2}_[0-9]{3}$", v_id):
                        continue

                    # 2. Vendor Name: Length 2 to 25
                    if not (2 <= len(v_name) <= 25):
                        continue

                    # 3. Year and Week: YYYYWW and WW between 1-52
                    if len(year_week) != 6:
                        continue
                    week_num = int(year_week[4:])
                    if not (1 <= week_num <= 52):
                        continue

                    # 4. Hotdogs: Divisible by 10
                    if vegan % 10 != 0 or meat % 10 != 0:
                        continue

                    # 5. Onions: Half kilogram increments (e.g., 0.5, 1.0, 1.5)
                    # We check if doubling it results in a whole number
                    if (onions * 2) % 1 != 0:
                        continue

                    # 6. Ketchup: Integer between 1 and 4
                    if not (1 <= ketchup <= 4):
                        continue

                    # If it passed everything, add to data
                    record = {
                        "id": v_id,
                        "name": v_name,
                        "week": int(year_week),
                        "vegan": vegan,
                        "meat": meat,
                        "onions": onions,
                        "ketchup": ketchup
                    }
                    data.append(record)

                except ValueError:
                    continue
                    
    except FileNotFoundError:
        print("Error: File not found.")
    
    return data





# =========================
# LINEAR SEARCH (UNSORTED)
# =========================
def linear_search(data, target):
    for item in data:
        if item["id"] == target:
            return item
    return None


# LINEAR SEARCH THROUFH SORTED DATA

def linear_search_sorted(data, target):
    for item in data:
        if item["id"] == target:
            return item
        elif item["id"] > target:
            break
    return None




# BINARY SEARCH THROUGH THE DATA


def binary_search(data, target): #Initialises the boundaries
    low = 0
    high = len(data) - 1


    try:
        while low <= high: #Continues searching as long as there's an element
                mid = (low + high) // 2 #The formula utilised for it


                if data[mid]["id"] == target: #Check if the searching element is equal to the target
                   return data[mid]
                elif data[mid]["id"] < target: 
                    low = mid + 1 #If middle is lower than target discard left
                else:
                    high = mid - 1 #If middle is higher than target discard right

    except (KeyError,  TypeError):
            print(f"Warning: Skipping malformed entry at index {mid}")

            return None






# =========================
# BUBBLE SORT
# =========================
def bubble_sort(data):
    arr = data.copy()
    n = len(arr)


    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j]["id"] > arr[j+1]["id"]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


    return arr






# =========================
# QUICK SORT
# =========================
def quick_sort(data):
    if len(data) <= 1:
        return data


    pivot = data[0]
    left = [x for x in data[1:] if x["id"] <= pivot["id"]]
    right = [x for x in data[1:] if x["id"] > pivot["id"]]


    return quick_sort(left) + [pivot] + quick_sort(right)






# =========================
# TIMING FUNCTIONS
# =========================
def time_searches(data, target):
    sorted_data = quick_sort(data)


    start = time.time()
    linear_search(data, target)
    t1 = time.time() - start


    start = time.time()
    linear_search_sorted(sorted_data, target)
    t2 = time.time() - start


    start = time.time()
    binary_search(sorted_data, target)
    t3 = time.time() - start


    return t1, t2, t3




def time_sorts(data):
    start = time.time()
    bubble_sort(data)
    t1 = time.time() - start


    start = time.time()
    quick_sort(data)
    t2 = time.time() - start


    return t1, t2

hotdog_data = load_data("Hotdog.txt")
result = time_searches(hotdog_data, "")


# =========================
# DATA ANALYSIS
# =========================
def analyse_data(data):
    vendor_totals = {}
    vegan_total = 0
    meat_total = 0
    least_ketchup_vendor = None
    least_ketchup = float('inf')


    for item in data:
        name = item["name"]


        # Total per vendor
        if name not in vendor_totals:
            vendor_totals[name] = 0


        vendor_totals[name] += item["vegan"] + item["meat"]


        vegan_total += item["vegan"]
        meat_total += item["meat"]


        if item["ketchup"] < least_ketchup:
            least_ketchup = item["ketchup"]
            least_ketchup_vendor = name


    # Most productive vendor
    most_productive = max(vendor_totals, key=vendor_totals.get)


    return {
        "most_productive": most_productive,
        "vegan_total": vegan_total,
        "meat_total": meat_total,
        "least_ketchup_vendor": least_ketchup_vendor
    }



# =========================
# SAVE ANALYSIS TO FILE
# =========================
def save_analysis(results, filename="analysis.txt"):
    with open(filename, "w") as file:
        file.write("HOTDOG DATA ANALYSIS\n")
        file.write("====================\n")
        file.write(f"Most productive vendor: {results['most_productive']}\n")
        file.write(f"Total vegan hotdogs: {results['vegan_total']}\n")
        file.write(f"Total meat hotdogs: {results['meat_total']}\n")
        file.write(f"Least ketchup used by: {results['least_ketchup_vendor']}\n")
    
    return results



# =========================
# MAIN PROGRAM
# =========================
def main():
    data = load_data("Hotdogs.txt")

    if not data:
        print("No data loaded. Please check the file path.")
        return

    # ############################################################
    # SEARCH INPUT VALIDATION
    # ############################################################
    
    # Create a unique list of vendor names for validation
    name_to_id = {item["name"]: item["id"] for item in data}
    
    while True:
        target = input("Enter the Vendor Name to search: ").strip()

        # Validation: Check if the input name exists in our records
        if target in name_to_id:
            target_id = name_to_id[target]
            print(f"--- Valid Vendor Selected: {target} (ID: {target_id}) ---")
            break
        else:
            # Error message if the name is not found
            print(f"Error: '{target}' is not in our records. Please try again.")
  

    # SEARCH TIMINGS
    t1, t2, t3 = time_searches(data, target)

    print("\nSearch Times:")
    print(f"Linear (unsorted): {t1}")
    print(f"Linear (sorted): {t2}")
    print(f"Binary: {t3}")

    # SORT TIMINGS
    t1, t2 = time_sorts(data)

    print("\nSort Times:")
    print(f"Bubble sort: {t1}")
    print(f"Quick sort: {t2}")

    # ANALYSIS
    results = analyse_data(data)

    print("\nAnalysis:")
    print(results)

    save_analysis(results)


# RUN PROGRAM
main()
