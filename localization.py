import csv

# Read the csv file and return a list of lists
f = open('localization.csv', 'r')
reader = csv.reader(f)
localization = list(reader)
f.close()

# Convert to dict
langs = ["english", "icelandic"]
localization_dict = {}
for lang in range(len(langs)):
	localization_dict[langs[lang]] = {}
	for row in localization:
		key = row[0]
		value = row[lang + 1]
		if "Upgrade Mod" in key:
			msg = value.split("|")[0]
			mod = value.split("|")
			if len(mod) > 1: mod = mod[1]
			else: mod = mod[0]
			localization_dict[langs[lang]][key + " - Message"] = msg
			localization_dict[langs[lang]][key + " - Mod"] = mod
		else:
			localization_dict[langs[lang]][key] = value

# Setup

lang = "english"
def loc(s):
	if lang in localization_dict:
		if s in localization_dict[lang]:
			return localization_dict[lang][s]
	return s

def set_lang(l):
	global lang
	lang = l

def getlanglist():
	return langs

def get_lang():
	return lang

if __name__ == "__main__":
	print(localization_dict)
