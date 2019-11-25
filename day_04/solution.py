
from datetime import datetime
from collections import defaultdict, Counter


def parse_event(line):
	time, event = line.split(']', 1)
	time = datetime.fromisoformat(time[1:])
	event = event.split()[1]  # up/asleep/#{id}
	return (time, event)


with open('input.txt') as f:
	events = sorted(parse_event(line) for line in f)


sleeping_guards = defaultdict(list)
on_duty = None
sleep_start = None
for time, event in events:
	if event.startswith('#'):
		on_duty = int(event[1:])
	elif event == 'asleep':
		sleep_start = time.minute
	elif event == 'up':
		assert sleep_start is not None
		sleeping_guards[on_duty].append(range(sleep_start, time.minute))
	else:
		raise ValueError(f'unknown event: {event}')

most_sleepy = (0, 0)
for guard, sleep in sleeping_guards.items():
	sleep_time = sum(len(nap) for nap in sleep)
	most_sleepy = max(most_sleepy, (sleep_time, guard))

sleeping_beauty = sleeping_guards[most_sleepy[1]]

histogram = Counter()
for nap in sleeping_beauty:
	histogram.update(nap)

minute, _ = histogram.most_common(1)[0]

print('Day 4, part 1:', minute * most_sleepy[1])

