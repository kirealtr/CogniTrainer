def get_biases_for_table():
    biases = []
    with open("./data/biases.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            bias, definition, source = line.split(";")
            biases.append([cnt, bias, definition])
            cnt += 1
    return biases


def write_bias(new_bias, new_definition):
    new_bias_line = f"{new_bias};{new_definition};user"
    with open("./data/biases.csv", "r", encoding="utf-8") as f:
        existing_biases = [l.strip("\n") for l in f.readlines()]
        title = existing_biases[0]
        old_biases = existing_biases[1:]
    biases_sorted = old_biases + [new_bias_line]
    biases_sorted.sort()
    new_biases = [title] + biases_sorted
    with open("./data/biases.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_biases))


def get_biases_stats():
    db_biases = 0
    user_biases = 0
    defin_len = []
    with open("./data/biases.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            bias, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_biases += 1
            elif "db" in added_by:
                db_biases += 1
    stats = {
        "biases_all": db_biases + user_biases,
        "biases_own": db_biases,
        "biases_added": user_biases,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats
