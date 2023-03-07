from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from functools import reduce
from time import sleep
from statistics import mean
from send import bet_siska

def creation():
    try:
        url = "https://www.handball24.com"
        browser = webdriver.Chrome()
        browser.get(url)
        resume = input("Select matches and press enter to continue(Add to favorite) ")
        browser.implicitly_wait(1)
        matches = browser.find_elements(By.CSS_SELECTOR,"[id^='g_7']")
        checklist = list()
        for i in matches:
            link = i.get_attribute("id")
            urls = f"https://www.handball24.com/match/{link[4:]}"
            checklist.append(urls)
    finally:
        browser.quit()
    return checklist

schedule = creation()



def check_link(url):
    print(url)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps, options=options)
    browser.get(url)
    browser.implicitly_wait(1)
    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
        "href") + "results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
        "href") + "results/"
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text
    print(title)

    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            # print(line)
            if "(" in line or "Awrd" in line or "Abn" in line or "WO" in line:
                continue
            if len([i for i in line.split() if i.isdigit()]) < 6:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser, link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_7']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches, team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser, link1)
        match_list_away, team2 = get_data(browser, link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)

    team1_name = games[2].split()
    team2_name = games[3].split()

    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18", "U19", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        print(team_)
        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches

    team1_home, team1_away = separation_home_away(team1_name, games[0])
    team2_home, team2_away = separation_home_away(team2_name, games[1])

    results_1 = games[0]
    results_2 = games[1]

    def get_scores(results):
        scorelines = []
        for match in results:
            if len([i for i in match if i.isdigit()]) < 10:
                continue
            if "AOT" in match:
                scoreline = match[-13:-1]
            else:
                scoreline = match[-11:-1]
            scorelines.append(list(map(int, scoreline)))
        return scorelines

    def get_scores(results):
        scorelines = []
        for match in results:
            if len([ i for i in match if i.isdigit() ]) < 6:
                continue
            if "AET" in match or 'Pen' in match:
                scoreline = match[-9:-1]
            else:
                scoreline = match[-7:-1]
            scorelines.append(list(map(int,scoreline)))
        return scorelines

    for i in get_scores(team1_home):
        print(i)


    def half_one(scores):
        dataset1, dataset2 = [], []

        for matches in scores:
            dataset1.append(matches[2])
            dataset2.append(matches[3])

        return dataset1, dataset2, list(map(sum,zip(dataset1,dataset2)))

    def half_two(scores):
        dataset1, dataset2 = [], []

        for matches in scores:
            dataset1.append(matches[4])
            dataset2.append(matches[5])

        return dataset1, dataset2, list(map(sum,zip(dataset1,dataset2)))

    ''' Team1 at home totals '''
    team1_scored_1h_home_ind = half_one(get_scores(team1_home))[0]
    team1_conceded_1h_home_ind = half_one(get_scores(team1_home))[1]
    team1_1h_home_total = half_one(get_scores(team1_home))[2]
    team1_scored_2h_home_ind = half_two(get_scores(team1_home))[0]
    team1_conceded_2h_home_ind = half_two(get_scores(team1_home))[1]
    team1_2h_home_total = half_two(get_scores(team1_home))[2]
    team1_scored_ind_home = list(map(sum,zip(team1_scored_1h_home_ind, team1_scored_2h_home_ind)))
    team1_conceded_ind_home = list(map(sum, zip(team1_conceded_1h_home_ind, team1_conceded_2h_home_ind)))
    team1_total_home = list(map(sum, zip(team1_scored_ind_home, team1_conceded_ind_home)))
    ''' Team1  away totals '''
    team1_scored_1h_away_ind = half_one(get_scores(team1_away))[1]
    team1_conceded_1h_away_ind = half_one(get_scores(team1_away))[0]
    team1_1h_away_total = half_one(get_scores(team1_away))[2]
    team1_scored_2h_away_ind = half_two(get_scores(team1_away))[1]
    team1_conceded_2h_away_ind = half_two(get_scores(team1_away))[0]
    team1_2h_away_total = half_two(get_scores(team1_away))[2]
    team1_scored_ind_away = list(map(sum,zip(team1_scored_1h_away_ind, team1_scored_2h_away_ind)))
    team1_conceded_ind_away = list(map(sum, zip(team1_conceded_1h_away_ind, team1_conceded_2h_away_ind)))
    ''' Team2 at home totals '''
    team2_scored_1h_home_ind = half_one(get_scores(team2_home))[0]
    team2_conceded_1h_home_ind = half_one(get_scores(team2_home))[1]
    team2_1h_home_total = half_one(get_scores(team2_home))[2]
    team2_scored_2h_home_ind = half_two(get_scores(team2_home))[0]
    team2_conceded_2h_home_ind = half_two(get_scores(team2_home))[1]
    team2_2h_home_total = half_two(get_scores(team2_home))[2]
    team2_scored_ind_home = list(map(sum,zip(team2_scored_1h_home_ind, team2_scored_2h_home_ind)))
    team2_conceded_ind_home = list(map(sum, zip(team2_conceded_1h_home_ind, team2_conceded_2h_home_ind)))
    ''' Team2  away totals '''
    team2_scored_1h_away_ind = half_one(get_scores(team2_away))[1]
    team2_conceded_1h_away_ind = half_one(get_scores(team2_away))[0]
    team2_1h_away_total = half_one(get_scores(team2_away))[2]
    team2_scored_2h_away_ind = half_two(get_scores(team2_away))[1]
    team2_conceded_2h_away_ind = half_two(get_scores(team2_away))[0]
    team2_2h_away_total = half_two(get_scores(team2_away))[2]
    team2_scored_ind_away = list(map(sum,zip(team2_scored_1h_away_ind, team2_scored_2h_away_ind)))
    team2_conceded_ind_away = list(map(sum, zip(team2_conceded_1h_away_ind, team2_conceded_2h_away_ind)))
    team2_total_away = list(map(sum, zip(team2_scored_ind_away, team2_conceded_ind_away)))

    def handicap(scores):
        dataset1_total, dataset2_total = [], []
        dataset1_1half, dataset2_1half = [], []
        dataset1_2half, dataset2_2half = [], []

        for match in scores:
            dataset1_total.append(match[2]+match[4] - match[3]-match[5])
            dataset2_total.append(match[3]+match[5] - match[2]-match[4])

            dataset1_1half.append(match[2] - match[3])
            dataset2_1half.append(match[3] - match[2])

            dataset1_2half.append(match[4] - match[5])
            dataset2_2half.append(match[5] - match[4])

        return dataset1_total, dataset2_total, dataset1_1half, dataset2_1half, dataset1_2half, dataset2_2half

    ''' Team1 handicaps ...'''
    team1_handicap_total_home = handicap(get_scores(team1_home))[0]
    team1_handicap_total_away = handicap(get_scores(team1_away))[1]
    team1_handicap_1half_home = handicap(get_scores(team1_home))[2]
    team1_handicap_1half_away = handicap(get_scores(team1_away))[3]
    team1_handicap_2half_home = handicap(get_scores(team1_home))[4]
    team1_handicap_2half_away = handicap(get_scores(team1_away))[5]
    ''' Team2 handicaps ...'''
    team2_handicap_total_home = handicap(get_scores(team2_home))[0]
    team2_handicap_total_away = handicap(get_scores(team2_away))[1]
    team2_handicap_1half_home = handicap(get_scores(team2_home))[2]
    team2_handicap_1half_away = handicap(get_scores(team2_away))[3]
    team2_handicap_2half_home = handicap(get_scores(team2_home))[4]
    team2_handicap_2half_away = handicap(get_scores(team2_away))[5]



    """  Mean values ... """

    """  Team1   """
    mean_t1_ind_scored_home = round(mean(team1_scored_ind_home), 1)
    mean_t1_ind_scored1H_home = round(mean(team1_scored_1h_home_ind), 1)
    mean_t1_ind_scored2H_home = round(mean(team1_scored_2h_home_ind), 1)
    mean_t1_ind_conceded_home = round(mean(team1_conceded_ind_home), 1)
    mean_t1_ind_conceded1H_home = round(mean(team1_conceded_1h_home_ind), 1)
    mean_t1_ind_conceded2H_home = round(mean(team1_conceded_2h_home_ind), 1)


    mean_t1_ind_scored_away = round(mean(team1_scored_ind_away), 1)
    mean_t1_ind_scored1H_away = round(mean(team1_scored_1h_away_ind), 1)
    mean_t1_ind_scored2H_away = round(mean(team1_scored_2h_away_ind), 1)
    mean_t1_ind_conceded_away = round(mean(team1_conceded_ind_away), 1)
    mean_t1_ind_conceded1H_away = round(mean(team1_conceded_1h_away_ind), 1)
    mean_t1_ind_conceded2H_away = round(mean(team1_conceded_2h_away_ind), 1)

    """  Team2  """
    mean_t2_ind_scored_home = round(mean(team2_scored_ind_home), 1)
    mean_t2_ind_scored1H_home = round(mean(team2_scored_1h_home_ind), 1)
    mean_t2_ind_scored2H_home = round(mean(team2_scored_2h_home_ind), 1)
    mean_t2_ind_conceded_home = round(mean(team2_conceded_ind_home), 1)
    mean_t2_ind_conceded1H_home = round(mean(team2_conceded_1h_home_ind), 1)
    mean_t2_ind_conceded2H_home = round(mean(team2_conceded_2h_home_ind), 1)

    mean_t2_ind_scored_away = round(mean(team2_scored_ind_away), 1)
    mean_t2_ind_scored1H_away = round(mean(team2_scored_1h_away_ind), 1)
    mean_t2_ind_scored2H_away = round(mean(team2_scored_2h_away_ind), 1)
    mean_t2_ind_conceded_away = round(mean(team2_conceded_ind_away), 1)
    mean_t2_ind_conceded1H_away = round(mean(team2_conceded_1h_away_ind), 1)
    mean_t2_ind_conceded2H_away = round(mean(team2_conceded_2h_away_ind), 1)

    def per_minute(data, minute):
        ''' for half minute -> 30
            for fulltime minute -> 60 '''

        return round(data/minute, 2)

    def noramal_value(*args):
        return round(sum(args) / 2, 1)

    '''   Aprox. values for main totol coef.
            to compare with...  '''

    match_mean_total = noramal_value(mean_t1_ind_scored_home, mean_t2_ind_conceded_away, mean_t1_ind_conceded_home, mean_t2_ind_scored_away)
    match_mean_1H = noramal_value(mean_t1_ind_scored1H_home, mean_t2_ind_conceded1H_away, mean_t1_ind_conceded1H_home, mean_t2_ind_scored1H_away)
    match_mean_2H = noramal_value(mean_t1_ind_scored2H_home, mean_t2_ind_conceded2H_away, mean_t1_ind_conceded2H_home,
                                  mean_t2_ind_scored2H_away)
    match_mean_t1_H1_ind = noramal_value(mean_t1_ind_scored1H_home, mean_t2_ind_conceded1H_away)
    match_mean_t2_H1_ind = noramal_value(mean_t1_ind_conceded1H_home, mean_t2_ind_scored1H_away)
    match_mean_t1_ind = noramal_value(mean_t1_ind_scored_home, mean_t2_ind_conceded_away)
    match_mean_t2_ind = noramal_value(mean_t1_ind_conceded_home, mean_t2_ind_scored_away)


    print()
    print('CALC TOTAL:: ', match_mean_total)
    print('CALC 1HALF:: ', match_mean_1H)
    print('CALC 1HALF:: ', match_mean_2H)
    print()
    print('CALC TEAM1 IND. TOTAL::', match_mean_t1_ind,f'each: {mean_t1_ind_scored_home} {mean_t2_ind_conceded_away}')
    print('CALC TEAM2 IND. TOTAL::', match_mean_t2_ind, f'each: {mean_t1_ind_conceded_home} {mean_t2_ind_scored_away}')



    def bet_string(list):
        part1 = sorted(list)[:3]
        part2 = sorted(list)[-3:]
        return f'{part1}<{round(mean(list), 1)}>{part2}'

    print('1 HALF:: ')
    print('1T IND 1H SC:',bet_string(team1_scored_1h_home_ind))
    print('2T IND 1H CD:',bet_string(team2_conceded_1h_away_ind))
    print('1T IND 1H Ha:',bet_string(team1_handicap_1half_home))
    print('2T IND 1H Ha:',bet_string(team2_handicap_1half_away))
    print('1T TOTAL  1H:',bet_string(team1_1h_home_total))
    print('2T TOTAL  1H:',bet_string(team2_1h_away_total))
    print('FULLTIME:: ')
    print('1T IND FT SC:',bet_string(team1_scored_ind_home))
    print('2T IND FT CD:',bet_string(team2_conceded_ind_away))
    print('1T IND FT Ha:',bet_string(team1_handicap_total_home))
    print('2T IND FT Ha:',bet_string(team2_handicap_total_away))
    print('1T TOTAL FT:',bet_string(team1_total_home))
    print('2T TOTAL FT:',bet_string(team2_total_away))


    bet  = (title,' '.join(map(str,team1_name)),' '.join(map(str,team2_name)),
            "1 HALF TOTAL:: ",
            '1T IND 1H SC:' + bet_string(team1_scored_1h_home_ind),
            '2T IND 1H CD:' + bet_string(team2_conceded_1h_away_ind),
            '2T IND 1H SC:' + bet_string(team2_scored_1h_away_ind),
            '1T IND 1H CD:' + bet_string(team1_conceded_1h_home_ind),
            "HANDICAP 1HALF",
            '1T IND 1H Ha:' + bet_string(team1_handicap_1half_home),
            '2T IND 1H Ha:' + bet_string(team2_handicap_1half_away),
            '1T TOTAL  1H:' + bet_string(team1_1h_home_total),
            '2T TOTAL  1H:' + bet_string(team2_1h_away_total),
            'FULLTIME:: ',
            '1T IND FT SC:' + bet_string(team1_scored_ind_home),
            '2T IND FT CD:' + bet_string(team2_conceded_ind_away),
            '2T IND FT SC:' + bet_string(team2_scored_ind_away),
            '1T IND FT CD:' + bet_string(team1_conceded_ind_home),
            "HANDICAP FULLTIME",
            '1T IND FT Ha:' + bet_string(team1_handicap_total_home) ,
            '2T IND FT Ha:' + bet_string(team2_handicap_total_away) ,
            '1T TOTAL  FT:' + bet_string(team1_total_home) ,
            '2T TOTAL  FT:' + bet_string(team2_total_away)

                )

    bet_siska(bet)

for i in schedule:
    try:
        check_link(i)
    except:
        continue





