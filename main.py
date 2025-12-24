from follows import follow_people
from posts import post_tweet

def run():
    print(" Automation started")

    post_tweet()        
    follow_people()     

    print(" Automation finished")

if __name__ == "__main__":
    run()
