import requests
import json

 
class time_table_api():
	def __init__(self, module_code_group):
		self.module_code_group = module_code_group
		self.parse_html(module_code_group)

	url = 'https://celcat-tst.nwu.ac.za:8446/Home/GetCalendarData'
	modules = []
	module_code_group =""

	def return_module_code(self):
		return self.module_code_group
	
	# return size of the modules
	def return_module_size(self):
		return len(self.modules)
    
	# return modules
	def return_modules(self,pos):
		return self.modules[pos]
	
	@classmethod
	def parse_html(self, module_code_group):
		module_code = module_code_group
		headers = {
				'accept': 'application/json, text/javascript, */*; q=0.01',
				'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,en-ZA;q=0.7',
				'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
				'cookie': '.AspNetCore.Antiforgery.TYugxAo8bBE=CfDJ8L2yCPvd6C5NsETwbUW935zjYJsbnlUfqfEjR1wxcXryDtvZLqnt7L8WQ16viDh1Mu44_gLWgvFeVdRvUk92_dU9Xn8wklCYlXidiH3WWYhMAbD1leR6yOj5582EPgb9-1GeZxWS8EsJ6q_Svseihbk; .Celcat.Calendar.Session=CfDJ8L2yCPvd6C5NsETwbUW935xtafpskM0UV5ivflIHvo1gry%2BdqUOkGu1M6uPhTLm0AZCi6J%2Fn7ZF2BQ49z2gxt9ng5iUsCNhTi8wwq%2B41UKnVeHViH0I0mFIJ%2Bgwx%2Fb3LtJit3DgANb4QYfsUT1IoOG%2BzUuT3sukvl%2F8NFpgqTpce',
				'dnt': '1',
				'origin': 'https://celcat-tst.nwu.ac.za:8446',
				'referer': 'https://celcat-tst.nwu.ac.za:8446/cal?vt=agendaWeek&dt=2024-03-20&et=group&fid0='+module_code,
				'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': '"Windows"',
				'sec-fetch-dest': 'empty',
				'sec-fetch-mode': 'cors',
				'sec-fetch-site': 'same-origin',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
				'x-requested-with': 'XMLHttpRequest'
		}
		data = {
					'start': '2024-03-18',
					'end': '2024-03-24',
					'resType': '103',
					'calView': 'agendaWeek',
					'federationIds[]': [module_code],
					'colourScheme': '3'
					}


		try:
				response = requests.post(self.url, headers=headers, data=data)
				modules = json.loads(response.text)
				self.modules = modules

		except: 
				print("HTTP Error") 


