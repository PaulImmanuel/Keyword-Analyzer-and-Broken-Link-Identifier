import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, SoupStrainer
import tkinter as tk


class QuestionsExplorer:
    def GetQuestions(self, questionType, userInput, countryCode):
        questionResults = []
        # Build Google Search Query
        searchQuery = questionType + " " + userInput + " "
        # API Call
        googleSearchUrl = "http://google.com/complete/search?output=toolbar&gl=" + \
            countryCode + "&q=" + searchQuery
        # Call The URL and Read Data
        result = requests.get(googleSearchUrl)
        tree = ET.ElementTree(ET.fromstring(result.content))
        root = tree.getroot()
        for suggestion in root.findall('CompleteSuggestion'):
            question = suggestion.find('suggestion').attrib.get('data')
            questionResults.append(question)
        return questionResults

    def search_questions(self):
        # Get a Keyword From The User
        userInput = self.keyword_entry.get()

        # Call The Method and pass the parameters
        questions = self.GetQuestions("is", userInput, "us")

        # Clear the current contents of the result text box
        self.result_text.delete(1.0, tk.END)

        # Loop over the list and print the questions to the result text box
        for result in questions:
            self.result_text.insert(tk.END, result + "\n")
#program2
    def check_links(self):
        # Prompt user to enter the URL
        url = self.url_entry.get()

        # Make a request to get the URL
        page = requests.get(url)

        # Get the response code of given URL
        response_code = str(page.status_code)

        # Display the text of the URL in str
        data = page.text

        # Use BeautifulSoup to use the built-in methods
        soup = BeautifulSoup(data)

        # Clear the current contents of the result text box
        self.result_text.delete(1.0, tk.END)

        # Iterate over all links on the given URL with the response code next to it
        for link in soup.find_all('a'):
            self.result_text.insert(
                tk.END, f"Url: {link.get('href')} | Status Code: {response_code}\n")

    def __init__(self, master):
        self.master = master
        master.title("Keyword Research and Broken Links Checker")

        # Create keyword input label and entry box
        self.keyword_label = tk.Label(master, text="Enter a Keyword:")
        self.keyword_label.pack()
        self.keyword_entry = tk.Entry(master)
        self.keyword_entry.pack()

        # Create search button
        self.search_button = tk.Button(
            master, text="Search Questions", command=self.search_questions)
        self.search_button.pack()

        # Create URL input label and entry box
        self.url_label = tk.Label(master, text="Enter a URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        # Create check links button
        self.check_links_button = tk.Button(
            master, text="Check Links", command=self.check_links)
        self.check_links_button.pack()

        # Create result text box
        self.result_label = tk.Label(master, text="Results:")
        self.result_label.pack()
        self.result_text = tk.Text(master, height=10)
        self.result_text.pack()


root = tk.Tk()
app = QuestionsExplorer(root)
root.mainloop()
