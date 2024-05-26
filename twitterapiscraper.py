import yaml

from twitter.scraper import Scraper

class TwitterScraper:

    def __init__(self, email: str, username: str, password: str):
        # https://github.com/trevorhobenshield/twitter-api-client/blob/main/readme.md
        self.scraper = Scraper(email, username, password)

    def scrape(self, tweet_id: int) -> list:
        tweets_data = self.scraper.tweets_details([tweet_id])
        tweets = TwitterScraper._extract_tweets(tweets_data)
        tree = TwitterScraper._build_tweet_tree(tweets.copy())
        return TwitterScraper._clean_tweet_tree(tree)

    @staticmethod
    def _extract_tweets(tweets_data: dict):
        tweets = []
        for tweet_data in tweets_data:
            for instruction in tweet_data['data']['threaded_conversation_with_injections_v2']['instructions']:
                if instruction['type'] != 'TimelineAddEntries':
                    continue
                for entry in instruction['entries']:
                    if entry['content']['entryType'] == 'TimelineTimelineItem' and entry['content']['itemContent']['itemType'] == 'TimelineTweet':
                        result = entry['content']['itemContent']['tweet_results']['result']
                        tweets.append({
                            'handle': result['core']['user_results']['result']['legacy']['screen_name'],
                            'text': result['legacy']['full_text'],
                            'id': result['legacy']['id_str'],
                            'replyToId': result['legacy']['in_reply_to_status_id_str'] if 'in_reply_to_status_id_str' in result['legacy'].keys() else None
                        })
                    if entry['content']['entryType'] == 'TimelineTimelineModule':
                        for i in entry['content']['items']:
                            if i['item']['itemContent']['itemType'] == 'TimelineTweet':
                                result = i['item']['itemContent']['tweet_results']['result']
                                tweets.append({
                                    'handle': result['core']['user_results']['result']['legacy']['screen_name'],
                                    'text': result['legacy']['full_text'],
                                    'id': result['legacy']['id_str'],
                                    'replyToId': result['legacy']['in_reply_to_status_id_str'] if 'in_reply_to_status_id_str' in result['legacy'].keys() else None
                                })
        return tweets

    @staticmethod
    def _build_tweet_tree(tweets: list, tree: dict = None) -> dict:
        if tree is None:
            tree = {}
            for i in tweets.copy():
                if i['replyToId'] is None:
                    tree[i['id']] = i
                    tree[i['id']]['children'] = {}
                    tweets.remove(i)
        for i in tweets.copy():
            if i['replyToId'] in tree.keys():
                i['children'] = {}
                tree[i['replyToId']]['children'][i['id']] = i
                tweets.remove(i)
        for child in tree.values():
            TwitterScraper._build_tweet_tree(tweets, child['children'])
        return tree

    @staticmethod
    def _clean_tweet_tree(tree: dict) -> list:
        l = list(tree.values())
        for i in l:
            children = i.pop('children')
            del i['replyToId']
            i['children'] = TwitterScraper._clean_tweet_tree(children)
        return l

    @staticmethod
    def _strip_ids(l: list) -> list:
        for i in l:
            del i['id']
            TwitterScraper._strip_ids(i['children'])

    @staticmethod
    def clean_tree_to_yaml(cleaned: list) -> str:
        cleaned = cleaned.copy()
        TwitterScraper._strip_ids(cleaned)
        return yaml.dump(cleaned, indent=2, sort_keys=False)
