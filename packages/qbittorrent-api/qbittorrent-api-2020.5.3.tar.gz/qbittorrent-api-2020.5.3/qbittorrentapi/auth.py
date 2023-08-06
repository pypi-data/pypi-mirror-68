import logging

from qbittorrentapi.request import RequestMixIn
from qbittorrentapi.helpers import suppress_context, APINames
from qbittorrentapi.decorators import login_required

from qbittorrentapi.exceptions import *


logger = logging.getLogger(__name__)


class AuthMixIn(RequestMixIn):
    @property
    def is_logged_in(self):
        return bool(self._SID)

    def auth_log_in(self, username='', password=''):
        """
        Log in to qBittorrent host.

        Exceptions:
            raise LoginFailed if credentials failed to log in
            raise Forbidden403Error if user user is banned

        :param username: user name for qBittorrent client
        :param password: password for qBittorrent client
        :return: None
        """
        if username != '':
            self.username = username
            assert password
            self._password = password

        try:
            self._initialize_context()

            response = self._post(_name=APINames.Authorization,
                                  _method='login',
                                  data={'username': self.username,
                                        'password': self._password}
                                  )
            self._SID = response.cookies['SID']
            logger.debug('Login successful for user "%s"' % self.username)
            logger.debug('SID: %s' % self._SID)

        except KeyError:
            logger.debug('Login failed for user "%s"' % self.username)
            raise suppress_context(LoginFailed('Login authorization failed for user "%s"' % self.username))

    @login_required
    def auth_log_out(self, **kwargs):
        """ Log out of qBittorrent client """
        self._get(_name=APINames.Authorization, _method='logout', **kwargs)
