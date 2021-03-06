#!/usr/bin/env python
# coding: utf-8
import psycopg2

DBNAME = "news"


def question_1(cursor):
    print("\n1. What are the most popular three articles of all time?\n")

    cursor.execute("""select articles.title, count(*) as views
    from log,articles where articles.slug = substring(log.path from 10)
    group by articles.title order by views desc limit 3;""")

    posts = cursor.fetchall()
    for title, views in posts:
        print("\""+str(title)+"\""+" — "+str(views)+" views")
    print("\n")


def question_2(cursor):
    print("\n2. Who are the most popular article authors of all time?\n")

    cursor.execute("""select authors.name , count(*) as views
    from authors,articles,log where authors.id = articles.author
    and articles.slug = substring(log.path from 10)
    group by authors.name order by views desc;""")

    posts = cursor.fetchall()
    for name, views in posts:
        print(str(name)+" — "+str(views)+" views")
    print("\n")


def question_3(cursor):
    print("\n3. On which days did more than 1% of requests lead to errors?\n")

    subq_for_total = """(select to_char(time, 'DD Mon YYYY') as day
    , count(*) as num from log group by to_char(time, 'DD Mon YYYY')
    order by to_char(time, 'DD Mon YYYY')) as total"""

    subq_for_errors = """(select to_char(time, 'DD Mon YYYY') as day
    , count(*) as num from log where substring(status from 1 for 3) = '404'
    group by to_char(time, 'DD Mon YYYY')
    order by to_char(time, 'DD Mon YYYY')) as error"""

    cursor.execute("""select total.day
    , trunc((cast(error.num as decimal)/total.num)*100,2) as error
    from """+subq_for_total+""" , """+subq_for_errors+"""
    where total.day = error.day
    and trunc((cast(error.num as decimal)/total.num)*100,2) > 1 """)

    posts = cursor.fetchall()
    for day, error in posts:
        print(str(day)+" — "+str(error)+"% errors")
    print("\n")


def answerQuestions():
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print ("Unable to connect to the database")
        return

    cursor = db.cursor()

    question_1(cursor)
    question_2(cursor)
    question_3(cursor)

    db.close()


answerQuestions()
