import tweepy
import config

#initializing the client 

def getClient():
  client=tweepy.Client(bearer_token=config.BEARER_TOKEN,
                      consumer_key=config.API_KEY, 
                      consumer_secret=config.API_SECRET, 
                      access_token=config.ACCESS_TOKEN,
                        access_token_secret=config.ACCESS_TOKEN_SECRET,
                    )

  return client


def getUserInfo():
    client=getClient()
    user=client.get_user(username="username_here")
    
    return user.data.id

user=getUserInfo()

print(user)
   


