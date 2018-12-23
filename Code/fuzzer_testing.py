from fuzzing.fuzzer import FuzzExecutor
import glob
import logging

class FuzzerTest():
    def __init__(self):
        self.data = "Data/Stocks/"
        self.articles = "Articles/"
        self.files_lst_stocks = []
        self.files_lst_articles = []
        self.number_of_runs = 13
        self.apps_under_test = ["/Applications/Sublime Text.app/Contents/MacOS/Sublime Text"]
        logging.basicConfig(level=logging.INFO) # logging information

    def get_stocks(self):
        logging.info("Gathering stocks.")
        for index, file in enumerate(glob.glob(self.data+"*.csv")):
            self.files_lst_stocks.append(file)
        assert len(self.files_lst_stocks) > 0

    def get_articles(self):
        logging.info("Gathering articles.")
        for index, file in enumerate(glob.glob(self.articles + "*.csv")):
            self.files_lst_articles.append(file)
        assert len(self.files_lst_articles) > 0

    def test_stocks(self):
        self.get_stocks()
        logging.info("Running Fuzzing to test if stocks are valid.")
        fuzz_tester = FuzzExecutor(self.apps_under_test, self.files_lst_stocks)
        fuzz_tester.run_test(self.number_of_runs)
        return fuzz_tester.stats

    def test_articles(self):
        self.get_articles()
        logging.info("Running Fuzzing to test if articles are valid.")
        fuzz_tester = FuzzExecutor(self.apps_under_test, self.files_lst_articles)
        fuzz_tester.run_test(self.number_of_runs)
        return fuzz_tester.stats

    def main(self):
        stats = self.test_articles()
        print(stats)

if __name__ == '__main__':
    test = FuzzerTest()
    test.main()
