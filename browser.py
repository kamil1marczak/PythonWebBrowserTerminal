import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


class Browser:
    commands = {"exit", "back"}
    tags = ["p", 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
    links = []

    def __init__(self, path_to_file):
        init(autoreset=True)
        self.history = list()
        self.is_executable = True
        self.set_files_names = set()
        self.path_to_file = path_to_file

    @staticmethod
    def url_validate(web_page: str):
        if web_page.startswith("https://"):
            return web_page
        else:
            return "https://" + web_page


    @staticmethod
    def path_validate(dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def command_execute(self, command):
        if command == "exit":
            self.is_executable = False
        elif command == "back":
            if len(self.history) > 1:
                self.history.pop()
                data = self.read_data_from_file(self.history[-1])
                Browser.print_from_file(data)

    @staticmethod
    def download_page_from_url(url):
        url = Browser.url_validate(url)
        data = requests.get(url)
        data.encoding = 'utf-8'
        return data.text

    def read_data_from_file(self, file_name):
        path = self.path_to_file + "/" + file_name + ".txt"
        data = open(path, "r").read()
        return data

    @staticmethod
    def convert_html_to_text(html_data):
        parsed_html = BeautifulSoup(html_data, "html.parser")
        parsed_html_lines_from_tags = parsed_html.find_all(Browser.tags)

        for line in parsed_html_lines_from_tags:
            if str(line)[1] == 'a':
                line_to_print = line.get_text().strip()
                Browser.links.append(line_to_print)
                print(Fore.BLUE + line_to_print)
            else:
                line_to_print = line.get_text().strip()
                print(line_to_print)

        list_of_text_lines = [line.get_text().strip() for line in parsed_html_lines_from_tags]
        final_text = "\n".join(list_of_text_lines)
        return final_text

    @staticmethod
    def highlight(word):
        if word in Browser.links:
            return Fore.BLUE + str(word) + Fore.RESET
        else:
            return str(word)

    @staticmethod
    def print_from_file(data):
        text = data.strip().split('\n')
        colored_words = list(map(Browser.highlight, text))
        final = "\n".join(colored_words)
        print(final)

    def write_data_to_file(self, site, data):
        Browser.path_validate(self.path_to_file)
        file_name = ".".join(site.split(".")[:-1])

        self.history.append(file_name)
        self.set_files_names.add(file_name)

        file_path = self.path_to_file + "/" + file_name + ".txt"
        with open(file_path, "w") as file:
            file.write(data)

    def run(self):
        while self.is_executable:
            web_page = input()

            if web_page in Browser.commands:
                self.command_execute(web_page)
                continue

            if web_page not in self.set_files_names and web_page.count(".") == 0:
                print("Error: Incorrect URL\n")
                continue

            if web_page in self.set_files_names:
                data = self.read_data_from_file(web_page)
                Browser.print_from_file(data)
                continue

            url_data = Browser.download_page_from_url(web_page)
            data = Browser.convert_html_to_text(url_data)
            if len(sys.argv) == 2 and web_page not in self.set_files_names:
                self.write_data_to_file(web_page, data)

if __name__ == "__main__":
    browser = Browser("")
    if len(sys.argv) == 2:
        browser = Browser(sys.argv[1])
    browser.run()