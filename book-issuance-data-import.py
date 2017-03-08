import csv

filename = 'MCCSS Book Issuance Form (Responses) - Form Responses 1.csv'

def first_attempt():
	with open(filename) as f:
		reader = csv.DictReader(f)
		for row in reader:
			print(row['Family ID'], row['Student Name'], row['Books Issued'])


def read_file():
	file = open(filename)
	for line in file:
		print line


read_file()