import pykov

email = "enter EFT email here"
password = "enter EFT password here"

t = pykov.tarkov.Tarkov(email, password)

f = open("testing_get_all_items.txt", "w+")
f.write(json.dumps(t.get_items(), indent=4))
f.close()