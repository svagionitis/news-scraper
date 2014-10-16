import urllib
import random

class ScraperOpener(urllib.FancyURLopener):
    _user_agent_list = []

    def set_user_agent(self, user_agent):
        """ Set the user agent
        """
        self.version = user_agent

    def load_user_agents(self, filename):
        """ Load user agents from a file to a list
        """
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line:
                    self._user_agent_list.append(line)

    def set_random_user_agent(self, filename):
        """ Set the user agent randomly from a file
        """
        # If the user agent list is populated, then get the random one
        # Else load the user agents from the file first and then choose one randomly
        if self._user_agent_list:
            set_user_agent(random.choice(self._user_agent_list))
        else:
            self.load_user_agents(filename)
            self.set_user_agent(random.choice(self._user_agent_list))


if __name__ == '__main__':

    opener = ScraperOpener()

    print('User agent before change - %s' % opener.version)

    opener.set_user_agent('Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')

    print('User agent after change - %s' % opener.version)

    opener.set_random_user_agent('user-agents.txt')

    print('User agent after random change - %s' % opener.version)
