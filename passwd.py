import glob, os

os.chdir(r"C:\Users\bapti\Desktop\SRC_FTP-master\Serveur_Storage\PARIS")
for file in glob.glob("*"):
    print(file)
