import requests
from bs4 import BeautifulSoup
import re
import datetime


BASE_URL = 'http://nesssi.cacr.caltech.edu/catalina/'

FIELDS = (
	'newast',
	'av_motn',
	'av_deltime',
	'av_uncertx',
	'av_uncerty',
	'av_inclin',
	'Time',
	'Time2',
	'Time3',
	'Time4',
	'appreject',
	'mastersn',
	'averagesn',
	'theta',
	'nhigh',
	'RA',
	'Dec',
	'Mag',
	'Mag_err',
	'FWHM',
	'Master',
	'MasterRAoff',
	'MasterDecoff',
	'RA2',
	'Dec2',
	'Mag2',
	'Mag2_err',
	'FWHM2',
	'RA3',
	'Dec3',
	'Mag3',
	'Mag3_err',
	'FWHM3',
	'RA4',
	'Dec4',
	'Mag4',
	'Mag4_err',
	'FWHM4',
	'Oppos_ang',
	'Inner_motion',
	'Outer_motion',
	'Eclip_long',
	'Eclip_lat',
)

def get_details(item):
	r = requests.get(item['url'])
	for field in FIELDS:
		m = re.search(field + r'\s+=\s+([^<]+)', r.text)
		if m is not None:
			item[field] = m.group(1)
	print '-------------------------------------'
	for k, v in item.iteritems():
		print '{0}: {1}'.format(k, v)
	print '-------------------------------------'
	# do_something_with_item


def get_entries():
	r = requests.get(BASE_URL)
	soup = BeautifulSoup(r.text)

	links = soup.find_all('a')

	# Ordena las entradas por fecha
	entries = [link.getText() for link in soup.find_all('a')]
	entries.sort()

	# La del dia actual da un 403. Obtenemos la del dia anterior
	url = BASE_URL + entries[-2]

	r = requests.get(url)

	"""
	Example out:
	<h2>Catalina Transients 20140409</h2>
	(...)
	<a href=1404091350674132315.html>1404091350674132315</a> 225.0097600  36.0053100  2456756.925520 Created Wed Apr  9 03:17:42 2014 Prior 1303231350674129048<br/>
	<a href=1404091350674117264.html>1404091350674117264</a> 225.4700300  34.9978900  2456756.925520 Created Wed Apr  9 03:18:03 2014 Prior 0<br/>
	"""

	iterator = re.finditer(r'^<a href=([^>]+)>([^<]*)</a>\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+' + \
		r'Created\s+([^P]+)Prior\s+(\d+)<br/>$', r.text, re.MULTILINE)

	for match in iterator:
		item = {
			'id': match.group(2),
			'url': '{0}/{1}'.format(url, match.group(1)),
			'x': match.group(3),
			'y': match.group(4),
			'z': match.group(5),
			'created_on': datetime.datetime.strptime(match.group(6), '%a %b  %d %H:%M:%S %Y '),
			'prior': match.group(7),
		}
		get_details(item)


if __name__ == '__main__':
	get_entries()
	