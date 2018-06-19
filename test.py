import sys
import json
import xml.dom.minidom as minidom

def main():
	doc = minidom.parse("MyFile.xml")

	print(doc.nodeName)
	print(doc.firstChild.tagName)

	expertise = doc.getElementsByTagName("Interval")
	for skill in expertise:
		myArray = skill.getAttribute("TimeLapse")
	myArray = myArray.split(' ')
	
	myArray = [int(i) for i in myArray]
	print(myArray)
	

if __name__=="__main__":
	main()
