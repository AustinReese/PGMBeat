from json import loads, load

class PgmWriteup:
    def __init__(self):
        self.data = load(open('seed_data/3.json', 'r'))
        self.table_lookups = {k: int(v) for k, v in dict(self.data[0]).items()}
        self.playerNameLookups = {}
        self.gameInfoLookups = {}
        self.teamSalaryLookups = {}
        self.teamIdenLookups = {}
        print(self.table_lookups)

    def writeIntro(self):
        with open("./context/README.txt", "w") as f:
            f.writelines("These files contain information about a simulated American Football league. The annual salary cap is $254 million dollars. Teams may not pay players in excess of this amount.")

    def writeTeamRatings(self):
        team_rating_lookups = [int(x) for x in self.data[self.table_lookups["TeamRating"]]]
        team_rating_writeup = ["This file contains team metric data.\n"]
        bad_skills = ["iden", "teamName", "teamIden"]
        for team_rating_lookup in team_rating_lookups:
            team_rating_object = self.data[team_rating_lookup]
            team_name = self.data[int(team_rating_object["teamName"])]
            self.teamIdenLookups[team_rating_object["teamIden"]] = team_name
            team_skills_string = ", ".join([f"{k}: {v}" for k, v in team_rating_object.items() if k not in bad_skills])
            team_rating_writeup.append(f"{team_name} team metrics: {team_skills_string}\n")

        with open("./context/teamMetrics.txt", "w") as f:
            f.writelines(team_rating_writeup)

    def lookupMetrics(self, object, metrics_to_lookup):
        for k, v in object.items():
            if k in metrics_to_lookup:
                object[k] = self.data[int(v)]

        return object

    def deleteMetrcis(self, object, metrics_to_delete):
        for metric in metrics_to_delete:
            del object[metric]

        return object

    def deleteZeroMetrics(self, object):
        metrics_to_delete = []
        for k, v in object.items():
            if v == 0:
                metrics_to_delete.append(k)

        for metric in metrics_to_delete:
            del object[metric]

        return object

    def parsePlayers(self, player_objects):
        metrics_to_lookup = ["iden", "forename", "surname", "position", "team", "draftTeam", "draftCollege", "draftDeclare", "skill", "injury", "award", "salary", "guarantee", "basePosition"]
        metrics_to_ignore = ["testVar", "appearance", "suspReason", "interviewFog", "playbook"]
        teams_to_ignore = ["Rookie", "Retired"]
        for player_object in player_objects:
            keys_to_delete = []
            player_object = self.lookupMetrics(player_object, metrics_to_lookup)

            if player_object["team"] in teams_to_ignore:
                continue

            metrics_to_ignore += [x for x in metrics_to_ignore if x in [k for k, v in player_object.items() if "Scout" in k]]

            player_object = self.deleteZeroMetrics(player_object)
            player_object = self.deleteMetrcis(player_object, metrics_to_ignore)

            self.playerNameLookups[player_object["iden"]] = f"{player_object["forename"]} {player_object["surname"]}"
            del player_object["iden"]

            if len(player_object["salary"]) > 0:
                if player_object["team"] not in self.teamSalaryLookups:
                    self.teamSalaryLookups[player_object["team"]] = int(player_object["salary"][0]) + int(player_object["guarantee"][0])
                else:
                    self.teamSalaryLookups[player_object["team"]] += int(player_object["salary"][0]) + int(player_object["guarantee"][0])
            else:
                if player_object["team"] not in self.teamSalaryLookups:
                    self.teamSalaryLookups[player_object["team"]] = 700000
                else:
                    self.teamSalaryLookups[player_object["team"]] += 700000

            player_object["award"] = [self.data[int(x)] for x in player_object["award"]]
            for i in range(len(player_object["award"])):
                player_object["award"][i] = {k: v for k, v in player_object["award"][i].items() if v != 0 and k not in ["iden", "playerIden", "playerPosition"]}
            player_object["salary"] = ["$" + str(x) for x in player_object["salary"]]
            player_object["guarantee"] = ["$" + str(x) for x in player_object["guarantee"]]

        return player_objects


    def writePlayers(self):
        player_lookups = [int(x) for x in self.data[self.table_lookups["PlayerNew"]]]
        player_objects = [self.data[x] for x in player_lookups]
        self.parsePlayers(player_objects)

        player_writeup = ["This file contains player information and ratings. The rating curRatingOVR indicates the player's current overall rating. If an item is not present it's because value is 0\n"]

        for player_object in player_objects:
            player_writeup_string = ", ".join([f"{k}: {v}" for k, v in player_object.items()])
            player_writeup_string += "\n"
            player_writeup.append(player_writeup_string)

        with open("./context/players.txt", "w") as f:
            f.writelines(player_writeup)

    def writeSeasonRecords(self):
        season_record_lookups = [int(x) for x in self.data[self.table_lookups["SeasonRecord"]]]
        metrics_to_lookup = ["teamName", "division"]
        metrics_to_ignore = ["iden", "teamIden"]
        season_recored_writeup = ["This file contains team records and statistics from the season.\n"]
        for season_record_lookup in season_record_lookups:
            season_record_object = self.data[season_record_lookup]

            for k, v in season_record_object.items():
                if k in metrics_to_lookup:
                    season_record_object[k] = self.data[int(v)]
            player_writeup_string = ", ".join([f"{k}: {v}" for k, v in season_record_object.items() if k not in metrics_to_ignore])
            player_writeup_string += "\n"
            season_recored_writeup.append(player_writeup_string)

        with open("./context/seasonRecords.txt", "w") as f:
            f.writelines(season_recored_writeup)

    def writeGameStats(self):
        game_stat_lookups = [int(x) for x in self.data[self.table_lookups["GameStat"]]]
        metrics_to_lookup = ["playerIden", "playerPos", "team", "oppo"]
        static_metrics = ["name", "playerPos", "team", "season"]
        metrics_to_ignore = ["iden", "gameIden", "complete", "iden", "playerIden", "complete"]
        game_stat_writeup = ["This file contains player statistics from all games this season. If an item is not present it's because the value is 0. Missing games indicates the player did not play.\n"]
        player_objects = {}
        for game_stat_lookup in game_stat_lookups:
            game_stat_object = self.data[game_stat_lookup]

            keys_to_delete = []
            for k, v in game_stat_object.items():
                if k in metrics_to_lookup:
                    game_stat_object[k] = self.data[int(v)]
                # Save space
                if v == 0:
                    keys_to_delete.append(k)


            for k in keys_to_delete:
                del game_stat_object[k]

            if len(keys_to_delete) == 45:
                continue

            game_stat_object["name"] = self.playerNameLookups[game_stat_object["playerIden"]]

            if game_stat_object["playerIden"] not in player_objects:
                player_objects[game_stat_object["playerIden"]] = {k: v for k, v in game_stat_object.items() if k in static_metrics}
                if "gamesPlayed" in game_stat_object and game_stat_object["gamesPlayed"] != 0:
                    player_objects[game_stat_object["playerIden"]]["final_stats"] = {k: v for k, v in game_stat_object.items() if k not in static_metrics and k not in metrics_to_ignore + ["oppo"]}
                    player_objects[game_stat_object["playerIden"]]["games"] = []
                else:
                    player_objects[game_stat_object["playerIden"]]["games"] = [{k: v for k, v in game_stat_object.items() if k not in static_metrics and k not in metrics_to_ignore}]
            else:
                if "gamesPlayed" in game_stat_object and game_stat_object["gamesPlayed"] != 0:
                    player_objects[game_stat_object["playerIden"]]["final_stats"] = {k: v for k, v in game_stat_object.items() if k not in static_metrics and k not in metrics_to_ignore + ["oppo"]}
                else:
                    player_objects[game_stat_object["playerIden"]]["games"].append({k: v for k, v in game_stat_object.items() if k not in static_metrics and k not in metrics_to_ignore})

        for iden, player_object in player_objects.items():
            game_stat_string = ", ".join([f"{k}: {v}" for k, v in player_object.items() if k in static_metrics])
            game_stat_string += ", games: "
            for game in player_object["games"]:
                game_stat_string += ", ".join([f"{k}: {v}" for k, v in game.items()])
                game_stat_string += " | "
            game_stat_string += "Season total stats: "
            game_stat_string += ", ".join([f"{k}: {v}" for k, v in player_object["final_stats"].items()])
            game_stat_string += "\n"
            game_stat_writeup.append(game_stat_string)

        with open("./context/gameStats.txt", "w") as f:
            f.writelines(game_stat_writeup)

    def writeGames(self):
        game_lookups = [int(x) for x in self.data[self.table_lookups["GameNew"]]]
        game_writeup = ["This file contains game information.\n"]
        metrics_to_lookup = ["teamAway", "teamHome", "awayBox", "homeBox", "iden"]
        bad_metrics = ["playoffConf", "user", "complete", "gameLog", "play"]
        for game_lookup in game_lookups:
            game_object = self.data[game_lookup]

            keys_to_delete = []
            for k, v in game_object.items():
                if k in metrics_to_lookup:
                    game_object[k] = self.data[int(v)]
                # Save space
                if v == 0:
                    keys_to_delete.append(k)

            for k in keys_to_delete:
                del game_object[k]

            self.gameInfoLookups[game_object["iden"]] = game_object["week"]

            del game_object["iden"]

            game_string = ", ".join([f"{k}: {v}" for k, v in game_object.items() if k not in bad_metrics])
            game_string += "\n"
            game_writeup.append(game_string)

        with open("./context/games.txt", "w") as f:
            f.writelines(game_writeup)

    def writeGameLogs(self):
        game_log_lookups = [int(x) for x in self.data[self.table_lookups["GameLogNew"]]]
        bad_metrics = ["playerStats", "playerIden", "iden", "playNum", "logType"]
        game_log_writeup = ["This file contains game logs.\n"]
        for game_log_lookup in game_log_lookups:
            game_log_object = self.data[game_log_lookup]

            for metric in bad_metrics:
                del game_log_object[metric]

            for k, v in game_log_object.items():
                game_log_object[k] = self.data[int(v)]
            game_log_object["week"] = self.gameInfoLookups[game_log_object["gameIden"]]
            del game_log_object["gameIden"]

            game_log_string = ", ".join([f"{k}: {v}" for k, v in game_log_object.items() if k not in bad_metrics])
            game_log_string += "\n"
            game_log_writeup.append(game_log_string)

        with open("./context/gameLogs.txt", "w") as f:
            f.writelines(game_log_writeup)

    def writeTeamInfo(self):
        team_info_lookups = [int(x) for x in self.data[self.table_lookups["TeamNew"]]]
        bad_metrics = ["iden"]
        bad_season_record_metrics = ['iden', 'teamIden','teamName', 'division']
        team_info_writeup = ["This file contains game logs.\n"]
        metrics_to_lookup = ["name", "division", "color", "seasonRecord", "rating"]
        for team_info_lookup in team_info_lookups:
            team_info_object = self.data[team_info_lookup]
            for metric in bad_metrics:
                del team_info_object[metric]

            keys_to_delete = []
            for k, v in team_info_object.items():
                if k in metrics_to_lookup:
                    team_info_object[k] = self.data[int(v)]
                    if k == "seasonRecord":
                        team_info_object[k] = [self.data[int(x)] for x in team_info_object[k]]

                        for bad_season_record_metric in bad_season_record_metrics:
                            for i in range(len(team_info_object[k])):
                                del team_info_object[k][i][bad_season_record_metric]
                # Save space
                if v == 0:
                    keys_to_delete.append(k)

            for k in keys_to_delete:
                del team_info_object[k]

            team_info_object["totalSalarySpent"] = self.teamSalaryLookups[team_info_object["name"]]
            team_info_string = ", ".join([f"{k}: {v}" for k, v in team_info_object.items() if k not in bad_metrics])
            team_info_string += "\n"
            team_info_writeup.append(team_info_string)

        with open("./context/teamInfo.txt", "w") as f:
            f.writelines(team_info_writeup)
        
    def writeTrades(self):
        trade_lookups = [int(x) for x in self.data[self.table_lookups["OfferNew"]]]
        trade_writeup = ["This file contains trades made during the season.\n"]
        bad_metrics = ["iden", "complete"]
        metrics_to_lookup = ["offerTeam", "offerTeamPlayers", "offerTeamPicks", "recTeam", "recTeamPicks", "recTeamPlayers"]
        metrics_to_super_parse = ["offerTeamPlayers", "offerTeamPicks", "recTeamPlayers", "recTeamPicks"]
        for trade_lookup in trade_lookups:
            trade_object = self.data[trade_lookup]
            for k, v in trade_object.items():
                if k in metrics_to_lookup:
                    trade_object[k] = self.data[int(v)]
                    if k in metrics_to_super_parse:
                        if type(trade_object[k]) == type([]):
                            trade_object[k] = [self.data[int(x)] for x in trade_object[k]]
                            for i in range(len(trade_object[k])):
                                if "Picks" in k: # wild shit here sorry
                                    if type(trade_object[k][i]["origTmIden"]) == type(1):
                                        trade_object[k][i]["origTmIden"] = self.data[int(trade_object[k][i]["origTmIden"])]
                                        trade_object[k][i]["curTmIden"] = self.data[int(trade_object[k][i]["curTmIden"])]
                                    elif len(trade_object[k][i]["origTmIden"]) > 3:
                                        trade_object[k][i]["origTmIden"] = self.teamIdenLookups[trade_object[k][i]["origTmIden"]]
                                        trade_object[k][i]["curTmIden"] = self.teamIdenLookups[trade_object[k][i]["curTmIden"]]

                                    trade_object[k][i] = {k: v for k, v in trade_object[k][i].items() if k not in ["iden", "complete"]}

                                else:
                                    trade_object[k][i] = self.parsePlayers([trade_object[k][i]])[0]

            trade_string = ", ".join([f"{k}: {v}" for k, v in trade_object.items() if k not in bad_metrics])
            trade_string += "\n"
            trade_writeup.append(trade_string)

        with open("./context/trades.txt", "w") as f:
            f.writelines(trade_writeup)

def main():
    print("Writing...")
    pgmWriteup = PgmWriteup()
    pgmWriteup.writeIntro()
    pgmWriteup.writeTeamRatings()
    pgmWriteup.writePlayers()
    pgmWriteup.writeSeasonRecords()
    pgmWriteup.writeGameStats()
    pgmWriteup.writeGames()
    pgmWriteup.writeGameLogs()
    pgmWriteup.writeTeamInfo()
    pgmWriteup.writeTrades()
    print("Written to ./context/")

if __name__ == "__main__":
    main()