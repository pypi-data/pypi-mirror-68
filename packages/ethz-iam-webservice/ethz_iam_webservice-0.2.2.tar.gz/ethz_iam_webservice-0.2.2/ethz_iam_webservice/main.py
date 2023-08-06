import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse, urljoin, quote
import os
import json
import re
import click

# display messages when in a interactive context (IPython or Jupyter)
try:
    get_ipython()
except Exception:
    VERBOSE = False
else:
    VERBOSE = True


class ETH_IAM_conn():
    def __init__(self, admin_username, admin_password, hostname, endpoint_base):
        self._admin_username = admin_username
        self._admin_password = admin_password
        self.hostname = hostname
        self.endpoint_base = endpoint_base
        self.verify_certificates = True
        self.timeout=600

    def _delete_request(self, endpoint):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.delete(
            full_url,
            headers={'Accept': 'application/json'},
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _post_request(self, endpoint, body):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.post(
            full_url,
            json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _put_request(self, endpoint, body):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.put(
            full_url,
            json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _get_request(self, endpoint):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.get(
            full_url,
            headers={'Accept': 'application/json'},
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp


    def new_person(self, firstname, lastname):
        raise Exception("not implemented yet")
        return Person(conn=self, firstname=firstname, lastname=lastname)

    
    def get_person(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = '/usermgr/person/{}'.format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = '/usermgr/person?{}'.format(args)
        else:
            raise ValueError("please provide an identifier")

        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Person(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def get_user(self, identifier):
        endpoint = '/usermgr/user/{}'.format(identifier)
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return User(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def new_group(self, name, description, admingroup, targets, members=None):
        """
        name=<Group Name>
        description=<what is the purpose of this group>
        admingroup=<Admin Group>
        targets=['AD', 'LDAPS'] -- specify at least one target system
        members=['username1', 'username2']
        """
        if members is None:
            members = []

        endpoint = '/groupmgr/group'
        body = {
            "name": name,
            "description": description,
            "admingroup": admingroup,
            "targets": targets,
            "members": members
        }
        resp = self._post_request(endpoint, body)
        if resp.ok:
            data = json.loads(resp.content.decode())
            if VERBOSE: print("new group {} was successfully created".format(name))
            return Group(conn=self, data=data)
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


    def del_group(self, name):
        """Deletes a group and removes it from all its target systems.
        """
        endpoint = '/groupmgr/group/{}'.format(name)
        resp = self._delete_request(endpoint)
        if resp.ok:
            if VERBOSE: print("group {} was successfully deleted".format(name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


    def get_groups(self, **kwargs):
        """
        agroup=<Admin Group>  -- Get all groups of a given admin group
        name=group_name*      -- all groups starting with «group_name*»
        """
        if kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = '/groupmgr/groups?{}'.format(args)
        else:
            raise ValueError("please provide a name or agroup parameter (or both)")

        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            groups = []
            for item in data:
                groups.append(Group(conn=self, data=item))

            return groups
        else:
            raise ValueError(data['message'])


    def get_group(self, identifier=None):
        if identifier is not None:

            if re.search(r'^\d+$', identifier):
                # we searched for a gidNumber
                groups = self.get_groups(gidNumber=identifier)
                if len(groups) == 1:
                    return groups[0]
                else:
                    raise ValueError('No group found with gidNumber={}'.format(identifier))
            else:
                endpoint = '/groupmgr/group/{}'.format(identifier)
        else:
            raise ValueError("please provide an identifier")
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Group(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    
    def get_mailinglist(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = '/mailinglists/{}'.format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val) for key, val in kwargs.items())
            endpoint = '/mailinglists/?{}'.format(args)
        else:
            raise ValueError("please provide an identifier")
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Mailinglist(conn=self, data=data)
        else:
            raise ValueError(data['message'])


class Person():
    def __init__(self, conn, data=None):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])
        
    def new_user(self, username, password, description=None):
        endpoint = '/usermgr/person/{}'.format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body) 
        if resp.ok:
            user = self.conn.get_user(username) 
            if VERBOSE: print("new user {} was successfully created".format(username))
            return user
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
    

class User():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

    def delete(self):
        endpoint = '/usermgr/person/{}'.format(self.username)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE: print("User {} deleted.".format(self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def get_person(self):
        endpoint = '/usermgr/person/{}'.format(self.npid)
        resp = self.conn._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Person(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def _to_from_group(self, group_name, action='add', mess="{} {}"):
        endpoint = '/groupmgr/group/{}/members/{}'.format(group_name, action)
        body = [ self.username ]
        resp = self.conn._put_request(endpoint, body)
        if resp.ok:
            if VERBOSE: print(mess.format(self.username, group_name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def add_to_group(self, group_name):
        self._to_from_group(group_name, action='add_forgiving', mess="Added user {} to group {}")

    def remove_from_group(self, group_name):
        self._to_from_group(group_name, 'del', mess="Removed user {} from group {}")


    def grant_service(self, service_name):
        endpoint = '/usermgr/user/{}/service/{}'.format(self.username, service_name)
        resp = self.conn._post_request(endpoint, {})
        if resp.ok:
            if VERBOSE: print("Service {} granted to {}".format(service_name, self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def revoke_service(self, service_name):
        endpoint = '/usermgr/user/{}/service/{}'.format(self.username, service_name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE: print("Service {} revoked from {}".format(service_name, self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def get_service(self, service_name):
        # TODO: API is not implemented yet
        endpoint = '/usermgr/user/{}/service/{}'.format(self.username, service_name)
        resp = self.conn._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Service(conn=self.conn, data=data)
        else:
            raise ValueError(data['message'])

    def set_password(self, password, service_name="LDAPS"):
        """Sets a password for a given service
        """
        endpoint = '/usermgr/user/{}/service/{}'.format(self.username, service_name)
        body = { "password": password }
        resp = self.conn._put_request(endpoint, body) 

        if resp.ok:
            if VERBOSE: print(
                "password for user {} and service {} has been successfully changed.".format(
                    self.username, service_name
                )
            )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


class Service():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])


class Group():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

    def set_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(members, action='', mess="Members group {} set")

    def add_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(members, action='add_forgiving', mess="Added members to group {}")

    def del_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        self._to_from_group(members, action='del', mess="Removed members from group {}")

    def _to_from_group(self, members, action='add', mess="{}"):
        endpoint = '/groupmgr/group/{}/members/{}'.format(self.name, action)
        resp = self.conn._put_request(endpoint, members)
        if resp.ok:
            if VERBOSE: print(mess.format(self.name))
            self.data = json.loads(resp.content.decode())
            self.members = self.data['members']
            self.targets = self.data['targets']
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def delete(self):
        endpoint = '/groupmgr/group/{}'.format(self.name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE: print("Group {} deleted.".format(self.name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


class Mailinglist():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

            self.name = data['listName']

            members=[]
            self.members = members
            for member in data['members']:
                match = re.search(r'^cn=(?P<cn>.*?)\,', member, re.IGNORECASE)
                if match:
                    members.append(match.groupdict()['cn'])

    def set_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        resp = self._to_from_group(members, action='', mess="Members for mailinglist {} set")
        try:
            text = resp['audit_trail']['granted']
            text = re.sub(r'[\[\]]', '', text)
            self.members = re.split(r'\,\s*', text)
        except Exception:
            pass

    def add_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        try:
            resp = self._to_from_group(members, action='add', mess="Added members to mailinglist {}")
            text = resp['audit_trail']['granted']
            text = re.sub(r'[\[\]]', '', text)
            members_to_add = re.split(r'\,\s*', text)
            for member in members_to_add:
                if member:
                    self.members.append(member)
        except Exception:
            pass

    def del_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        try:
            resp = self._to_from_group(members, action='del', mess="Removed members from mailinglist {}")
            text = resp['audit_trail']['revoked']
            text = re.sub(r'[\[\]]', '', text)
            members_to_revoke = re.split(r'\,\s*', text)
            for member in members_to_revoke:
                if member:
                    self.members.remove(member)

        except Exception:
            pass


    def _to_from_group(self, members, action='add', mess="{}"):
        endpoint = '/mailinglists/{}/members/{}'.format(self.name, action)
        resp = self.conn._put_request(endpoint, members)
        if resp.ok:
            if VERBOSE: print(mess.format(self.name))
            return json.loads(resp.content.decode())
            
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def delete(self):
        endpoint = '/mailinglists/{}'.format(self.name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE: print("Mailinglist {} deleted.".format(self.name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


def _load_configuration(paths, filename='.ethz_iam_webservice'):
    if paths is None:
        paths = [os.path.expanduser("~")]

    # look in all config file paths 
    # for configuration files and load them
    admin_accounts = []
    for path in paths:
        abs_filename = os.path.join(path, filename)
        if os.path.isfile(abs_filename):
            with open(abs_filename, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    for admin_account in config['admin_accounts']:
                        admin_accounts.append(admin_account)
                except yaml.YAMLexception as e:
                    print(e)
                    return None

    return admin_accounts


def login(admin_username=None, admin_password=None):
    hostname = "https://iam.passwort.ethz.ch"
    endpoint_base = "/iam-ws-legacy"

    config_path = os.path.join(
        os.path.expanduser("~"),
        '.ethz_iam'
    )
    if os.path.exists(config_path):
        import configparser
        raise Exception("not yet implemented")

    if admin_username is None:
        admin_username = input("Enter the admin username: ".format(admin_username))

    if admin_password is None:
        import getpass
        admin_password = getpass.getpass("Enter the password for admin user {}".format(admin_username))

    return ETH_IAM_conn(admin_username, admin_password, hostname, endpoint_base)

def get_username_password(ctx):

    if ctx.obj['username'] is None:
        ctx.obj['username'] = click.prompt(
            text='Username', 
            default=os.environ.get('USER', ''),
            show_default=True,
        )

    if ctx.obj['password'] is None:
        ctx.obj['password'] = click.prompt(text='Password', hide_input=True)


@click.command()
@click.argument('group')
@click.option('-d', '--delete',
    is_flag=True,
    help='delete this group'
)
@click.option('-m', '--members',
    is_flag=True,
    help='show members of the group',
)
@click.option('-i', '--info',
    is_flag=True,
    help='all information about the group',
)
@click.option('-a', '--add',
    help='username to add to group. Can be used multiple times: -a us1 -a us2',
    multiple=True
)
@click.option('-r', '--remove',
    help='username to remove from group. Can be used multiple times: -r us1 -r us2',
    multiple=True
)
@click.pass_context
def group(ctx, group, delete, members, info, add=None, remove=None):
    """group modifications.
    """
    if add is None: add = ()
    if remove is None: remove = ()

    get_username_password(ctx)

    e = login(ctx.obj['username'], ctx.obj['password'])
    group = e.get_group(group)

    if add:
        group.add_members(*add)
    if remove:
        group.del_members(*remove)

    if add or remove or members:
        print(json.dumps(group.members))

    if info:
        print(json.dumps(group.data, indent=4, sort_keys=True))

    if delete:
        confirmed = click.confirm('Do you really want to delete this group?', abort=True)
        group.delete()


#default=os.environ.get('NEO4J_HOSTNAME')
#@click.option('--password', prompt=True, hide_input=True,
#    help='password of your ETHZ IAM admin account')
@click.group()
@click.option('-u', '--username',
    help='username of your ETHZ IAM admin account (if not provided, it will be prompted)')
@click.option('--password', 
    help='password of your ETHZ IAM admin account (if not provided, it will be prompted)')
@click.option('-h', '--host',
    default= "https://iam.passwort.ethz.ch",
    help="default: https://iam.passwort.ethz.ch"
)
@click.pass_context
def cli(ctx, host, username, password=None):
    """ETHZ IAM command-line tool.
    """
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['username'] = username
    ctx.obj['password'] = password

cli.add_command(group)

if __name__ == '__main__':
        cli(obj={})
