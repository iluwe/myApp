import click
import time
from sqlitedb import UsersDataBase
from datetime import datetime, date
from random import choice, randint
from tabulate import tabulate

db = UsersDataBase('users.db')  # init db


def check_input_date(date_of_birth, sex):
    """Checking input data for correct format"""
    flag = 1
    if sex != 'm' and sex != 'f':
        click.echo('===== Sex - not correct data. Format should be m (male) or f (female)')
        flag = 0
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        click.echo('===== Date - not correct data. Format should be %Y-%m-%d')
        flag = 0
    return flag


@click.command()
@click.argument('operation', nargs=-1)
def main(operation):
    if operation[0] == '1':
        if db.check_table():
            answer = input('Table already exists. Want to clear all data? [y/N]')
            if answer == 'y':
                rows = db.clear_table()
                click.echo(f'{rows} have been deleted')
        else:
            db.create_table()
            click.echo('Table is created')

    elif operation[0] == '2':
        full_name = ' '.join(operation[1:4])
        date_of_birth = operation[4]
        sex = operation[5]
        if not check_input_date(date_of_birth, sex):
            return
        db.add_user(full_name, date_of_birth, sex)

    elif operation[0] == '3':
        rows = db.unique_full_name_date()
        table = []
        today = date.today()
        for row in rows:
            dob = row[1].split('-')
            dob = list(map(int, dob))
            age = today.year - dob[0] - ((today.month, today.day) < (dob[1], dob[2]))
            table.append([row[0], row[1], row[2], age])
        click.echo(tabulate(table, headers=['Name', 'Day of birth', 'Sex', 'Age'], tablefmt='orgtbl'))

    elif operation[0] == '4':
        params = []
        sex_list = ['m', 'f']
        f_names = ['Marry', 'Terry', 'Jin', 'Ameli', 'Anna', 'Emma', 'Olivia', 'Ava', 'Sophia', 'Charlotte']
        m_names = ['Tom', 'John', 'Jacob', 'Michel', 'Henry', 'James', 'Noah', 'Mason', 'Logan', 'Alex']
        surnames = ['mith', 'ohnson', 'illiams', 'rown', 'iller', 'avis', 'ilson', 'owak', 'arcia', 'ossi'] # without first char
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(1000000):
            first_char = choice(chars)
            sex = choice(sex_list)
            dob = datetime(randint(1965, 2010), randint(1, 12), randint(1, 28)).strftime('%Y-%m-%d')
            if sex == 'm':
                full_name = f'{first_char}{choice(surnames)} {choice(m_names)} {choice(m_names)}'
            else:
                full_name = f'{first_char}{choice(surnames)} {choice(f_names)} {choice(f_names)}'
            params.append((full_name, dob, sex))
        db.insert_million_rows(params)
        click.echo('Million rows inserted')
        params = []
        for i in range(100):
            first_char = 'F'
            sex = 'm'
            dob = datetime(randint(1965, 2010), randint(1, 12), randint(1, 28)).strftime('%Y-%m-%d')
            full_name = f'{first_char}{choice(surnames)} {choice(m_names)} {choice(m_names)}'
            params.append((full_name, dob, sex))
        db.insert_million_rows(params)
        click.echo('Hundred rows with F inserted')

    elif operation[0] == '5':
        start = time.time()
        db.get_m_starts_f()
        click.echo(f'Lead Time: {time.time()-start}')


if __name__ == '__main__':
    main()