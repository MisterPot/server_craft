import configparser as cp

start_properties = {
	'maxMemory': '-Xmx{}M',
	'initMemory': '-Xms{}M',
	'port': '--port {}',
	'world': '--world {}',
	'world_dir': '--universe {}',

	'gui': {
		True: None,
		False: '--nogui',
	},
	'bonus': {
		True: '--bonusChest',
		False: None,
	},
	'safe' : {
		True: '--safeMode',
		False: None,
	},
	'init': {
		True: '--initSettings',
		False: None,
	},
	'cache': {
		True: '--eraseCache',
		False: None,
	},
	'demo': {
		True: '--demo',
		False: None,
	},
}	


class Config(object):

	def __init__(self, config_file):
		self.parser = cp.RawConfigParser()
		self.parser.read(config_file)
		self.mem_props = []
		self.start_props = []
		self.spec_props = []
		self.__set_props()
		self.start_props.extend(self.spec_props)
		self.__clear()
		self.__clear()

	def __clear(self):
		for i in self.start_props:
			if i is None:
				self.start_props.remove(i)

	def __add(self, prop):
		self.start_props.append(prop)

	def __mem_arg(self, prop):
		self.mem_props.append(prop)

	def __spec_arg(self, prop):
		self.spec_props.extend(prop.split(' '))

	def __set_props(self):

		t = ['str', 'int']

		def get(prop,type_='bool'):
			sec = 'server'
			if type_ == 'str':
				return self.parser.get(sec, prop)
			elif type_ == 'bool':
				return self.parser.getboolean(sec, prop)
			elif type_ == 'int':
				return self.parser.getint(sec, prop)


		max_ = get('maxMemory', type_=t[0])
		min_ = get('initMemory', type_=t[0])
		port = get('port', type_=t[1])
		world_dir = get('worldDir', type_=t[0])
		world = get('world', type_=t[0])
		gui = get('gui')
		bonus = get('bonusChest')
		demo = get('demo')
		cache = get('eraseCache')
		onl_init = get('onlyInit')
		safe_mod = get('safeMode')


		self.__mem_arg(start_properties['maxMemory'].format(max_))
		self.__mem_arg(start_properties['initMemory'].format(min_))
		self.__spec_arg(start_properties['port'].format(port))
		self.__spec_arg(start_properties['world'].format(world))
		self.__spec_arg(start_properties['world_dir'].format(world_dir))
		self.__add(start_properties['gui'][gui])
		self.__add(start_properties['bonus'][bonus])
		self.__add(start_properties['safe'][safe_mod])
		self.__add(start_properties['init'][onl_init])
		self.__add(start_properties['cache'][cache])
		self.__add(start_properties['demo'][demo])
