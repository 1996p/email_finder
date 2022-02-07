import re
import csv
import datetime
import requests
import json


def find_email(text: str):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', text)

    time_now = datetime.datetime.now()

    with open(f'{time_now.day}_{time_now.month}_{time_now.year}_emails.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for email in emails:
            if email[-1] + email[-2] == 'TR':
                email = email[:-2]
            writer.writerow(email.split())


def get_page(url):
    headers = {
        'accept': '*/*',
        'authorization': '',
        'user-agent': '',
        'referer': 'https://twitter.com/SendBeatsBot',
        'x-csrf-token': '',
        'x-guest-token': '',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'ru'
    }
    response = requests.get(url=url, headers=headers)

    data = json.loads(response.text)
    all_tweets = data['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']
    not_parsed_text = ''
    for tweet in all_tweets:
        try:
            not_parsed_text += tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
        except KeyError:
            pass
    return not_parsed_text

def main():
    text = get_page('https://twitter.com/i/api/graphql/cPBm-f7kzI0Z5-10CgivWw/UserTweets?variables={"userId":"845840682644193280","count":699,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":false,"__fs_interactive_text":false,"__fs_responsive_web_uc_gql_enabled":false,"__fs_dont_mention_me_view_api_enabled":false}')
    find_email(text=text)

if __name__ == '__main__':
    main()