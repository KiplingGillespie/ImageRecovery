from FileIO import *
from CommentCounter import *

def main():
	text = FileIO.readText("test/testIO/testCommentCounter.txt")
	print(getComments(text))
	print("!")
	print(getWords(text))


if __name__=="__main__":
	main()
