import csv
import mysql.connector
import datetime
from datetime import date

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

def populate_books_purchased(cursor, books_list, books_dict):
	add_book_query = 'insert into books_purchased (title, created, updated) values (%s, %s, %s)'
	for book in books_list:
		data_book_query = (book, date.today(), date.today())
		cursor.execute(add_book_query, data_book_query)
		book_id = cursor.lastrowid
		books_dict[book] = book_id

def populate_books_distribution(reader, cursor):
	add_book_distribution_query = 'insert into books_distribution (student_id, book_id, dist_date, created, updated) values (%s, %s, %s, %s, %s)'
	get_student_query = 'select id from students where family_id = %s and first_name = %s and is_active = %s'
	family_ids_with_two_word_first_name = [42082, 73143, 41772, 92539, 60480, 97937]
	problem_record_count = 0

	for row in reader:
		family_id = int(row['Family ID'])
		
		name = row['Student Name'].split()
		books = row['Books Issued'].split()

		if family_id not in family_ids_with_two_word_first_name:
			get_student_query_data = (int(row['Family ID']), name[0], 1)
		elif family_id == 41772 and name[0] == 'Abdul': # Handle Basit's case as exception. Her family has 2 word name but his name is 3 word
			get_student_query_data = (int(row['Family ID']), name[0] + ' ' + name[1], 1)
		elif family_id == 41772 and name[0] != 'Abdul': # Handle case of children other than Basit as exception. Her family has 2 word name but his name is 3 word
			get_student_query_data = (int(row['Family ID']), name[0], 1)
		elif family_id == 97937 and name[0] == 'Aqib': # Handle Aqib's case as exception. His family has 2 word name but his name is 3 word
			get_student_query_data = (int(row['Family ID']), name[0] + ' ' + name[1], 1)
		elif family_id == 97937 and name[0] != 'Aqib': # Handle Aqib's case as exception. His family has 2 word name but his name is 3 word
			get_student_query_data = (int(row['Family ID']), name[0], 1)
		else:
			get_student_query_data = (int(row['Family ID']), name[0] + ' ' + name[1], 1)

		cursor.execute(get_student_query, get_student_query_data)

		rows = cursor.fetchall()

		if len(rows) > 1:
			print 'Student Info Problem: More than one student record found: Family ID', family_id, 'Student Name', row['Student Name']
			problem_record_count = problem_record_count + 1
		elif len(rows) == 0:
			print 'Student Info Problem: No student record found: Family ID', family_id, 'Student Name', row['Student Name']
			problem_record_count = problem_record_count + 1
		else:
			for row in rows:
				print 'Student Record Found: ', row[0]

	print "Total Problem Records:", problem_record_count



		




# parse csv file and build a list i.e. books_list
#books_dict = dict()
file_handle = open(filename)
reader = csv.DictReader(file_handle)
#books_list = list()
'''for row in reader:
	books = row['Books Issued'].split(', ')
	books_list.extend(books)
	
# build a dictionary i.e. books_dict from books_list to remove duplicate books
for book in books_list:
	if books_dict.get(book, 0) == 0:
		books_dict[book] = book

# Remove duplicates from books_list
books_list = sorted(books_dict.values())

index = 0
for index in range(len(books_list)):
	print books_list[index]'''

# populate books in books_distribution table
cnx = mysql.connector.connect(user='mccss_adeeb', password='Pleasanton!', host='127.0.0.1', database='schooladminv3')
cursor = cnx.cursor()

#populate_books_purchased(cursor, books_list, books_dict)
populate_books_distribution(reader, cursor)

#cnx.commit()

'''rows = cursor.fetchall()

for row in rows:
	print row[0]'''

cursor.close()
cnx.close()