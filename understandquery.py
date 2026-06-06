
#Function which will tell our model what actually to do
def UnderStandQuery(user_inp):
    if "map" in user_inp.split():
        return "open map"
    elif "open" in user_inp.split():
        word_list = ["what", "how", "open", "are", "you", "am", "can", "me", "i", "will",'please', "for", "and", "hey", "buddy", "ok", "me?", "and", "also"]
        app = [i for i in user_inp.split() if i not in word_list and i != "open"]

        return app
    elif "play" in user_inp.split():
        return "play song"

    else:
        return user_inp
    
