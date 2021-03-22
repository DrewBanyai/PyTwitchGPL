#!/usr/bin/env python3
import requests
import re
import json

TWITCH_USER = "drewthebear"

# Fetch client-id
homepage = requests.get("https://www.twitch.tv").text
client_id = re.search('"Client-ID" ?: ?"(.*?)"', homepage).group(1)



def gqlQuery(query):
    global client_id
    return requests.post("https://gql.twitch.tv/gql", data = json.dumps([{"query": query}]), headers = {"Client-ID": client_id},).json()



def get_top_game_clips(gamename):
    return gqlQuery('query query { game(name: "' + gamename + '") { name followersCount viewersCount clips(criteria: { period: LAST_MONTH }) { edges { node { id title viewCount createdAt durationSeconds curator { login } broadcaster { login } } } } videos(sort: VIEWS) { edges { node { id creator { login } title viewCount createdAt lengthSeconds broadcastType } } } } }')



def get_top_live_streams():
    respJSON = gqlQuery('query { streams(first: 25) { edges { node { id title viewersCount broadcaster { displayName } game { name } } } } }')

    streamsJSON = respJSON[0]["data"]["streams"]["edges"]
    liveStreamNames = []

    for s in streamsJSON:
        liveStreamNames.append(s["node"]["title"])

    return liveStreamNames



def get_top_100_game_streams(gamename):
    respJSON = gqlQuery('query { game(name: "' + gamename + '") { streams(first: 100) { edges { node { broadcaster { broadcastSettings { title } } } } } } }')

    streamsJSON = respJSON[0]["data"]["game"]["streams"]["edges"]
    liveStreamNames = []

    for s in streamsJSON:
        liveStreamNames.append(s["node"]["broadcaster"]["broadcastSettings"]["title"])

    return liveStreamNames



def get_user_data(username):
    return gqlQuery('query { user(login: "' + username + '") { id login displayName followers { totalCount } description createdAt roles { isAffiliate isPartner } stream { id title type viewersCount createdAt game { name } } } }')



def get_first_100_followers(username):
    respJson = gqlQuery('query { user(login: "' + username + '") { followers(first:100) { totalCount edges { node { displayName } } } } }')

    followers = []
    followersJSON = respJson[0]["data"]["user"]["followers"]["edges"]
    for f in followersJSON:
        followers.append(f["node"]["displayName"])

    return followers



def get_user_sub_levels_and_emotes(username):
    return gqlQuery('query { user(login: "' + username + '") { subscriptionProducts { id name displayName price tier hasAdFree hasFastChat hasSubOnlyChat hasSubonlyVideoArchive interval { duration unit } emoteSetID emotes { id state text token } } } }')



def get_cheer_badges_and_cheermotes(username):
    return gqlQuery('query { user(login: "' + username + '") { cheer { availableBadges { title description clickURL imageURL } emotes { id prefix type tiers { bits images { id theme isAnimated dpiScale url } } } } } }')



def get_user_mods(username):
    respJSON = gqlQuery('query { user(login: "' + username + '") { mods { edges { node { login } } } } }')

    modsListJSON = respJSON[0]["data"]["user"]["mods"]["edges"]
    modsList = []
    for x in modsListJSON:
        modsList.append(x["node"]["login"])

    return modsList



def get_current_stream_video_data(username):
    return gqlQuery('query { user(login: "' + username + '") { stream { averageFPS bitrate broadcasterSoftware codec height width } } }')



def get_current_user_hosting(username):
    return gqlQuery('query { user(login: "' + username + '") { hosting { login } } }')



def GQL_Test():
    global TWITCH_USER

    #  Grab the user data for TWITCH_USER
    print("Grabbing user data for " + TWITCH_USER + "...")
    user_data = get_user_data(TWITCH_USER)
    print(user_data)
    print("")
    
    #  Display specific information from the payload
    print("TWITCH USER: " + str(user_data[0]["data"]["user"]["displayName"]))
    print("FOLLOWER COUNT: " + str(user_data[0]["data"]["user"]["followers"]["totalCount"]))
    print("")

    #  Display the first 100 followers on an account
    print("USER FIRST 100 FOLLOWERS (" + TWITCH_USER + "):")
    print(get_first_100_followers(TWITCH_USER))
    print("")

    #  Display the current top live streams
    print(get_top_live_streams())
    print("")

    #  Display the current top 100 game streams for a certain game
    print(get_top_100_game_streams("Teamfight Tactics"))
    print("")

    #  Display a user's sub levels and emotes
    print(get_user_sub_levels_and_emotes(TWITCH_USER))
    print("")

    #  Display a user's cheer badges and cheermotes (warning: LONG)
    print(get_cheer_badges_and_cheermotes(TWITCH_USER))
    print("")

    #  Display the list of a user's mods
    print(get_user_mods(TWITCH_USER))
    print("")

    #  Display the data for the current stream of a user
    print(get_current_stream_video_data(TWITCH_USER))
    print("")

    #  Display who a user is currently hosting
    print(get_current_user_hosting(TWITCH_USER))
    print("")

##  START PROGRAM
GQL_Test()