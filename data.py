from fifa_rankings import FIFA_RANKINGS

teams = [
  "Qatar", "Ecuador", "Senegal", "Netherlands",
  "England", "Iran", "United States", "Wales",
  "Argentina", "Saudi Arabia", "Mexico", "Poland",
  "France", "Australia", "Denmark", "Tunisia",
  "Spain", "Costa Rica", "Germany", "Japan",
  "Belgium", "Canada", "Morocco", "Croatia",
  "Brazil", "Serbia", "Switzerland", "Cameroon",
  "Portugal", "Ghana", "Uruguay", "South Korea"
]

def elo_ranking(team):
  return list(filter(lambda x: x['name'] == team, FIFA_RANKINGS))[0]