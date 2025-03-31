def kuhn_algorithm(preferences_a, preferences_b):
    rank_b = {b: {a: rank for rank, a in enumerate(prefs)} for b, prefs in preferences_b.items()}
    free_a = list(preferences_a.keys())
    matches = {}  
    partners = {}  
    
    while free_a:
        a = free_a[0]

        if preferences_a[a]:
            b = preferences_a[a][0]  
            preferences_a[a].pop(0)  
            
            if b not in partners:
                partners[b] = a
                matches[a] = b
                free_a.pop(0) 
            else:

                current_match = partners[b]

                if rank_b[b][a] < rank_b[b][current_match]:

                    partners[b] = a
                    matches[a] = b
                    free_a.pop(0)  

                    free_a.append(current_match)
                    del matches[current_match]
        else:

            free_a.pop(0)
    
    return matches

preferences_a = {
    'A1': ['B1', 'B2', 'B3'],
    'A2': ['B2', 'B1', 'B3'],
    'A3': ['B1', 'B3', 'B2']
}

preferences_b = {
    'B1': ['A1', 'A2', 'A3'],
    'B2': ['A2', 'A1', 'A3'],
    'B3': ['A1', 'A3', 'A2']
}

matches = kuhn_algorithm(preferences_a, preferences_b)
print("Final matches:", matches)
