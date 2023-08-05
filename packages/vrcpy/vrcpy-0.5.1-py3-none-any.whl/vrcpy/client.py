from vrcpy.request import *
from vrcpy.errors import *
from vrcpy import objects
from vrcpy import aobjects
import base64
import time
import json

class Client:
    def fetch_me(self):
        '''
            Simply returns newest version of CurrentUser
        '''

        resp = self.api.call("/auth/user")
        self._raise_for_status(resp)

        self.me = objects.CurrentUser(self, resp["data"])
        return self.me

    def fetch_full_friends(self):
        '''
        Returns list of Users
        This function uses possibly lot of calls, use with caution
        '''

        self.fetch_me()
        friends = []

        # Get friends
        for friend in self.me.friends:
            time.sleep(0)
            resp = self.api.call("/users/"+friend)
            try:
                self._raise_for_status(resp)
            except NotFoundError:
                # User no longer exists
                continue

            friends.append(objects.User(self, resp))

        return friends

    def fetch_friends(self):
        '''
        Returns list of LimitedUsers
        '''

        self.fetch_me()
        friends = []

        # Get all pages of friends if > 100
        for offset in range(0, len(self.me.friends), 100):
            resp = self.api.call("/auth/user/friends", json={"offset": offset, "offline": True})
            self._raise_for_status(resp)

            for friend in resp["data"]:
                friends.append(objects.LimitedUser(self, friend))

        for offset in range(0, len(self.me.friends), 100):
            resp = self.api.call("/auth/user/friends", json={"offset": offset, "offline": False})
            self._raise_for_status(resp)

            for friend in resp["data"]:
                friends.append(objects.LimitedUser(self, friend))

        return friends

    def fetch_avatar(self, id):
        '''
            ID is the AvatarId of the avatar
            Returns Avatar object
        '''

        resp = self.api.call("/avatars/"+id)
        self._raise_for_status(resp)

        return objects.Avatar(self, resp["data"])

    def fetch_user_by_id(self, id):
        '''
        Returns User or FriendUser
            id, string The users id
        '''

        resp = self.api.call("/users/"+id)
        self._raise_for_status(resp)

        return objects.User(self, resp["data"])

    def logout(self):
        self.api.new_session()
        self.loggedIn = False

    def login(self, username, password):
        '''
            Used to initialize the client for use
        '''
        if self.loggedIn: raise AlreadyLoggedInError("Client is already logged in")

        auth = username+":"+password
        auth = str(base64.b64encode(auth.encode()))[2:-1]

        resp = self.api.call("/auth/user", headers={"Authorization": "Basic "+auth}, no_auth=True)
        self._raise_for_status(resp)

        self.api.set_auth(auth)
        self.me = objects.CurrentUser(self, resp["data"])
        self.loggedIn = True

    def _raise_for_status(self, resp):
        if resp["status"] == 401: raise IncorrectLoginError(resp["data"]["error"]["message"])
        if resp["status"] == 404:
            if type(resp["data"]) == bytes:
                raise NotFoundError(json.loads(resp["data"].decode()))
            raise NotFoundError(resp["data"]["error"]["message"])
        if resp["status"] != 200: raise GeneralError("Unhandled error occured: "+str(resp["data"]))
        if "requiresTwoFactorAuth" in resp["data"]: raise TwoFactorAuthNotSupportedError("2FA is not supported yet.")

    def __init__(self):
        self.api = Call()
        self.loggedIn = False
        self.me = None

class AClient(Client):
    async def fetch_me(self):
        '''
            Simply returns newest version of CurrentUser
        '''
        resp = await self.api.call("/auth/user")
        self._raise_for_status(resp)

        self.me = aobjects.CurrentUser(self, resp["data"])
        return self.me

    async def fetch_full_friends(self):
        '''
        Returns list of Users
        This function uses possibly lot of calls, use with caution
        '''

        await self.fetch_me()
        friends = []

        # Get friends
        for friend in self.me.friends:
            await asyncio.sleep(0)
            resp = await self.api.call("/users/"+friend)
            try:
                self._raise_for_status(resp)
            except NotFoundError:
                # User no longer exists
                continue

            friends.append(aobjects.User(self, resp))

        return friends

    async def fetch_friends(self):
        '''
        Returns list of LimitedUsers
        '''

        await self.fetch_me()
        friends = []

        # Get all pages of friends if > 100
        for offset in range(0, len(self.me.friends), 100):
            resp = await self.api.call("/auth/user/friends", json={"offset": offset, "offline": True})
            self._raise_for_status(resp)

            for friend in resp["data"]:
                friends.append(aobjects.LimitedUser(self, friend))

        for offset in range(0, len(self.me.friends), 100):
            resp = await self.api.call("/auth/user/friends", json={"offset": offset, "offline": False})
            self._raise_for_status(resp)

            for friend in resp["data"]:
                friends.append(aobjects.LimitedUser(self, friend))

        return friends

    async def fetch_avatar(self, id):
        '''
            ID is the AvatarId of the avatar
            Returns Avatar object
        '''

        resp = await self.api.call("/avatars/"+id)
        self._raise_for_status(resp)

        return aobjects.Avatar(self, resp["data"])

    async def fetch_user_by_id(self, id):
        '''
        Returns User or FriendUser
            id, string The users id
        '''

        resp = await self.api.call("/users/"+id)
        self._raise_for_status(resp)

        return objects.User(self, resp["data"])

    async def login(self, username, password):
        '''
            Used to initialize the client for use
        '''
        if self.loggedIn: raise AlreadyLoggedInError("Client is already logged in")

        auth = username+":"+password
        auth = str(base64.b64encode(auth.encode()))[2:-1]

        resp = await self.api.call("/auth/user", headers={"Authorization": "Basic "+auth}, no_auth=True)
        self._raise_for_status(resp)

        self.api.openSession(auth)
        self.me = aobjects.CurrentUser(self, resp["data"])
        self.loggedIn = True

    async def logout(self):
        await self.api.closeSession()
        await asyncio.sleep(0)

        self.api = ACall()
        self.loggedIn = False

    def __init__(self):
        super().__init__()

        self.api = ACall()
        self.loggedIn = False
        self.me = None
