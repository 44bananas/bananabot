#grading

import grading_data

def get_stats(weapon):
    if (weapon.upper() in grading_data.pistol_dispos):
        return (grading_data.pistol_base_stats, grading_data.pistol_dispos[weapon.upper()])
    elif (weapon.upper() in grading_data.rifle_dispos):
        return (grading_data.rifle_base_stats, grading_data.rifle_dispos[weapon.upper()])
    elif (weapon.upper() in grading_data.shotgun_dispos):
        return (grading_data.shotgun_base_stats, grading_data.shotgun_dispos[weapon.upper()])
    elif (weapon.upper() in grading_data.melee_dispos):
        return (grading_data.melee_base_stats, grading_data.melee_dispos[weapon.upper()])
    elif (weapon.upper() in grading_data.archgun_dispos):
        return (grading_data.archgun_base_stats, grading_data.archgun_dispos[weapon.upper()])
    else:
        raise Exception("weapon type not found",weapon)

def grade_stat(weapon, stat_name, stat_value):
    (stats, dispo) = get_stats(weapon)
    if stat_name in stats:
        base_stat = stats[stat_name]
        avg_val = base_stat * dispo
        avg_val = round(avg_val, 3)
        #.9375 is the 3 stat riven modifier
        avg_val = avg_val * 0.9375
        stat_value = float(stat_value)
        grade = stat_value/avg_val
        grade = round(grade,3)
        #output grade
        if grade >= 1.102:
            return(grade, "? grade")
        if 1.095 <= grade and grade < 1.101:
            return (grade, "S grade")
        if 1.075 <= grade and grade < 1.095:
            return (grade, "A+ grade")
        if 1.055 <= grade and grade < 1.075:
            return (grade, "A grade")
        if 1.035 <= grade and grade < 1.055:
            return (grade, "A- grade")
        if 1.015 <= grade and grade < 1.035:
            return (grade, "B+ grade")
        if 0.985 <= grade and grade < 1.015:
            return (grade, "B grade")
        if .965 <= grade and grade < .985:
            return (grade, "B- grade")
        if .945 <= grade and grade < .965:
            return (grade, "C+ grade")
        if .925 <= grade and grade < .945:
            return (grade, "C grade")
        if .905 <= grade and grade < .925:
            return (grade, "C- grade")
        if .9 <= grade and grade < .905:
            return (grade, "F grade")
        if grade <= .89:
            return (grade, "? grade")

def grade_weapon(weapon, stat1val, stat1name, stat2val, stat2name, stat3val, stat3name):
    grade1 = ()
    if (stat1name != ""):
        grade1 = grade_stat(weapon, stat1name, stat1val)
    else:
        grade1 = ("", "")
    grade2 = ()
    if (stat2name != ""):
        grade2 = grade_stat(weapon, stat2name, stat2val)
    else:
        grade2 = ("", "")
    grade3 = ()
    if (stat3name != ""):
        grade3 = grade_stat(weapon, stat3name, stat3val)
    else:
        grade3 = ("", "")

    return [
        grade1,
        grade2,
        grade3,
    ]
