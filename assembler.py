def main():
	with open("input.txt", "r") as file:
		while line := file.readline():
			print(line)


if __name__ == "__main__":
	main()
