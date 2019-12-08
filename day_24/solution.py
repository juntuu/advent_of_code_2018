
import sys
from dataclasses import dataclass
from typing import FrozenSet, Optional
from copy import deepcopy


@dataclass
class Group:
	army: str
	units: int
	initiative: int
	hp: int
	damage: int
	attack: str
	immunities: FrozenSet[str] = frozenset()
	weaknesses: FrozenSet[str] = frozenset()
	target: Optional['Group'] = None

	def __hash__(self):
		return id(self)

	def __lt__(self, x):
		return (self.effective_power, self.initiative) < (x.effective_power, x.initiative)

	@property
	def dead(self):
		return self.units <= 0

	@property
	def effective_power(self):
		return self.damage * self.units

	def damage_to(self, target):
		if self.attack in target.immunities:
			return 0
		if self.attack in target.weaknesses:
			return 2 * self.effective_power
		return self.effective_power


def parse_group(name, s):
	n, *_, hp, _1, _2, s = s.split(maxsplit=7)
	immune = []
	weak = []
	if s.startswith('('):
		x, s = s.split(') ', maxsplit=1)
		parts = x[1:].split('; ')
		for p in parts:
			p, _, x = p.split(maxsplit=2)
			if p.startswith('weak'):
				weak.extend(x.split(', '))
			elif p.startswith('immune'):
				immune.extend(x.split(', '))

	*_, d, t, s = s.split(maxsplit=7)
	*_, i = s.split()
	return Group(
			army=name,
			initiative=int(i),
			units=int(n),
			hp=int(hp),
			damage=int(d),
			attack=t,
			immunities=frozenset(immune),
			weaknesses=frozenset(weak))


def parse(filename):
	units = []
	name = None
	with open(filename) as f:
		for line in f:
			if line.isspace():
				name = None
			elif name is None:
				name = line.strip(':\n')
			else:
				units.append(parse_group(name, line))
	return units


def battle(groups):
	armies = {u.army for u in units}
	while all(any(u.army == army for u in groups) for army in armies):
		targets = {
				a: {t for t in groups if t.army != a}
				for a in armies
				}
		for g in sorted(groups, reverse=True):
			for e in sorted(targets[g.army], key=lambda e: (g.damage_to(e), e), reverse=True):
				if g.damage_to(e) > 0:
					g.target = e
					targets[g.army].remove(e)
					break

		kills = 0
		for g in sorted(groups, key=lambda g: g.initiative, reverse=True):
			if g.dead:
				continue
			if g.target:
				killed = g.damage_to(g.target) // g.target.hp
				g.target.units -= killed
				kills += killed
			g.target = None
		if not kills:
			break
		groups = [g for g in groups if not g.dead]
	return {a: sum(g.units for g in groups if g.army == a) for a in armies}


if len(sys.argv) > 1:
	units = parse(sys.argv[1])
else:
	units = parse('input.txt')

res = battle(deepcopy(units))
print('Day 24, part 1:', max(res.values()))


def boosted_battle(groups, **boosts):
	for g in groups:
		g.damage += boosts.get(g.army, 0)
	return battle(groups)


lo, hi = 1, None
while hi is None or lo < hi:
	if hi:
		boost = (lo + hi) // 2 + 1
	else:
		boost = lo * 2
	res = boosted_battle(deepcopy(units), **{'Immune System': boost})
	if res['Infection']:
		lo = boost + 1
	else:
		hi = boost
		final = res

print('Day 24, part 2:', final['Immune System'])

