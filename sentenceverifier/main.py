import argparse
from sentenceverifier.verifysentence import verify_input


def is_valid_number(parser, arg):
    try:
        arg = int(arg)
    except ValueError:
        parser.error('Numerical arguments must be integers bigger than 0 ! You have inserted {} !'.format(arg))
    if arg <= 0:
        parser.error('Numerical arguments must be integers bigger than 0 ! You have inserted {} !'.format(arg))
    else:
        return arg


parser = argparse.ArgumentParser(description="program verify true/false the input sentence")

parser.add_argument("sentence",
                    help="sentence to verify",
                    type=str)
parser.add_argument("--positivity",
                    help="enter P if your sentence is positive or N if it is negative. You can try this if in"
                         " default attempt you don't get answer.",
                    default='P',
                    type=str)
parser.add_argument("--precision",
                    help="precision of verification",
                    default=5,
                    type=lambda x: is_valid_number(parser, x))


args = parser.parse_args()

if args.positivity == 'P':
    positivity = 1
elif args.positivity == 'N':
    positivity = -1

verify_input(args.sentence, args.precision, positivity)
