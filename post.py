from github import Github
from datetime import datetime, timedelta
from twitter import Twitter, OAuth


DEFAULT_PARAMETERS = {
    'GITHUB_TOKEN': None,                       # GitHub authirization token
    'GITHUB_ORG_NAME': None,                    # Name (login) of organization
    'TW_CONSUMER_KEY': None,                    # Twitter application key
    'TW_CONSUMER_SECRET': None,                 # Twitter application secret
    'TW_OAUTH_TOKEN': None,                     # Twitter Oauth token
    'TW_OAUTH_SECRET': None,                    # Twitter Oauth secret
    'STATISTIC_INTERVAL': timedelta(days=1),    # Statistics interval
    'MIN_COMMITS_COUNT': 1,                     # Minimum commits count required to send twit
    'TWIT_TEMPLATE': 'Today commits count by'   # Twit template
                     ' {company} team - {commits}'
                     '. Lines added - {lines_added}'
}

def get_stats(token, org_name, stat_interval):
    """ Get github statistic for specified organization """
    gh_api = Github(token, timeout=100)
    gh_user = gh_api.get_user()
    for gh_org in gh_user.get_orgs():
        if gh_org.login == org_name:
            break
    else:
        raise ValueError('Organization with name `%s` was not found. User needs to be a member of it.' %
                        org_name)

    # Calculate statistic
    total_commits_count = 0
    total_lines_added = 0
    total_lines_deleted = 0
    total_lines = 0
    since = datetime.now() - stat_interval
    for repo in gh_org.get_repos():
        for commit in repo.get_commits(since=since):
            total_commits_count += 1
            stats = commit.stats
            total_lines_added += stats.additions
            total_lines_deleted += stats.deletions
            total_lines += stats.total

    return {
        'company': gh_org.name,
        'commits': total_commits_count,
        'lines_added': total_lines_added,
        'lines_deleted': total_lines_deleted,
        'lines': total_lines,
    }


def render_template(template, data):
    """ Render template with python `str.format` """
    return template.format(**data)


def send_twit(oauth_token, oauth_secret, consumer_key, consumer_secret, twit_body):
    """ Send twit """
    twitter_client = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    return twitter_client.statuses.update(status=twit_body)


if __name__ == '__main__':

    try:
        import settings
    except ImportError:
        raise ImportError('You need to create settings.py.')

    # Get user defined params
    user_defined_params = {}
    for attr in dir(settings):
        if attr not in DEFAULT_PARAMETERS:
            continue
        user_defined_params[attr] = getattr(settings, attr)

    PARAMETERS = dict(DEFAULT_PARAMETERS.items() + user_defined_params.items())

    # Check required paramaeters
    if None in PARAMETERS.values():
        missed_params = [key for key, val in PARAMETERS.items() if val is None]
        missed_params_joined = ', '.join(missed_params)
        raise ValueError('You need to specify (in settings.py) following required parameters: %s.'
                        % missed_params_joined)

    # Run!
    data = get_stats(PARAMETERS['GITHUB_TOKEN'], PARAMETERS['GITHUB_ORG_NAME'], 
                PARAMETERS['STATISTIC_INTERVAL'])

    # Check minimum comments restriction
    if data['commits'] >= PARAMETERS['MIN_COMMITS_COUNT']:
        twit_body = render_template(PARAMETERS['TWIT_TEMPLATE'], data)
        send_twit(PARAMETERS['TW_OAUTH_TOKEN'], PARAMETERS['TW_OAUTH_SECRET'], 
                  PARAMETERS['TW_CONSUMER_KEY'], PARAMETERS['TW_CONSUMER_SECRET'], 
                  twit_body)