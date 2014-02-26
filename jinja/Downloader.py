from time import sleep
import urllib
import urllib2
import zipfile
import os
import options
import shutil
import paramiko


def get_downloader():
    in_format = options.getOptions()[0].in_format
    print "in_format", in_format
    if in_format == "ISAR":
    	return ISAR_downloader()
    else:
    	return SACK_downloader()

def _download(url, file_name):
    print "INF: Try download: ", file_name
    try:
        f = urllib.URLopener()
        f.retrieve(url, file_name)
        ex = 0
    except:
        print 'Problem with downloading:', url
        ex = 1
    return ex

def _unpack( file_name):
	print "INF: Unpacking: ", file_name
	fh = open(file_name, 'rb')
	with zipfile.ZipFile(file_name, "r") as z:
		
		for name in z.namelist():
			outpath = "."
			z.extract(name, outpath)
	fh.close()	

def _get_config_file():
	addr = "192.168.255.1"
	port = 22
	user = "toor4nsn"
	private_key = "/home/ute/.ssh/toor4nsn/id_rsa"

	def ssh_connect(host, username, private_key, port=22):
		"""Helper function to initiate an ssh connection to a host."""
		transport = paramiko.Transport((host, port))

		if os.path.exists(private_key):
		    rsa_key = paramiko.RSAKey.from_private_key_file(private_key)
		    transport.connect(username=username, pkey=rsa_key)
		else:
		    raise TypeError("Incorrect private key path")

		return transport

	def exec_cmd(transport, command):
	    """Executes a command on the same server as the provided
	    transport
	    """
	    channel = transport.open_session()
	    channel.exec_command(command)
	    output = channel.makefile('rb', -1).readlines()
	    return output


	os.system("curl -k -u Nemuadmin:nemuuser https://192.168.255.129/protected/enableSsh.cgi")
	ssh = ssh_connect(host=addr,
	                  username=user,
	                  private_key=private_key)


	print"INF: Download config file from BTS"

	if "true\n" in exec_cmd(ssh, "[ -e /flash/config/config ] && echo \"true\" || echo \"false\""):
		config_content = exec_cmd(ssh, "cat /flash/config/config")
		with open("config_from_bts", "w") as f:
			for l in config_content:
				f.write(l)

class SACK_downloader(object):

	print "SACK"
	url = "http://wrling30.emea.nsn-net.net:9989/job/html_env_generator/"
	config_from_bts = 'config_from_bts'
	current_config = 'config'
	sack_required_nr = ''
	sack_current_nr = ''
	cwd =''

	def __init__(self):
		self.cwd = os.getcwd()		

	def __get_sack_ver(self, file_name):
		sack_nr = ''
		with open(file_name, "r") as f:
			sack_nr = f.read()

		sack_nr = sack_nr.split("\n")
		sack_nr = sack_nr[4].split(" ")
		sack_nr = sack_nr[3]

		return sack_nr

	def __check_versions(self):
		
		self.sack_required_nr = self.__get_sack_ver(self.config_from_bts)
		print"INF: Required version of sack is: ", self.sack_required_nr 
		self.sack_current_nr = self.__get_sack_ver(self.current_config)
		print"INF: Current version of sack is: ", self.sack_current_nr

		if self.sack_current_nr == self.sack_required_nr:
			print "INF: SACK verison is OK"
			return 0
		else:
			print "INF: SACK ver is not actual"
			if os.path.exists(os.path.join(self.cwd, "HTML_ENV")):
				shutil.rmtree(os.path.join(self.cwd, "HTML_ENV"))
			return 1

	def __get_url_addr(self):
		f = urllib.urlopen(self.url)
		html = f.readlines()
		f.close()
		index = 0
		for l in html:
			if self.sack_required_nr in l:
				index = html.index(l)
				break
		addr = "/".join([self.url[:-1], html[index-1][-4:-1],"artifact", self.sack_required_nr + ".zip"])
		return addr

	def __generate_sack(self, build_version):
		print"INF: Generate sack version: ", build_version  
		post_data = 'name=TAG_NAME&value='+build_version+'&json=%7B%22parameter%22%3A+%7B%22name%22%3A+%22TAG_NAME%22%2C+%22value%22%3A+%22'+build_version+'%22%7D%7D&Submit=Buduj'
		url = "http://wrling30.emea.nsn-net.net:9989/job/html_env_generator/build?delay=0sec"
		request = urllib2.Request(url, post_data)
		response = urllib2.urlopen(request)
		sleep(120)

	def __clean(self):
		os.chdir(self.cwd)
		os.remove(self.sack_required_nr + ".zip")
		os.remove("config")
		os.rename("config_from_bts", "config")

	def check(self):
		_get_config_file()
		if 1 == self.__check_versions():
			self.__generate_sack(self.sack_required_nr)
			_download(self.__get_url_addr(), self.sack_required_nr + ".zip")
			_unpack(self.sack_required_nr + ".zip")
			self.__clean()

class ISAR_downloader(object):

	print "ISAR"
	url = 'http://dspcimaster.emea.nsn-net.net:2020/view/Sack/job/Zipped_sacks_automatic_Trunk/'
	config_from_bts = 'config_from_bts'
	current_config = 'config'
	isar_required_nr = ''
	isar_current_nr = ''
	cwd = ''

	def __init__(self):
		self.cwd = os.getcwd()
		print self.cwd

	def __get_isar_ver(self, file_name):
		sack_nr = ''
		with open(file_name, "r") as f:
			isar_nr = f.read()

		isar_nr = isar_nr.split("\n")
		isar_nr = isar_nr[10].split(' ')
		isar_nr = isar_nr[3]

		return isar_nr

	def __check_versions(self):
		self.isar_required_nr = self.__get_isar_ver(self.config_from_bts)
		print"INF: Required version of isar is: ", self.isar_required_nr 
		self.isar_current_nr = self.__get_isar_ver(self.current_config)
		print"INF: Current version of isar is: ", self.isar_current_nr

		if self.isar_current_nr == self.isar_required_nr:
			print "INF: ISAR verison is OK"
			return 0
		else:
			print "INF: ISAR ver is not actual"
			return 1

	def __get_url_addr(self):
		f = urllib.urlopen(self.url)
		html = f.readlines()
		f.close()
		index = 0
		for l in html:
			if self.isar_required_nr in l:
				index = html.index(l)
				break
		addr = "/".join([self.url[:-1], html[index-1][-4:-1],"artifact/*zip*/archive.zip"])
		return addr

	def __get_isar_name(self):
		os.chdir(os.path.join("archive", "output"))
		list_dir = os.listdir(".")
		for l in list_dir:
			if "[CLEAN]" in l:
				return l

	def __clean(self):
		os.chdir(self.cwd)
		if os.path.exists(os.path.join(self.cwd, "Xml")):
			shutil.rmtree(os.path.join(self.cwd, "Xml"))
		path = os.path.join(self.cwd, "archive", "output", "I_Interface", "Application_Env", "Isar_Env", "Xml")
		shutil.move(path, self.cwd)
		os.remove("archive.zip")
		shutil.rmtree(os.path.join(self.cwd, "archive"))
		os.remove("config")
		os.rename("config_from_bts", "config")

	def check(self):
		_get_config_file()
		if 1 == self.__check_versions():
			self.__get_url_addr()
			_download(self.__get_url_addr(), "archive.zip")
			_unpack("archive.zip")
			_unpack(self.__get_isar_name())
			self.__clean()
