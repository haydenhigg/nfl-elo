import json

# load match data
with open('matches20242025.json') as f:
    matches = json.load(f)

# calculate ratings
K = 12.5 # to match the original equations

ratings = {}

def expected(a: int, b: int) -> float:
    # denominator was 400 in the original formula but adjusted as these ratings
    # are not skewed in the same way (other constants are dropped)
    return 1 / (1 + 10 ** ((b - a) / K))

for i, (a, b, outcome) in enumerate(matches):
    if a not in ratings: ratings[a] = K
    if b not in ratings: ratings[b] = K

    e = expected(ratings[a], ratings[b])
    ratings[a] += outcome - e
    ratings[b] += e - outcome

# print ratings
for k, v in sorted(ratings.items(), key=lambda r: -r[1]):
    print(f'{k} - {v:.1f}')

# start interactive match prediction
print('\nex. "Match: eagles commanders"')
while (match := input('Match: ')) != '':
    try:
        a, b = match.split(' ', 1)
    except ValueError:
        print('bad format')
        continue

    try:
        e = expected(ratings[a.upper()], ratings[b.upper()])
    except KeyError:
        print('unknown key')
        continue

    if e >= 0.5:
        print(f'{a} {100 * e:.1f}%')
    else:
        print(f'{b} {100 * (1 - e):.1f}%')
