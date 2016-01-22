import praw

class WeeklyChallenges(object):
"""
Contains the challenges for each week

Attributes:
    index (int): The weeks index, the main way of keeping track of challenges
        instead of using dates
    challenges (dict): dict of {challenge : submission}
"""
    def __init__(self, index):
        self.index = index
        self.challenges = None
        self.setup_challenge()       

    def setup_challenge(self):
        challenges = ['easy', 'intermediate', 'hard', 'mini']
        self.challenges = collections.OrderedDict((challenge, '**-**') for challenge in challenges)

    def add_challenge(self, challenge):
        """
        Args:
            challenge (submission):
        """
        title = challenge.title
        if '[Easy]' in title:
            self.challenges['easy'] = challenge
        elif '[Intermediate]' in title:
            self.challenges['intermediate'] = challenge
        elif '[Hard]' in title or '[Difficult]' in title:
            self.challenges['hard'] = challenge
        elif 'Mini' in title and self.mini is None:
            self.challenges['mini'] = challenge

    def __repr__(self):
        result = ""
        for challenge in self.challenges:
            post = self.challenges[challenge]
            if post != '**-**':
                result += '| [{}]({})'.format(post.title, post.url)
            else:
                result += '| ' + post
        result += ' |\n'

        return result
class DailyProgrammer(object):
"""
Gets n submissions from the 'hot' tab of /r/DailyProgrammer
"""
    def __init__(self):
        self.user_agent = 'daily programmer scraper'
        self.reddit = praw.Reddit(user_agent=self.user_agent)
        self.subreddit = self.reddit.get_subreddit('DailyProgrammer')
        self.get_posts()

    def get_posts(self):
        posts = self.subreddit.get_hot(limit=100) #Takes a while because of the limit of 100 fetches at a time
        posts_by_index = {}
        for post in posts:
            title = post.title
            if '] challenge #' not in title.lower():
                continue
            title = title.split('#')
            index = title[1].strip().split(' ')
            index = int(index[0])

            if index not in posts_by_index:
                posts_by_index[index] = WeeklyChallenges(index)
                posts_by_index[index].add_challenge(post)                
            else:
                posts_by_index[index].add_challenge(post)
        self.posts_by_index = posts_by_index

    def generate_header(self):
        indices = self.posts_by_index.keys()
        last_index = indices[len(indices) - 1]

    def get_challenges_by_indices(self, *indices):
        return [self.posts_by_index[index] for index in indices]

    def display_last_n_weeks(self, n):
        header = "Easy | Intermediate | Hard | Weekly/Bonus\n-------------|-------------|-------------|-------------\n"
        result = header
        weeks = sorted(self.posts_by_index.keys())[::-1]
        weeks = weeks[:n]
        for week in weeks:
            result += self.posts_by_index[week].__repr__()

        return result

dp = DailyProgrammer()
res = dp.display_last_n_weeks(15)