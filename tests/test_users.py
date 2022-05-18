import secrets
from unittest import IsolatedAsyncioTestCase
import aiobastion
import random
import tests
from aiobastion import CyberarkAPIException, CyberarkException, AiobastionException


class TestUsers(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.vault = aiobastion.EPV(tests.CONFIG)
        await self.vault.login()
        self.api_user = "bastion_test_usr"
        self.test_safe = "sample-it-dept"
        self.test_usr = "bastion_std_usr"

    async def get_random_account(self, n=1):
        accounts = await self.vault.account.search_account_by(
            safe=self.test_safe
        )
        self.assertGreaterEqual(len(accounts), 1)
        if n == 1:
            return random.choice(accounts)
        else:
            return random.choices(accounts, k=n)

    async def test_list(self):
        req = await self.vault.user.list()
        self.assertIn(self.api_user, req)
        self.assertIn(self.test_usr, req)


    async def test_get_users(self):
        req = await self.vault.user.list()
        self.assertIn(self.api_user, req)
        self.assertIn(self.test_usr, req)

    async def test_get_user_id(self):
        req = await self.vault.user.get_id(self.api_user)
        self.assertIsInstance(req, int)

        with self.assertRaises(AiobastionException):
            await self.vault.user.get_id("vdsv,pnovdope,vb")

    async def test_exists(self):
        self.assertTrue(await self.vault.user.exists(self.api_user))
        self.assertFalse(await self.vault.user.exists("zvnlkvvenpoop"))

    async def test_details(self):
        req = await self.vault.user.details(self.api_user)
        self.assertEqual(req["username"], self.api_user)

    async def test_groups(self):
        req = await self.vault.user.groups(self.api_user)
        self.assertIn("Vault Admins", req)

    async def test_add_ssh_key(self):
        random_key = secrets.token_urlsafe(88)
        req = await self.vault.user.add_ssh_key(self.test_usr, random_key)
        self.assertIn("KeyID", req)
        new_key = req["KeyID"]

        req = await self.vault.user.get_ssh_keys(self.test_usr)
        all_key_id = [k["KeyID"] for k in req]
        self.assertIn(new_key, all_key_id)

        await self.vault.user.del_ssh_key(self.test_usr, new_key)
        #check
        req = await self.vault.user.get_ssh_keys(self.test_usr)
        all_key_id = [k["KeyID"] for k in req]
        self.assertNotIn(new_key, all_key_id)

    async def test_get_ssh_keys(self):
        req = await self.vault.user.get_ssh_keys(self.test_usr)
        self.assertIsInstance(req, list)

    async def test_del_all_ssh_keys(self):
        for i in range(8):
            random_key = secrets.token_urlsafe(88)
            await self.vault.user.add_ssh_key(self.test_usr, random_key)
        req = await self.vault.user.get_ssh_keys(self.test_usr)
        self.assertGreaterEqual(len(req), 8)

        await self.vault.user.del_all_ssh_keys(self.test_usr)
        req = await self.vault.user.get_ssh_keys(self.test_usr)
        self.assertEqual(len(req), 0)

    async def test_list_group(self):
        req = await self.vault.group.list()
        self.assertIn("Vault Admins", req)

        req = await self.vault.group.list(pattern="Admins")
        self.assertIn("Vault Admins", req)

        req = await self.vault.group.list(group_type="Vault")
        self.assertIn("Vault Admins", req)

    async def test_get_id_group(self):
        req = await self.vault.group.get_id("Vault Admins")
        self.assertIsInstance(req, int)

        with self.assertRaises(AiobastionException):
            req = await self.vault.group.get_id("Les Poneys")

    async def test_add_group(self):
        new_group_name = "new_group_test"
        await self.vault.group.add(new_group_name, "New awesome group")
        req = await self.vault.group.list()
        self.assertIn(new_group_name, req)

        await self.vault.group.delete(new_group_name)
        req = await self.vault.group.list()
        self.assertNotIn(new_group_name, req)



