from math import ceil, log
import argparse
import sys


class MyArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        sys.exit(status)

    def error(self, message):
        # self.print_usage(sys.stderr)
        print('Incorrect parameters')
        # args = {'prog': self.prog, 'message': message}
        self.exit(2)


parser = MyArgumentParser(description='This program calculates...', exit_on_error=False)


parser.add_argument('-pr', '--principal', type=int,
                    help='--principal You can get its value if you know the interest, annuity payment, '
                         'and number of months.')
parser.add_argument('-pa', '--payment', type=float,
                    help='--payment is the payment amount. It can be calculated using the provided principal, '
                         'interest, and number of months.')
parser.add_argument('-pe', '--periods', type=int,
                    help='--principal You can get its value if you know the interest, '
                         'annuity payment, and number of months.')
parser.add_argument('-i', '--interest', type=float, required=True,
                    help='--interest is specified without a percent sign. Note that it can accept a floating-point '
                         'value. Our loan calculator can\'t calculate the interest, so it must always be provided.')
parser.add_argument('-om', '--old_mode', action='store_true',
                    help='--old_mode enables old interface')
parser.add_argument('-t', '--type', required=True, choices=['annuity', 'diff'],
                    help='--type argument is indicating the type of payment: "annuity" or "diff" (differentiated). '
                         'It must always be provided in any run.')

def old_mode():
    loan_principal = 'Loan principal: 1000'
    final_output = 'The loan has been repaid!'
    first_month = 'Month 1: repaid 250'
    second_month = 'Month 2: repaid 250'
    third_month = 'Month 3: repaid 500'

    # write your code here
    print(f'''{loan_principal}
             {first_month}
             {second_month}
             {third_month}
             {final_output}''')

    def number_monthly_payments(loan, amount):
        months = ceil(loan / amount)
        return print(f'It will take {months} month{"s"[:months ^ 1]} to repay the loan')

    def monthly_payments(loan, months):
        payment = ceil(loan / months)
        last_payment = loan - ((months - 1) * payment)
        return print(
            f'Your monthly payment = {payment}{f" and the last payment = {last_payment}." if payment != last_payment else "."}')

    try:
        loan_principal = int(input('Enter the loan principal:\n'))
        option = input('''What do you want to calculate?
            type "m" for number or monthly payments,
            type "p" for monthly payment:\n''')

        if option not in ["m", "p"]:
            raise Exception('Only option "m" or "p" is allowed')
    except Exception as e:
        print(e)
    else:
        match option:
            case "m":
                payments_amount = int(input('Enter the monthly payments:\n'))
                number_monthly_payments(loan_principal, payments_amount)
            case "p":
                months_amount = int(input('Enter the number of months:\n'))
                monthly_payments(loan_principal, months_amount)
            case default:
                pass

    exit(1)


def calculate_overpayment(total: int, loan: int):
    print(f'Overpayment = {total - loan}')

def calculate_annuity(loan: int, interest: float, months: int):
    annuity = ceil(loan * ((interest * (1 + interest) ** months) / (((1 + interest) ** months) - 1)))
    print(f'Your monthly payment = {annuity}!')
    calculate_overpayment((annuity * months), loan)
    exit(1)


def calculate_loan_principal(annuity: float, interest: float, months: int):
    principal = int(annuity // ((interest * ((1 + interest) ** months))/(((1 + interest) ** months) - 1)))
    print(f'Your loan principal = {principal}!')
    calculate_overpayment(int(annuity * months), principal)
    exit(1)


def calculate_number_of_payments(interest: float, annuity: float, loan: int):
    periods = log((annuity / (annuity - interest * loan)), 1 + interest)
    years, months = divmod(ceil(periods), 12)

    if years == 0:
        print(f'{months} months')
        exit(1)

    result = f'{years} year{"s"[:years ^ 1]}'

    if months > 0:
        result += f' and {months} month{"s"[:months ^ 1]}'

    print(result)
    calculate_overpayment(int(annuity * ceil(periods)), loan)
    exit(1)


def calculate_nominal_interest_rate(interest: float):
    return interest / (12 * 100)


def calculate_differentiated_payments(loan: int, months: int, interest: float):
    sum = 0
    for i in range(1, months + 1):
        diff = ceil((loan / months) + (interest * (loan - ((loan * (i - 1))/months))))
        sum += diff
        print(f'Month {i}: payment is {diff}')
    calculate_overpayment(sum, loan)
    exit(1)


try:
    args = parser.parse_args()
except argparse.ArgumentError:
    print('Incorrect parameters')
except SystemExit:
    print('Incorrect parameters')
except argparse.ArgumentTypeError:
    print('Incorrect parameters')
else:
    if args.old_mode:
        old_mode()

    nir = calculate_nominal_interest_rate(args.interest)

    if args.type == 'annuity':
        if args.principal and args.payment and not args.periods:
            calculate_number_of_payments(nir, args.payment, args.principal)

        if args.principal and not args.payment and args.periods:
            calculate_annuity(args.principal, nir, args.periods)

        if not args.principal and args.payment and args.periods:
            calculate_loan_principal(args.payment, nir, args.periods)

    if args.type == 'diff':
        calculate_differentiated_payments(args.principal, args.periods, nir)

    raise argparse.ArgumentError(None, 'Incorrect parameters')